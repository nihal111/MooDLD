#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox as tm
import mechanize
import tkFileDialog
import os
import logging
import Tkinter

moodle = 'http://moodle.iitb.ac.in/login/index.php'
br = mechanize.Browser()

TotalInMoodle = 0
TotalInPreferences = 0


courseboxes = []
downloaded = []
downloadlinks = []
online_courses = []
myname = ''

'''
TTDs:

Flow Of Control:
1. m=Tkinter.Tk()
Creates a tkinter GUI frame

2. t=TraceConsole()
Creates the trace Console for logging

3.LoginFrame(m)
Passes the tkinter frame to LoginFrame class
i.e Login screen opens invariably the first time.
Initialises the screen elements and then checks for saved credentials
'''


class VerticalScrolledFrame(Frame):

    '''
    Creates Scrollable frame for Preferences page
    '''

    def __init__(self, parent, *args, **kw):
        '''
        Constructor
        '''

        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient = VERTICAL)
        vscrollbar.pack(fill = Y, side = RIGHT, expand = FALSE)

        hscrollbar = Scrollbar(self, orient = HORIZONTAL)
        hscrollbar.pack(fill = X, side = BOTTOM, expand = FALSE)

        canvas = Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set, xscrollcommand = hscrollbar.set)
        canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)
        vscrollbar.config(command = canvas.yview)
        hscrollbar.config(command = canvas.xview)


        # reset the view

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it

        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion='0 0 %s %s' % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width = interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        #_configure_canvas is used to resize the window size to fit content. Can be used when changing window.
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width = canvas.winfo_width())
        #calls the function _configure_canvas
        #canvas.bind('<Configure>', _configure_canvas)

class TraceConsole:  # Log Messages

    def __init__(self):

        # Init the main GUI window

        self._logFrame = Tkinter.Frame()
        self._log = Tkinter.Text(self._logFrame, wrap=Tkinter.NONE,
                                 setgrid=True, height=8, width=90)
        self._scrollb = Tkinter.Scrollbar(self._logFrame,
                orient=Tkinter.VERTICAL)
        self._scrollb.config(command=self._log.yview)
        self._log.config(yscrollcommand=self._scrollb.set)
        self._scrolla = Tkinter.Scrollbar(self._logFrame,
                orient=Tkinter.HORIZONTAL)
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

        # Write on GUI

        self._log.insert('end', msg + '\n')
        self._log.see(Tkinter.END)


class savedata:

    def __init__(self, mainlink, name, chkbox=None, directory=None, nflink=None, lastmain=None, lastnf=None):
        
        if chkbox is None:
            self.mainlink = mainlink
            self.name = name
            self.chkbox = "0"
            self.directory = "C:/"
            self.lastnf = -1
            self.lastnf = -1
            self.nflink = ""


        else:        
            self.chkbox = chkbox
            self.mainlink = mainlink
            self.directory = directory
            self.name = name
            self.nflink = nflink
            self.lastmain = lastmain
            self.lastnf = lastnf

    def get_nf_link(self):

        br.open(self.mainlink)
        for link in br.links(url_regex='http://moodle.iitb.ac.in/mod/forum/view.php'):
            if ("?f=" not in link.url and not link.url.endswith('id=340')):
                self.nflink = link.url
                print link.url


class LoginFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self)
        self.username_label = Label(self, text='Username')
        self.password_label = Label(self, text='Password')
        self.x = IntVar()
        self.username = Entry(self)
        self.password = Entry(self, show='*')
        self.keep_me_logged_in = IntVar()
        self.username_label.grid(row=0, sticky=W)
        self.password_label.grid(row=1, sticky=W)
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
        br = mechanize.Browser()
        t.log('Opening Moodle...')

        # If Cred.txt exists check for saved credentials

        if self.check_connection() and os.path.exists('Cred.txt'):
            with open('Cred.txt', 'r') as Cred:
                cred = Cred.readlines()

                # if credentials are found, login. else do nothing

                if int(cred[0][0]) == 1:
                    self.login(str((cred[1])[:cred[1].index('\n')]),
                               str((cred[2])[:cred[2].index('\n')]))
                    br.open(moodle)

    # On login button click

    def _login_btn_clicked(self):
        t.log('Attempting login...')
        if self.check_connection():

            with open('Cred.txt', 'w') as text_file:

                # var contains boolean for keep me logged in, entry_1 and entry_2 are username passwords

                if self.keep_me_logged_in.get():
                    text_file.write(str(self.keep_me_logged_in.get()) + '\n')
                    text_file.write(self.username.get() + '\n')
                    text_file.write(self.password.get() + '\n')
                    text_file.write('C:/')
                else:
                    text_file.write(str(self.keep_me_logged_in.get()) + '\n')
                    text_file.write('\n')
                    text_file.write('\n')
                    text_file.write('C:/')
                text_file.close()

                self.login(self.username.get(), self.password.get())

    def login(self, username, password):
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

        # Check for connection issues

        try:
            br.open('http://moodle.iitb.ac.in/login/index.php')
            return 1
        except:
            t.log('Could not connect to moodle, Please check your connection and try again!')
            m.update()
            return 0

    def new_window(self):
        self.destroy()
        self.newWindow = Sync(self.master)

class Sync(Frame):

    def __init__(self,master):
        Frame.__init__(self)
        self.pack()
        self.Name = 'Welcome ' + str(myname)
        self.label_1 = Label(self, text = self.Name, justify = LEFT)
        self.label_1.grid(row = 0,pady = 5)
        self.sync= Button(self, text = "DLD Files",command = self.dld)
        self.sync.grid(row = 1,pady = 5)
        self.pref=Button(self, text = "Preferences", command = self.pref)
        self.pref.grid(row = 2,pady = 5)
        self.logout=Button(self, text = "Logout", command = self.logout)
        self.logout.grid(row = 3,pady = 5)

    
    def retrieve(self, url, directory):
        m.update()
        global t
        global downloaded
        global downloadlinks
        self.links = []
        br.open(url)
        for link in br.links(url_regex='.'):
            if not link.url.startswith('http://moodle.iitb.ac.in/login/logout.php'
                    ) and not link.url.startswith(br.geturl()) \
                and not link.url.startswith('#') \
                and not link.url.startswith('http://moodle.iitb.ac.in/mod/forum'
                    ) \
                and not link.url.startswith('http://moodle.iitb.ac.in/my'
                    ) \
                and not link.url.startswith('http://moodle.iitb.ac.in/user'
                    ) \
                and not link.url.startswith('http://moodle.iitb.ac.in/badges'
                    ) \
                and not link.url.startswith('http://moodle.iitb.ac.in/calendar'
                    ) \
                and not link.url.startswith('http://moodle.iitb.ac.in/grade'
                    ) \
                and not link.url.startswith('http://moodle.iitb.ac.in/message'
                    ) and link.url not in downloaded:
                self.links.append(link)

        for link in self.links:
            m.update()

            br.open(link.url)
            url_text = br.geturl()
            if br.geturl().endswith('forcedownload=1'):
                url_text = br.geturl()[:-16]
            url_text = '.' + url_text.rsplit('.', 1)[-1]
            if url_text in ['.pdf', '.doc', '.ppt', '.pptx', '.docx', '.xls', '.xlsx']:

                if ']' in link.text:
                    if not os.path.exists(directory
                            + link.text[link.text.index(']') + 1:] + url_text):
                        if not link.url in downloadlinks:
                            t.log('Downloading '
                                  + link.text[link.text.index(']')
                                  + 1:] + url_text + ' to ' + directory)
                            if not os.path.isdir(directory):
                                os.makedirs(directory)
                            br.retrieve(link.url, directory
                                    + link.text[link.text.index(']')
                                    + 1:] + url_text)
                            downloadlinks.append(link.url)
                else:
                    if not os.path.exists(directory + link.text + url_text):
                        if not link.url in downloadlinks:
                            t.log('Downloading ' + link.text
                                  + url_text + ' to ' + directory)
                            if not os.path.isdir(directory):
                                os.makedirs(directory)
                            br.retrieve(link.url, directory + link.text + url_text)
                            downloadlinks.append(link.url)
            else:
                #Retrieve from folders
                if br.geturl().startswith('http://moodle.iitb.ac.in/mod/folder'
                        ) and link.url not in downloaded \
                    and link.text.startswith('[IMG]'):
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
                    self.retrieve(link.url, directory)

            br.back()
            self.pack()

    #On click of DLD Files button
    def dld(self):
        global t
        t.log('Downloading files, Please do not close until complete!')
        self.sync.config(state='disabled')
        self.pref.config(state='disabled')
        self.logout.config(state='disabled')
        urls = []
        directories = []
        if os.path.exists('Preferences.txt'):
            file_pref = open('Preferences.txt', 'r')
            lines = file_pref.readlines()
            n = len(lines) / 5
            if len(lines):
                for number in range(n):
                    urls.append((lines[5 * number + 2])[:lines[5 * number + 2].index('\n')])
                    directories.append((lines[5 * number + 3])[:lines[5 * number + 3].index('\n')])
                    nfurls.append((lines[5*number+4])[:lines[5*number+4].index("\n")])
                    if (lines[5 * number])[:lines[5 * number].index('\n')] == '1':
                        t.log('Retrieving from ' + (lines[5 * number+ 1])
                            [:lines[5 * number + 1].index('\n')] + ' at ' + directories[number])
                        self.retrieve(urls[number], directories[number])
            t.log('Successfully synced with Moodle!')
            self.sync.config(state='normal')
            self.pref.config(state='normal')
            self.logout.config(state='normal')
        else:
            t.log('Please set Preferences first!')
            self.sync.config(state='normal')
            self.pref.config(state='normal')
            self.logout.config(state='normal')
            self.destroy()
            self.newWindow = Home(self.master)

    def pref(self):
        t.log("Populating list of courses. This may take a while. Please be patient..")
        m.update()
        self.destroy()
        self.newWindow = Home(self.master)

    def logout(self):
        text_file = open('Cred.txt', 'w')
        text_file.write('0\n')
        text_file.close()
        t.log('Logout successful!')
        br.close()
        self.destroy()
        self.newWindow = LoginFrame(self.master)


