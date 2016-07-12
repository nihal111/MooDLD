#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import urllib
import mechanize
from Crypto.Cipher import DES

moodle = 'http://moodle.iitb.ac.in/login/index.php'
# Create a browser instance
br = mechanize.Browser()

# Declaring global arrays
# For keeping record of download pages
downloaded = []
# For keeping record of downloaded links
downloadlinks = []
# For making an array of CourseObject objects, online from moodle
online_courses = []
# Stores name of user
my_name = ''

"""
Flow Of Control:

-----
Home has following options:

1.  DLD files- Checks if "Preferences" exists. If not PrefScreen is opened.
    Else, courses stored in preferences are opened and their materials retrieved.

2.  Preferences- Open the PrefScreen which loads online_courses[] from moodle.
    Checks for existence of courses in "Preferences", if found, online_courses[i] parameters
    for corresponding course are updated.
    If a new course is found => get_nf_link() for that course. And set default parameters.
    Loads all online_courses as courseboxes (list of checkboxes and buttons).

    Save Settings- Saves the courseboxes and their corresponding parameters from online_courses to "Preferences".
    (Except directory as it may be changed. Directory is saved from courseboxes)

3.  Logout- Logs out and removes saved credentials and closes browser instance. Navigates to LoginFrame

"""


class CourseObject:
    """
    A class for storing CourseObject consisting of course url, course name,
    checkbox status, directory, nf link, last url from main url, last url from nf
    """

    def __init__(self,
                 mainlink,
                 name,
                 directory=None,
                 nflink=None,
                 lastmain=None,
                 lastnf=None):

        # Initialised with only mainlink and name (when retrieving from the web)
        if directory is None:
            self.mainlink = mainlink
            self.name = name
            self.directory = "C:/"
            self.lastnf = -1
            self.lastmain = -1
            self.nflink = ""

        else:
            self.mainlink = mainlink
            self.directory = directory
            self.name = name
            self.nflink = nflink
            self.lastmain = lastmain
            self.lastnf = lastnf

    # Get nf_link for any CourseObject
    def get_nf_link(self):
        br.open(self.mainlink)
        for link in br.links(url_regex='http://moodle.iitb.ac.in/mod/forum/view.php'):
            if "?f=" not in link.url and not link.url.endswith('id=340'):
                self.nflink = link.url


class LoginFrame:
    """
    Login to Moodle
    """

    def __init__(self):

        # TODO remove br
        global br

        # Reinitialize browser instance
        br = mechanize.Browser()
        # print('Opening Moodle...')

        # If Cred exists check for saved credentials

        if LoginFrame.check_connection() and os.path.exists('Cred'):
            with open('Cred', 'r') as Cred:
                cred = Cred.readlines()

                # if credentials are found, login. else do nothing

                if cred[0][0] == "1":
                    des = DES.new('01234567', DES.MODE_ECB)
                    space_pass = des.decrypt(str((cred[2])[:cred[2].index('\n')]).decode('hex'))[-1:]
                    decrypted_username = des.decrypt(str((cred[1])[:cred[1].index('\n')]).decode('hex'))
                    decrypted_password = des.decrypt(str((cred[2])[:cred[2].index('\n')]).decode('hex'))[:-(int(
                                                                                                        space_pass))]
                    LoginFrame.login(decrypted_username, decrypted_password)
                    # print(decrypted_username + " " + decrypted_password)
                    br.open(moodle)

    @staticmethod
    def login(username, password):
        """
        Submit form using arguments and set my_name to username
        """
        if LoginFrame.check_connection():
            br.select_form(nr=0)
            br['username'] = username
            br['password'] = password
            br.submit()
            if br.geturl() == 'http://moodle.iitb.ac.in/':
                profile = ""
                for link in br.links(url_regex='http://moodle.iitb.ac.in/user/profile.php'):
                    profile = link.url
                br.open(profile)
                global my_name
                my_name = br.title()[:br.title().index(':')]
                # print('Successful Login as ' + my_name)
            # else:
                # print('Incorrect username or password')

    @staticmethod
    def check_connection():
        """
        Check for connection availability
        """

        try:
            br.open('http://moodle.iitb.ac.in/login/index.php')
            return 1
        except EnvironmentError:
            # print('Could not connect to moodle, Please check your connection and try again!')
            return 0


