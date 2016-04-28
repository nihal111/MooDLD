#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import urllib
from Tkinter import Frame, Label, Button, Checkbutton, IntVar, StringVar, Entry, Scrollbar, Canvas
import tkMessageBox as tm
import tkFileDialog
import Tkinter
import mechanize
from Crypto.Cipher import DES

moodle = 'http://moodle.iitb.ac.in/login/index.php'
# Create a browser instance
br = mechanize.Browser()

#Declaring global arrays
#For box objects in Pref_Screen. Consists of checkbox, label and button
courseboxes = []
#For keeping record of download pages
downloaded = []
#For keeping record of downloaded links
downloadlinks = []
#For making an array of course_object objects, online from moodle
online_courses = []
#Stores name of user
myname = ''
#Boolean for force terminate Download
stop_DLD = False
#Boolean for whether DLD files is initiated once
auto_download = False

if os.path.exists('Cred'):
    file_pref = open('Cred', 'r')
    lines = file_pref.readlines()
    if len(lines) > 4:
        x = lines[4].replace('\n', '')
        if x == '1':
            auto_download = True
    file_pref.close()

'''
Flow Of Control:

1. m=Tkinter.Tk()
Creates a tkinter GUI frame

2. t=TraceConsole()
Creates the trace Console for logging

3.LoginFrame(m)
Passes the tkinter frame to LoginFrame class
i.e Login screen opens invariably the first time.

Screen elements are initialised and then saved credentials are checked for existence.
If saved credentials are found it moves on to Home.

-----
Home has following options:

1.  DLD files- Checks if "Preferences" exists. If not Pref_Screen is opened.
    Else, courses stored in preferences are opened and their materials retrieved.

2.  Preferences- Open the Pref_Screen which loads online_courses[] from moodle.
    Checks for existence of courses in "Preferences", if found, online_courses[i] parameters for corresponding course are updated.
    If a new course is found => get_nf_link() for that course. And set default parameters.
    Loads all online_courses as courseboxes (list of checkboxes and buttons).

    Save Settings- Saves the courseboxes and their corresponding parameters from online_courses to "Preferences".
    (Except directory as it may be changed. Directory is saved from courseboxes)

3.  Logout- Logs out and removes saved credentials and closes browser instance. Navigates to LoginFrame

'''


class ScrollableFrame(Frame):

    '''
    Creates a vertically and horizontally scrollable frame for Pref_Screen
    '''

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=Tkinter.VERTICAL)
        vscrollbar.pack(fill=Tkinter.Y, side=Tkinter.RIGHT, expand=Tkinter.FALSE)

        hscrollbar = Scrollbar(self, orient=Tkinter.HORIZONTAL)
        hscrollbar.pack(fill=Tkinter.X, side=Tkinter.BOTTOM, expand=Tkinter.FALSE)

        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        canvas.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=Tkinter.TRUE)
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)


        # reset the view

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it

        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=Tkinter.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):

            '''
            update the scrollbars to match the size of the inner frame
            '''
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion='0 0 %s %s' % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):

            '''
            _configure_canvas is used to resize the window size to fit content.
            Can be used when changing window.
            '''

            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        #calls the function _configure_canvas
        #canvas.bind('<Configure>', _configure_canvas)


class TraceConsole:

    '''
    Creates a Frame for Logging Messages
    '''

    def __init__(self):

        '''
        Init the main GUI window
        '''

        self._logFrame = Tkinter.Frame()
        self._log = Tkinter.Text(self._logFrame, wrap=Tkinter.NONE,
                                 setgrid=True, height=8, width=90)
        self._scrollb = Tkinter.Scrollbar(self._logFrame, orient=Tkinter.VERTICAL)
        self._scrollb.config(command=self._log.yview)
        self._log.config(yscrollcommand=self._scrollb.set)
        self._scrolla = Tkinter.Scrollbar(self._logFrame, orient=Tkinter.HORIZONTAL)
        self._scrolla.config(command=self._log.xview)
        self._log.config(xscrollcommand=self._scrolla.set)

        # Grid & Pack

        self._log.grid(column=0, row=0)
        self._scrollb.grid(column=1, row=0, sticky=Tkinter.S
                           + Tkinter.N)
        self._scrolla.grid(column=0, row=5, sticky=Tkinter.E
                           + Tkinter.W)
        self._logFrame.pack()

    def log(self, msg, level=None):

        '''
        Write on GUI
        '''

        self._log.insert('end', msg + '\n')
        self._log.see(Tkinter.END)