class Home(Frame):

    def sall(self):
        n = len(course)
        for i in range(0, n):
            courseboxes[i].checkbox.select()

    def dall(self):
        n = len(course)
        for i in range(0, n):
            courseboxes[i].checkbox.deselect()

    def save(self):
        open('Preferences.txt', 'w').close()
        preferences = open('Preferences.txt', 'w')
        for i in range(0, len(online_courses)):
            x = str(courseboxes[i].directory.get())
            if not x.endswith('/'):
                courseboxes[i].directory.set(x + '/')
            preferences.write(str(courseboxes[i].var.get()) + '\n')
            preferences.write(online_courses[i].name + '\n')
            preferences.write(online_courses[i].mainlink + '\n')
            preferences.write(courseboxes[i].directory.get() + '\n')
            preferences.write(online_courses[i].nflink + '\n')
            courseboxes[i].pack_forget()

        preferences.close()
        self.frame.destroy()
        self.newWindow = Sync(m)

        creds = open('Cred.txt', 'r')
        lines = creds.readlines()
        creds.close()
        creds = open('Cred.txt', 'w')
        lines[3] = self.root_dir_box.directory.get() + '\n'
        creds.writelines(lines)
        creds.close()

    def load_online_courses(self):
        br.open('http://moodle.iitb.ac.in/')

        for link in br.links(url_regex='http://moodle.iitb.ac.in/course/view.php'):
            online_courses.append(savedata(link.url, link.text))

    def update_from_preferences(self, n):

        if os.path.exists('Preferences.txt'):
            file_pref = open('Preferences.txt', 'r')
            lines = file_pref.readlines()
            TotalInPreferences = len(lines) / 5
            if len(lines):
                for number in range(0, TotalInPreferences):
                    for i in range (0, n):
                        if online_courses[i].mainlink in lines[5 * number + 2]:
                            print "Found match for " + online_courses[i].name
                            online_courses[i].directory = lines[5 * number + 3][:lines[5 * number + 3].index('\n')]
                            online_courses[i].chkbox = lines[5 * number][:lines[5 * number].index('\n')]
                            online_courses[i].nflink = lines[5 * number + 4][:lines[5 * number + 4].index('\n')]
                            break
                        else:
                            print lines[5 * number + 2]
                            print online_courses[i].mainlink

        for i in range(0, n):
            if online_courses[i].nflink is "":
                print "Finding news forum link for " + online_courses[i].name
                online_courses[i].get_nf_link()    

    def __init__(self, master):

        global myname
        del courseboxes[:]
        del online_courses[:]

        self.load_online_courses()

        global TotalInMoodle
        TotalInMoodle = len(online_courses)
        n = len(online_courses)

        self.update_from_preferences(n)

        self.frame = VerticalScrolledFrame(m)
        self.frame.pack(fill=BOTH, expand=YES)
        self.root_dir_box = box(self.frame)

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

        self.f = Frame(self.frame.interior, height=20)
        self.f.grid(row=2, columnspan=3, sticky="we")
        


