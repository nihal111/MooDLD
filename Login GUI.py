from Tkinter import *
import tkMessageBox as tm
import mechanize
import time

start_time = time.time()
moodle = 'http://moodle.iitb.ac.in/login/index.php'
br = mechanize.Browser()
print "Opening Moodle!"
br.open(moodle)
text_file = open("Cred.txt", "w")
root = Tk()
course = []
coursename = []
courses=[]


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
            text_file.write(self.entry_1.get()+'\n')
            text_file.write(self.entry_2.get()+'\n')
            text_file.close()
        
        
        br.select_form( nr=0 )
        br['username']= self.entry_1.get()
        br['password']= self.entry_2.get()
       
        br.submit()

        if ((br.geturl()) == "http://moodle.iitb.ac.in/"):
            tm.showinfo("Login info", "Welcome!")
            for link in br.links(url_regex='http://moodle.iitb.ac.in/user/profile.php'):
                self.profile = link.url
            self.new_window()
                        
        else:
            tm.showerror("Login error", "Incorrect username or password")
            self.new_window()
            
    def new_window(self):
        self.destroy()
        br.open (self.profile)
        self.newWindow = Home(self.master)
        

class Home(Frame):
    def __init__(self, master):
        Frame.__init__(self)
        self.Name = 'Welcome '+br.title()[:(br.title()).index(":")]
        self.label_1 = Label(self, text=self.Name, justify=LEFT)
        br.open('http://moodle.iitb.ac.in/')
        for link in br.links(url_regex='http://moodle.iitb.ac.in/course/view.php'):
                course.append(link)
                coursename.append(link.text)
        print coursename
        n= len(course)                
        self.label_1.grid(row=0, sticky=W)
        self.pack()
        for i in range (0,n):
            courses.append(box(root,i))

            
        
class box(Frame):
    def __init__(self, master, number):
        Frame.__init__(self)
        self.var = IntVar()
        self.checkbox = Checkbutton(self, text=coursename[number], variable= self.var)
        self.checkbox.grid(row=1,sticky = W)
        self.pack(fill =X)



root.wm_title("MooDLD")
root.iconbitmap('favicon.png')

lf = LoginFrame(root)
root.mainloop()