class course_object:

    '''
    A class for storing course_object consisting of course url, course name,
    checkbox status, directory, nf link, last url from main url, last url from nf
    '''

    def __init__(self, mainlink, name, chkbox=None, directory=None,
                 nflink=None, lastmain=None, lastnf=None):

        #Initialised with only mainlink and name (when retrieving from the web)
        if chkbox is None:
            self.mainlink = mainlink
            self.name = name
            self.chkbox = "0"
            self.directory = "C:/"
            self.lastnf = -1
            self.lastmain = -1
            self.nflink = ""

        else:
            self.chkbox = chkbox
            self.mainlink = mainlink
            self.directory = directory
            self.name = name
            self.nflink = nflink
            self.lastmain = lastmain
            self.lastnf = lastnf

    #Get nf_link for any course_object
    def get_nf_link(self):
        br.open(self.mainlink)
        for link in br.links(url_regex='http://moodle.iitb.ac.in/mod/forum/view.php'):
            if "?f=" not in link.url and not link.url.endswith('id=340'):
                self.nflink = link.url


class LoginFrame(Frame):

    '''
    Frame for login page.
    '''

    def __init__(self, master):
        Frame.__init__(self)
        self.username_label = Label(self, text='Username')
        self.password_label = Label(self, text='Password')
        self.x = IntVar()
        self.username = Entry(self)
        self.password = Entry(self, show='*')
        self.keep_me_logged_in = IntVar()
        self.username_label.grid(row=0, sticky=Tkinter.W)
        self.password_label.grid(row=1, sticky=Tkinter.W)
        self.username.grid(row=0, column=1)
        self.password.grid(row=1, column=1)

        # Keep me logged in state saved in var

        self.checkbox = Checkbutton(self, text='Keep me logged in',
                                    variable=self.keep_me_logged_in)
        self.checkbox.grid(columnspan=2)

        # login button, onClick = _login_btn_clicked

        self.loginbtn = Button(self, text='Login',
                               command=self._login_btn_clicked)
        self.loginbtn.grid(columnspan=2)

        self.pack()

        global br
        global t

        #Reinitialize browser instance
        br = mechanize.Browser()
        t.log('Opening Moodle...')

        # If Cred exists check for saved credentials

        if self.check_connection() and os.path.exists('Cred'):
            with open('Cred', 'r') as Cred:
                cred = Cred.readlines()

                # if credentials are found, login. else do nothing

                if cred[0][0] == "1":
                    des = DES.new('01234567', DES.MODE_ECB)
                    space_pass = des.decrypt(str((cred[2])[:cred[2].index('\n')]).decode('hex'))[-1:]
                    decrypted_username = des.decrypt(str((cred[1])[:cred[1].index('\n')]).decode('hex'))
                    decrypted_password = des.decrypt(str((cred[2])[:cred[2].index('\n')]).decode('hex'))[:-(int(space_pass))]
                    self.login(decrypted_username, decrypted_password)
                    br.open(moodle)

    def _login_btn_clicked(self):

        '''
        On login button click
        '''
        t.log('Attempting login...')
        #Check for connection and write to Cred
        if self.check_connection():
            #Default cred content excluding keep_me_logged_in, username and password.
            #Default directory: C:/ Default auto download ON
            lines = ["\n","\n","\n","Select Root Directory for all courses\n","1\n"]
            if os.path.exists("Cred"):
                file_cred = open('Cred', 'r')
                lines = file_cred.readlines()
                file_cred.close()

            lines[0] = str(self.keep_me_logged_in.get()) + '\n'
            if self.keep_me_logged_in.get():
                des = DES.new('01234567', DES.MODE_ECB)
                username = self.username.get()
                password = self.password.get()
                space_pass = 8 - len(password) % 8
                username += ' ' * (8 - len(username) % 8)
                password = password + ' ' * ((8 - len(password) % 8) - 1) + str(space_pass)
                encrypted_username = des.encrypt(username).encode('hex')
                encrypted_password = des.encrypt(password).encode('hex')
                lines[1] = encrypted_username + '\n'
                lines[2] = encrypted_password + '\n'

            else:
                lines[1] = '\n'
                lines[2] = '\n'

            file_cred = open('Cred', 'w')
            file_cred.writelines(lines)
            file_cred.close()

            if lines[4][0] == "1":
                add_to_startup()

            self.login(self.username.get(), self.password.get())

    def login(self, username, password):

        '''
        Submit form using arguments and set myname to username
        '''

        br.select_form(nr=0)
        br['username'] = username
        br['password'] = password
        br.submit()
        if br.geturl() == 'http://moodle.iitb.ac.in/':
            for link in \
                br.links(url_regex='http://moodle.iitb.ac.in/user/profile.php'):
                self.profile = link.url
            br.open(self.profile)
            global myname
            myname = br.title()[:br.title().index(':')]
            self.new_window()
            t.log('Successful Login as ' + myname)
        else:
            t.log('Incorrect username or password')

    def check_connection(self):
        '''
        Check for connection availability
        '''

        try:
            br.open('http://moodle.iitb.ac.in/login/index.php')
            return 1
        except:
            t.log('Could not connect to moodle, Please check your connection and try again!')
            m.update()
            return 0

    def new_window(self):

        '''
        Go to Home screen
        '''

        self.destroy()
        self.newWindow = Home(self.master)