class box(Frame):

    def getdir(self):
        directory = tkFileDialog.askdirectory(parent=m, initialdir='C:/'
                , title='Please select a directory')
        if len(directory) > 0:
            self.directory.set(directory)

    def rootgetdir(self):
        directory = tkFileDialog.askdirectory(parent=m, initialdir='C:/'
                , title='Please select a directory')
        if len(directory) > 0:
            self.directory.set(directory)
            for i in range(len(courseboxes)):
                courseboxes[i].directory.set(directory +'/' + coursename[i][:6])
        else:
            self.directory.set('C:/')

    def __init__(self, master, number=None):
        Frame.__init__(self)
        self.var = IntVar()
        if number is not None:
            self.directory = StringVar()
            self.checkbox = Checkbutton(master.interior,
                                        text=online_courses[number].name, width=60,
                                        variable=self.var)
            self.checkbox.grid(row=number + 3, column=0)
            self.browse = Button(master.interior, text='Browse',
                                 command=self.getdir)
            self.browse.grid(row=number + 3, column=1)

            if online_courses[number].chkbox == '1':
                self.checkbox.select()
            self.directory.set(online_courses[number].directory)
            self.label_dir = Label(master.interior,
                                   textvariable=self.directory)
            self.label_dir.grid(row=number + 3, column=2)

        else:
            self.directory = StringVar()
            self.label = Label(master.interior,
                            text='Root Directory', width=60)
            self.label.grid(row=1, column=0)
            self.browse = Button(master.interior, text='Browse',
                                 command=self.rootgetdir)
            self.browse.grid(row=1, column=1)

            if os.path.exists('Cred.txt'):
                file_pref = open('Cred.txt', 'r')
                lines = file_pref.readlines()
                if len(lines) > 3:
                    self.directory.set(lines[3].replace('\n',''))
                else:
                    self.directory.set('C:/')
            else:
                self.directory.set('C:/')

            self.label_dir = Label(master.interior, textvariable=self.directory)
            self.label_dir.grid(row=1, column=2)


m = Tkinter.Tk()
t = TraceConsole()
m.wm_title('MooDLD')
try:
    m.iconbitmap('moodle.ico')
except:
    t.log("Icon Not Found. Keep `moodle.ico` in same directory!")
l = LoginFrame(m)
m.mainloop()