class Home:
    """
    Frame for Home Screen.
    """

    def __init__(self):

        # array of all discussion urls
        self.urls = []
        # array of all downloadable files
        self.nflinks = []
        self.links = []
        # Download automatically on launch
        self.dld()

    def nfretrieve(self, url, directory, number):
        """
        Retrieve from News Forum when passed nfurl i.e forum/view.php
        Passed arguments forum url, directory, course number (as appearing in Preferences)
        """

        global downloaded
        global downloadlinks

        br.open(url)

        # Read lines from Preferences. Obtain last visited discussion for course at index=number
        preferences = open("Preferences", "r")
        lines = preferences.readlines()
        lasturl = (lines[7 * number + 6])[:lines[7 * number + 6].index("\n")]
        preferences.close()

        # Set flag for checking if any new threads have been created since last run
        flag = 0

        # create an array of all discussion links (self.urls)
        for link in br.links(url_regex="http://moodle.iitb.ac.in/mod/forum/discuss.php"):
            if link.url == lasturl:
                break
                # breaking loop once last visited discussion/thread is encountered
            if link.url not in self.urls:
                flag = 1
                self.urls.append(link.url)

        # Find newlasturl (last visited disussion/thread)
        # (Order of threads is in reverse. i.e Newest first)
        if flag == 1:
            newlasturl = self.urls[0] + '\n'

            # Update Preferences with newlasturl
            lines[number * 7 + 6] = newlasturl
            preferences = open("Preferences", "w")
            preferences.writelines(lines)
            preferences.close()

        # iterating through every discussion
        for url in self.urls:

            br.open(url)

            # create an array of all downloadables
            for link in br.links(url_regex="http://moodle.iitb.ac.in/pluginfile.php"):
                self.nflinks.append(link)

            # Download all downloadables
            for link in self.nflinks:
                br.open(link.url)
                url_text = br.geturl()
                if br.geturl().endswith('forcedownload=1'):
                    url_text = br.geturl()[:-16]
                file_extension = '.' + url_text.rsplit('.', 1)[-1]
                file_name = (url_text.rsplit('.', 1)[0]).rsplit('/', 1)[-1]
                file_name = urllib.unquote_plus(file_name)
                if file_name.endswith(file_extension):
                    file_name = file_name[:-len(file_extension)]
                if file_extension in ['.pdf', '.doc', '.ppt', '.pptx', '.docx',
                                      '.xls', '.xlsx', '.cpp', '.h', '.html',
                                      '.py', '.css', '.tex', '.java']:
                    if not os.path.exists(directory + file_name + file_extension):
                        if link.url not in downloadlinks:
                            # print('Downloading ' + file_name + file_extension +
                            #       ' to ' + directory)
                            if not os.path.isdir(directory):
                                os.makedirs(directory)
                            br.retrieve(link.url, directory + file_name + file_extension)
                            downloadlinks.append(link.url)

    def retrieve(self, url, directory):
        """
        Retrieve from course main page
        Arguments are main page url, directory
        """

        global downloaded
        global downloadlinks
        br.open(url)

        # Find all links inside given url and form array (self.links)
        for link in br.links(url_regex='.'):
            if (not link.url.startswith(
                    'http://moodle.iitb.ac.in/login/logout.php') and
                    not link.url.startswith(br.geturl()) and
                    not link.url.startswith('#') and
                    not link.url.startswith('http://moodle.iitb.ac.in/mod/forum') and
                    not link.url.startswith('http://moodle.iitb.ac.in/my') and
                    not link.url.startswith('http://moodle.iitb.ac.in/user') and
                    not link.url.startswith('http://moodle.iitb.ac.in/badges') and
                    not link.url.startswith('http://moodle.iitb.ac.in/calendar') and
                    not link.url.startswith('http://moodle.iitb.ac.in/grade') and
                    not link.url.startswith('http://moodle.iitb.ac.in/message') and
                    link.url not in downloaded):
                self.links.append(link)

        # Download all downloadable files from self.links
        for link in self.links:
            br.addheaders = [(
                'User-agent',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
            )]
            br.open(link.url)
            url_text = br.geturl()
            if br.geturl().endswith('forcedownload=1'):
                url_text = br.geturl()[:-16]
            file_extension = '.' + url_text.rsplit('.', 1)[-1]
            if file_extension in ['.pdf', '.doc', '.ppt', '.pptx', '.docx',
                                  '.xls', '.xlsx', '.cpp', '.h', '.html',
                                  '.py', '.css', '.tex', '.java']:

                # filename = ""
                if ']' in link.text:
                    file_name = link.text[link.text.index(']') + 1:]
                else:
                    file_name = link.text

                if file_name.endswith(file_extension):
                    file_name = file_name[:-len(file_extension)]

                if not os.path.exists(directory + file_name + file_extension):
                    if link.url not in downloadlinks:
                        # print('Downloading ' + file_name + file_extension +
                        #       ' to ' + directory)
                        if not os.path.isdir(directory):
                            os.makedirs(directory)
                        br.retrieve(link.url, directory + file_name + file_extension)
                        downloadlinks.append(link.url)
            else:
                # Retrieve from folders
                if (br.geturl().startswith(
                        'http://moodle.iitb.ac.in/mod/folder') and
                        link.url not in downloaded and
                        link.text.startswith('[IMG]')):
                    foldername = br.title()[br.title().index(':') + 2:]
                    newpath = directory + foldername
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    # print('Retrieving from ' + foldername + ' at ' + newpath)
                    downloaded.append(link.url)
                    self.retrieve(link.url, newpath + '/')

                # Retrieve Assignments
                if br.geturl().startswith('http://moodle.iitb.ac.in/mod/assign') and link.url not in downloaded:
                    downloaded.append(link.url)
                    if directory.endswith("Assignments/"):
                        newpath = directory[:-1]
                    else:
                        newpath = directory + "Assignments"
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    self.retrieve(link.url, newpath + '/')

            br.back()

    def dld(self):
        """
        On click of DLD Files button
        """
        if LoginFrame.check_connection():
            # print('Downloading files, Please do not close until complete!')
            urls = []
            nfurls = []
            directories = []

            # Open Preferences and call retrieve functions
            if os.path.exists('Preferences'):
                file_pref = open('Preferences', 'r')
                lines = file_pref.readlines()
                n = len(lines) / 7
                if len(lines):
                    for number in range(n):
                        urls.append(lines[7 * number + 2][:lines[7 * number +
                                                                 2].index('\n')])
                        directories.append(lines[7 * number + 3][:lines[7 * number + 3].index('\n')])
                        nfurls.append(lines[7 * number + 4][:lines[7 * number + 4].index("\n")])
                        if (lines[7 * number])[:lines[7 * number].index('\n')] == '1':
                            # print('Retrieving from ' + lines[
                            #     7 * number + 1][:lines[7 * number + 1].index('\n')] + ' at ' + directories[number])
                            self.retrieve(urls[number], directories[number])
                            # print("Retrieving from " + lines[
                            #     7 * number + 1][:lines[7 * number + 1].index("\n")] + " News Forum at " + directories[
                            #           number] + 'News Forum/')
                            self.nfretrieve(nfurls[number], directories[number] + 'News Forum/', number)
                # print("Successfully synced with Moodle!")

                # If Preferences does not exist take user to Preferences screen
            # else:
                # print('Please set Preferences first!')