class Home(Frame):

    '''
    Frame for Home Screen.
    '''

    def __init__(self, master):
        Frame.__init__(self)
        self.pack()
        self.Name = 'Welcome ' + str(myname)
        self.label_1 = Label(self, text=self.Name, justify=Tkinter.LEFT)
        self.label_1.grid(row=0, pady=5)
        self.sync = Button(self, text="DLD Files", command=self.DLD)
        self.sync.grid(row=1, pady=5)
        self.pref = Button(self, text="Preferences", command=self.pref)
        self.pref.grid(row=3, pady=5)
        self.logout = Button(self, text="Logout", command=self.logout)
        self.logout.grid(row=4, pady=5)
        self.stop = Button(self, text="Stop DLD", command=self.stopDLD)
        self.stop.grid(row=2, pady=5)
        self.stop.config(state='disabled')

        #Download automatically on launch
        if auto_download is True:
            t.log("Download automatically started. This can be disabled from preferences")
            self.dld()

    def nfretrieve(self, url, directory, number):

        '''
        Retrieve from News Forum when passed nfurl i.e forum/view.php
        Passed arguments forum url, directory, course number (as appearing in Preferences)
        '''

        m.update()
        global t
        #array of all discussion urls
        self.urls = []
        #array of all downloadables
        self.nflinks = []
        global downloaded
        global downloadlinks

        br.open(url)

        #Read lines from Preferences. Obtain last visited discussion for course at index=number
        preferences = open("Preferences", "r")
        lines = preferences.readlines()
        lasturl = (lines[7*number+6])[:lines[7*number+6].index("\n")]
        preferences.close()

        #Set flag for checking if any new threads have been created since last run
        flag = 0

        #create an array of all discussion links (self.urls)
        #Newer threads come first in br.links()
        for link in br.links(url_regex="http://moodle.iitb.ac.in/mod/forum/discuss.php"):
            if link.url == lasturl:
                break
                #breaking loop once last visited discussion/thread is encountered
            if link.url not in self.urls:
                flag = 1
                self.urls.append(link.url)

        #iterating through every discussion
        for url in self.urls:
            m.update()

            br.open(url)

            #create an array of all downloadables
            for link in br.links(url_regex="http://moodle.iitb.ac.in/pluginfile.php"):
                self.nflinks.append(link)

            #Download all downloadables
            for link in self.nflinks:
                if stop_DLD:
                    #Set flag 0 so that newlasturl is not updated, as all new threads may not be downloaded when force killed.
                    flag=0
                    break
                else:
                    m.update()
                    br.open(link.url)
                    url_text = br.geturl()
                    if br.geturl().endswith('forcedownload=1'):
                        url_text = br.geturl()[:-16]
                    file_extension = '.' + url_text.rsplit('.', 1)[-1]
                    file_name = (url_text.rsplit('.', 1)[0]).rsplit('/', 1)[-1]
                    file_name = urllib.unquote_plus(file_name)
                    if file_name.endswith(file_extension):
                        file_name = file_name[:-len(file_extension)]
                    if file_extension in ['.pdf', '.doc', '.ppt', '.pptx', '.docx', '.xls', '.xlsx',
                                          '.cpp', '.h', '.html', '.py', '.css', '.tex', '.java']:
                        if not os.path.exists(directory + file_name + file_extension):
                            if not link.url in downloadlinks:
                                t.log('Downloading ' + file_name
                                      + file_extension + ' to ' + directory)
                                if not os.path.isdir(directory):
                                    os.makedirs(directory)
                                br.retrieve(link.url, directory + file_name + file_extension)
                                downloadlinks.append(link.url)

        #Find newlasturl (last visited disussion/thread)
        #(Order of threads is in reverse. i.e Newest first)
        if flag == 1:
            newlasturl = self.urls[0]+'\n'

            #Update Preferences with newlasturl
            lines[number*7+6] = newlasturl
            preferences = open("Preferences", "w")
            preferences.writelines(lines)
            preferences.close()


    def retrieve(self, url, directory):
        '''
        Retrieve from course main page
        Arguments are main page url, directory
        '''

        m.update()
        global t
        global downloaded
        global downloadlinks
        self.links = []
        br.open(url)

        #Find all links inside given url and form array (self.links)
        for link in br.links(url_regex='.'):
            if (not link.url.startswith('http://moodle.iitb.ac.in/login/logout.php')
                    and not link.url.startswith(br.geturl())
                    and not link.url.startswith('#')
                    and not link.url.startswith('http://moodle.iitb.ac.in/mod/forum')
                    and not link.url.startswith('http://moodle.iitb.ac.in/my')
                    and not link.url.startswith('http://moodle.iitb.ac.in/user')
                    and not link.url.startswith('http://moodle.iitb.ac.in/badges')
                    and not link.url.startswith('http://moodle.iitb.ac.in/calendar')
                    and not link.url.startswith('http://moodle.iitb.ac.in/grade')
                    and not link.url.startswith('http://moodle.iitb.ac.in/message')
                    and link.url not in downloaded):
                self.links.append(link)

        #Downlod all downloadables from self.links
        for link in self.links:
            if stop_DLD:
                break
            else:
                m.update()
                br.open(link.url)
                url_text = br.geturl()
                if br.geturl().endswith('forcedownload=1'):
                    url_text = br.geturl()[:-16]
                file_extension = '.' + url_text.rsplit('.', 1)[-1]
                if file_extension in ['.pdf', '.doc', '.ppt', '.pptx', '.docx', '.xls', '.xlsx',
                                      '.cpp', '.h', '.html', '.py', '.css', '.tex', '.java']:

                    file_name = ""
                    if ']' in link.text:
                        file_name = link.text[link.text.index(']') + 1:]
                    else:
                        file_name = link.text

                    if file_name.endswith(file_extension):
                        file_name = file_name[:-len(file_extension)]

                    if not os.path.exists(directory + file_name + file_extension):
                        if not link.url in downloadlinks:
                            t.log('Downloading ' + file_name
                                  + file_extension + ' to ' + directory)
                            if not os.path.isdir(directory):
                                os.makedirs(directory)
                            br.retrieve(link.url, directory + file_name + file_extension)
                            downloadlinks.append(link.url)
                else:
                    #Retrieve from folders
                    if (br.geturl().startswith('http://moodle.iitb.ac.in/mod/folder')
                            and link.url not in downloaded
                            and link.text.startswith('[IMG]')):
                        foldername = br.title()[br.title().index(':') + 2:]
                        newpath = directory + foldername
                        if not os.path.exists(newpath):
                            os.makedirs(newpath)
                        t.log('Retrieving from ' + foldername + ' at '
                              + newpath)
                        downloaded.append(link.url)
                        self.retrieve(link.url, newpath + '/')

                    #Retrieve Assignments
                    if br.geturl().startswith('http://moodle.iitb.ac.in/mod/assign') \
                                                and link.url not in downloaded:
                        downloaded.append(link.url)
                        if directory.endswith("Assignments/"):
                            newpath = directory[:-1]
                        else:
                            newpath = directory + "Assignments"
                        if not os.path.exists(newpath):
                            os.makedirs(newpath)
                        self.retrieve(link.url, newpath + '/')

            #br.back()
            self.pack()

    def stopDLD(self):
        '''
        On click of Stop DLD button
        '''

        global t, stop_DLD
        t.log('Terminating downloads.')
        stop_DLD = True

    def DLD(self):

        '''
        On click of DLD Files button
        '''

        global t, stop_DLD
        t.log('Downloading files, Please do not close until complete!')
        self.sync.config(state='disabled')
        self.pref.config(state='disabled')
        self.logout.config(state='disabled')
        self.stop.config(state='normal')
        urls = []
        nfurls = []
        directories = []
        stop_DLD = False

        #Open Preferences and call retrieve functions
        if os.path.exists('Preferences'):
            file_pref = open('Preferences', 'r')
            lines = file_pref.readlines()
            n = len(lines) / 7
            if len(lines):
                for number in range(n):
                    if stop_DLD:
                        break
                    else:
                        urls.append(lines[7 * number + 2][:lines[7 * number + 2].index('\n')])
                        directories.append(lines[7 * number + 3][:lines[7 * number + 3].index('\n')])
                        nfurls.append(lines[7*number+4][:lines[7*number+4].index("\n")])
                        if (lines[7 * number])[:lines[7 * number].index('\n')] == '1':
                            t.log('Retrieving from ' + lines[7 * number+ 1]
                                  [:lines[7 * number + 1].index('\n')] + ' at ' + directories[number])
                            self.retrieve(urls[number], directories[number])
                            t.log("Retrieving from "+ lines[7*number+1][:lines[7*number+1].index("\n")]
                                  + " News Forum at " + directories[number] + 'News Forum/')
                            self.nfretrieve(nfurls[number], directories[number] + 'News Forum/', number)
            t.log("Successfully synced with Moodle!")
            self.sync.config(state='normal')
            self.pref.config(state='normal')
            self.logout.config(state='normal')
            self.stop.config(state='disabled')

            #If Preferences does not exist take user to Preferences screen
        else:
            t.log('Please set Preferences first!')
            self.sync.config(state='normal')
            self.pref.config(state='normal')
            self.logout.config(state='normal')
            self.destroy()
            self.newWindow = Pref_Screen(self.master)


    def pref(self):

        '''
        On Click Preferences button
        '''

        t.log("Populating list of courses. This may take a while. Please be patient..")
        m.update()
        self.destroy()
        self.newWindow = Pref_Screen(self.master)

    def logout(self):

        '''
        On Click Logout button
        '''
        lines = ["\n","\n","\n","C:/","\n","1","\n"]
        if os.path.exists("Cred"):
            file_cred = open('Cred', 'r')
            lines = file_cred.readlines()
            file_cred.close()

            lines[0] = '\n'
            lines[1] = '\n'
            lines[2] = '\n'

        file_cred = open('Cred', 'w')
        file_cred.writelines(lines)
        file_cred.close()
        t.log('Logout successful!')
        br.close()
        self.destroy()
        self.newWindow = LoginFrame(self.master)


