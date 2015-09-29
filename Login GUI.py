from Tkinter import *
import tkMessageBox as tm
import mechanize
import time
import tkFileDialog
import os

start_time = time.time()
moodle = 'http://moodle.iitb.ac.in/login/index.php'
br = mechanize.Browser()
print "Opening Moodle!"
br.open(moodle)
text_file = open("Cred.txt", "w")
root = Tk()
course = []
coursename = []
save =[]
courses=[]
downloaded= []
myname = ""

class savedata():
    def __init__(self,url,directory,name):
        self.url = url
        self.directory = directory
        self.name = name
        
class LoginFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self)
        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")
        self.x= IntVar()
        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")
        self.var = IntVar()
        self.label_1.grid(row=0, sticky=W)
        self.label_2.grid(row=1, sticky=W)
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)
        
        self.checkbox = Checkbutton(self, text="Keep me logged in", variable= self.var)
        self.checkbox.grid(columnspan=2)
        
        self.logbtn = Button(self, text="Login", command = self._login_btn_clickked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clickked(self):
       
        print "Attempting login..."        
        br.open(moodle)
        
        if (self.var.get() ):
            text_file.write(str(self.var.get())+'\n')
            text_file.write(self.entry_1.get()+'\n')
            text_file.write(self.entry_2.get()+'\n')
        else:                       
            text_file.write(str(self.var.get())+'\n')
        text_file.close()        
        br.select_form( nr=0 )
        br['username']= '150040015' #self.entry_1.get()
        br['password']= 'npain!!!'  #self.entry_2.get()
       
        br.submit()

        if ((br.geturl()) == "http://moodle.iitb.ac.in/"):
            
            for link in br.links(url_regex='http://moodle.iitb.ac.in/user/profile.php'):
                self.profile = link.url
            br.open (self.profile)
            global myname
            myname = br.title()[:(br.title()).index(":")]
            tm.showinfo("Login info", "Welcome "+myname+"!" )
            self.new_window()
            print "Successful Login!"
                        
        else:
            tm.showerror("Login error", "Incorrect username or password")
            self.new_window()
            
    def new_window(self):
        self.destroy()
        self.newWindow = Sync(self.master)


class Sync(Frame):
    
    def retrieve(self, url, directory):
        self.links = []
        global downloaded
        br.open(url)
        for link in br.links(url_regex="."):
            if ((not (link.url.startswith('http://moodle.iitb.ac.in/login/logout.php'))) and (not (link.url).startswith(br.geturl())) and (not (link.url).startswith('#')) and link.url not in downloaded):
                self.links.append(link)

        for link in self.links:
            br.open(link.url)
            if ((br.geturl()).endswith('.pdf') or (br.geturl()).endswith('forcedownload=1')):
                
                if (']' in link.text):
                    if not os.path.exists(directory+link.text[(link.text).index("]")+1:]+'.pdf'):
                        print "Downloading " + link.text[(link.text).index("]")+1:]+'.pdf' + " to " + directory
                        br.retrieve(link.url,directory+link.text[(link.text).index("]")+1:]+'.pdf')
                                    
            else:
                if ((br.geturl()).startswith('http://moodle.iitb.ac.in/mod/folder') and (link.url not in downloaded) and (link.text).startswith('[IMG]')):
                    foldername = br.title()[(br.title()).index(":")+2:]
                    newpath = directory + foldername
                    if not os.path.exists(newpath): os.makedirs(newpath)
                    print  "Retrieving from "+ foldername + " at " + newpath 
                    downloaded.append(link.url)
                    self.retrieve(link.url, newpath+'/')
                    
                    
            br.back()


    def dld(self):
        urls =[]
        directories= []
        
        file_pref=open("Preferences.txt",'r')
        lines = file_pref.readlines()
        n= len(lines)/3
        if(len(lines)):

            for number in range (0,n):
               urls.append((lines[3*number+1])[:lines[3*number+1].index("\n")])
               directories.append((lines[3*number+2])[:lines[3*number+2].index("\n")])
               print  "Retrieving from "+ (lines[3*number])[:lines[3*number].index("\n")] + " at " + directories[number]
               self.retrieve(urls[number], directories[number])
        print "Moodle is up-to-date!"

        

    def pref(self):
        self.destroy()
        self.newWindow = Home(self.master)
    
    def __init__(self,master):
        Frame.__init__(self)
        self.Name = 'Welcome '+ str(myname)
        self.label_1 = Label(self, text=self.Name, justify=LEFT)
        self.label_1.grid(row=0)
        self.sync= Button(self, text="DLD Files",command= self.dld)
        self.sync.grid(row=1)
        self.pref=Button(self, text="Preferences", command = self.pref)
        self.pref.grid(row=2)
        self.pack()
        

class Home(Frame):
    def sall(self):
        n= len(course)
        for i in range (0,n):
            courses[i].checkbox.select()
            print courses[i].var.get()
    def dall(self):

        n= len(course)
        for i in range (0,n):
            courses[i].checkbox.deselect()
            print courses[i].var.get()

            
    def save(self):
        n= len(courses)
        open("Preferences.txt","w").close()
        preferences = open("Preferences.txt", "w")
        for i in range (0,n):
            x=str(courses[i].directory.get())
            if not(x.endswith("/")):
                courses[i].directory.set(x+'/')
            save.append(savedata(course[i].url,courses[i].directory.get(),coursename[i]))
            preferences.write(save[i].name+'\n')
            preferences.write(save[i].url+'\n')
            preferences.write(save[i].directory+'\n')
            courses[i].pack_forget()
        preferences.close()
        self.destroy()
        self.newWindow = Sync(self.master)


            
    def __init__(self, master):
        Frame.__init__(self)
        global myname
        self.Name = 'Welcome '+myname
        self.label_1 = Label(self, text=self.Name, justify=CENTER)
        del courses[:]
        del course[:]
        del coursename[:]
        del save[:]
        br.open('http://moodle.iitb.ac.in/')
        for link in br.links(url_regex='http://moodle.iitb.ac.in/course/view.php'):
                course.append(link)
                coursename.append(link.text)
        
        n= len(course)                
        self.label_1.grid(row=0, sticky=W)
        self.pack()
        for i in range (0,n):
            courses.append(box(root,i))
        self.selectall = Button(self, text="Select All", command= self.sall)     
        self.selectall.grid(row=1,column=0)
        self.deselectall = Button(self, text="Deselect All", command= self.dall)     
        self.deselectall.grid(row=1, column =1)
        self.save = Button(self, text="Save Settings", command= self.save)     
        self.save.grid(row=1,column=2,padx=60)
        self.pack(fill =X)
        

            
        
class box(Frame):
    def getdir(self):
        directory = tkFileDialog.askdirectory(parent=root,initialdir ="C:/", title='Please select a directory')
        if len(directory) >0:
            self.directory.set(directory)
        
        
    def __init__(self, master, number):
        Frame.__init__(self)
        self.var = IntVar()
        self.directory=StringVar()
        try:
            with open('Preferences.txt') as file:
                pass
            file_pref=open("Preferences.txt",'r')
            lines = file_pref.readlines()
            if(str(coursename[number]) in str(lines[3*number])):
                self.directory.set((lines[3*number+2])[:lines[3*number+2].index("\n")])
                
            else:
                self.directory.set("C:/")
        except IOError as e:
                                    
            self.directory.set("C:/")
        self.checkbox = Checkbutton(self, text=coursename[number],width= 40, variable= self.var)
        self.checkbox.grid(row=number+1,sticky=W,pady=5)
        self.browse = Button(self, text ="Browse", command= self.getdir)
        self.browse.grid(row=number+1,column =5, sticky = E,pady=5)
        self.label_dir = Label(self,textvariable=self.directory)
        self.label_dir.grid(row=number+1 , column=6,pady=5)
        
        
        self.pack(fill =X,anchor= "w")

root.wm_title("MooDLD")
root.iconbitmap('favicon.png')

lf = LoginFrame(root)
root.mainloop()