class PrefScreen:
    """
    Load courses according to preferences
    """

    @staticmethod
    def load_online_courses():
        """
        Finds all links for course main pages and creates CourseObject objects
        """
        br.open('http://moodle.iitb.ac.in/')

        for link in br.links(url_regex='http://moodle.iitb.ac.in/course/view.php'):
            online_courses.append(CourseObject(link.url, link.text))

    @staticmethod
    def update_from_preferences(n):
        """
        Finds courses from Preferences and updates parameters
        for corresponding course in online_courses
        """

        if os.path.exists('Preferences'):
            file_pref = open('Preferences', 'r')
            lines = file_pref.readlines()
            total_in_preferences = len(lines) / 7
            if len(lines):
                for number in range(0, total_in_preferences):
                    for i in range(0, n):
                        if online_courses[i].mainlink in lines[7 * number + 2]:
                            online_courses[i].directory = lines[7 * number + 3][:lines[7 * number + 3].index('\n')]
                            online_courses[i].nflink = lines[7 * number + 4][:lines[7 * number + 4].index('\n')]
                            break

        # get_nf_link for all courses that don't have an nflink
        for i in range(0, n):
            if online_courses[i].nflink is "":
                online_courses[i].get_nf_link()

    def __init__(self):

        global my_name
        del online_courses[:]

        PrefScreen.load_online_courses()
        n = len(online_courses)

        PrefScreen.update_from_preferences(n)

# Log into account
l = LoginFrame()

# Start download
h = Home()