class Pref_Screen(Frame):

    '''
    Frame for Preferences screen.
    '''

    def sall(self):
        '''
        On CLick Select All button
        '''
        n = len(online_courses)
        for i in range(0, n):
            courseboxes[i].checkbox.select()

    def dall(self):
        '''
        On CLick Deselect All button
        '''
        n = len(online_courses)
        for i in range(0, n):
            courseboxes[i].checkbox.deselect()

    def save(self):
        '''
        On CLick Save Settings button
        '''
        #Saves courseboxes and online_courses data to Preferences
        open('Preferences', 'w').close()
        preferences = open('Preferences', 'w')
        for i in range(0, len(online_courses)):
            x = str(courseboxes[i].directory.get())
            if not x.endswith('/'):
                courseboxes[i].directory.set(x + '/')
            preferences.write(str(courseboxes[i].var.get()) + '\n')
            preferences.write(online_courses[i].name + '\n')
            preferences.write(online_courses[i].mainlink + '\n')
            preferences.write(courseboxes[i].directory.get() + '\n')
            preferences.write(online_courses[i].nflink + '\n')
            preferences.write(str(online_courses[i].lastmain) + '\n')
            preferences.write(str(online_courses[i].lastnf) + '\n')
            courseboxes[i].pack_forget()

        preferences.close()

        #Go to Home screen
        self.frame.destroy()
        self.newWindow = Home(m)

        #Save root directory address to Cred
        creds = open('Cred', 'r')
        lines = creds.readlines()
        creds.close()

        creds = open('Cred', 'w')
        lines[3] = self.root_dir_box.directory.get() + '\n'
        lines[4] = str(self.auto.get()) + '\n'

        creds.writelines(lines)
        creds.close()

        #Add key to registry for startup launch
        if self.auto.get() == 1:
            add_to_startup()
        #Remove key from registry for starup launch
        else:
            remove_from_startup()

    def load_online_courses(self):
        '''
        Finds all links for course main pages and creates course_object objects
        '''
        br.open('http://moodle.iitb.ac.in/')

        for link in br.links(url_regex='http://moodle.iitb.ac.in/course/view.php'):
            online_courses.append(course_object(link.url, link.text))

    def update_from_preferences(self, n):
        '''
        Finds courses from Preferences and updates parameters
        for corresponding course in online_courses
        '''

        if os.path.exists('Preferences'):
            file_pref = open('Preferences', 'r')
            lines = file_pref.readlines()
            TotalInPreferences = len(lines) / 7
            if len(lines):
                for number in range(0, TotalInPreferences):
                    for i in range(0, n):
                        if online_courses[i].mainlink in lines[7 * number + 2]:
                            online_courses[i].directory = lines[7 * number + 3]\
                                                        [:lines[7 * number + 3].index('\n')]
                            online_courses[i].chkbox = lines[7 * number]\
                                                     [:lines[7 * number].index('\n')]
                            online_courses[i].nflink = lines[7 * number + 4]\
                                                     [:lines[7 * number + 4].index('\n')]
                            break

        #get_nf_link for all courses that don't have an nflink
        for i in range(0, n):
            if online_courses[i].nflink is "":
                online_courses[i].get_nf_link()

    def __init__(self, master):

        global myname
        del courseboxes[:]
        del online_courses[:]

        self.load_online_courses()
        n = len(online_courses)

        self.update_from_preferences(n)

        self.frame = ScrollableFrame(m)

        self.frame.pack(fill=Tkinter.BOTH, expand=Tkinter.TRUE)

        self.root_dir_box = box(self.frame)

        #Create checkbox, label and browse button for all courses
        for i in range(0, n):
            courseboxes.append(box(self.frame, i))

        self.selectall = Button(self.frame.interior, text='Select All',
                                command=self.sall)
        self.selectall.grid(row=0, column=0, pady=10)
        self.deselectall = Button(self.frame.interior,
                                  text='Deselect All',
                                  command=self.dall)
        self.deselectall.grid(row=0, column=1, padx=[0, 100], pady=10)
        self.save = Button(self.frame.interior, text='Save Settings',
                           command=self.save)
        self.save.grid(row=0, column=2, pady=10)

        self.auto = IntVar()
        self.autoDLD = Checkbutton(self.frame.interior, text="Auto-Download", width=20,
                                   variable=self.auto)
        self.autoDLD.grid(row=0, column=0, sticky="w")

        if os.path.exists('Cred'):
            file_pref = open('Cred', 'r')
            lines = file_pref.readlines()
            if len(lines) > 4:
                x = lines[4].replace('\n', '')
                if x == '1':
                    self.autoDLD.select()

        self.f = Frame(self.frame.interior, height=20)
        self.f.grid(row=2, columnspan=3, sticky="we")


class box(Frame):
    '''
    Class for box object having checkbox, label, browsebutton
    '''

    def getdir(self):
        '''
        On click for browse button of courses
        '''
        directory = tkFileDialog.askdirectory(parent=m, initialdir='C:/',
                                              title='Please select a directory')
        if len(directory) > 0:
            self.directory.set(directory)

    def rootgetdir(self):
        '''
        On click for browse button for Root directory
        '''
        directory = tkFileDialog.askdirectory(parent=m, initialdir='C:/',
                                              title='Please select a directory')
        if len(directory) > 0:
            self.directory.set(directory)
            for i in range(len(courseboxes)):
                courseboxes[i].directory.set(directory +'/' + online_courses[i].name[:6])
        else:
            self.directory.set('C:/')

    def __init__(self, master, number=None):
        Frame.__init__(self)
        self.var = IntVar()

        #For courseboxes
        if number is not None:
            self.directory = StringVar()
            self.checkbox = Checkbutton(master.interior,
                                        text=online_courses[number].name, width=60,
                                        variable=self.var, anchor="w")
            self.checkbox.grid(row=number + 3, column=0, padx=5)
            self.browse = Button(master.interior, text='Browse',
                                 command=self.getdir)
            self.browse.grid(row=number + 3, column=1)

            if online_courses[number].chkbox == '1':
                self.checkbox.select()
            self.directory.set(online_courses[number].directory)
            self.label_dir = Label(master.interior,
                                   textvariable=self.directory)
            self.label_dir.grid(row=number + 3, column=2)

        #For root_dir_box
        else:
            self.directory = StringVar()
            self.label = Label(master.interior,
                               text='Root Directory', width=60)
            self.label.grid(row=1, column=0)
            self.browse = Button(master.interior, text='Browse',
                                 command=self.rootgetdir)
            self.browse.grid(row=1, column=1)

            if os.path.exists('Cred'):
                file_pref = open('Cred', 'r')
                lines = file_pref.readlines()
                if len(lines) > 4:
                    self.directory.set(lines[3].replace('\n', ''))
                else:
                    self.directory.set('C:/')
            else:
                self.directory.set('C:/')

            self.label_dir = Label(master.interior, textvariable=self.directory)
            self.label_dir.grid(row=1, column=2)

def add_to_startup():
    #Find path to exe file from current working directory
    exe_path = os.path.join(os.getcwd(),"MooDLD.exe")
    os.popen("REG ADD \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\" /V \"MooDLD\" /t REG_SZ /F /D " + exe_path)

def remove_from_startup():
    os.popen("REG DELETE \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\" /V \"MooDLD\" /F")

#Main Program
m = Tkinter.Tk()
t = TraceConsole()

#Set Window title
m.wm_title('MooDLD')

#Set icon if found
try:
    m.iconbitmap('moodle.ico')
except:
    t.log("Icon Not Found. Keep `moodle.ico` in same directory!")

l = LoginFrame(m)
m.mainloop()
