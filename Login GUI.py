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


class LoginFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self)
        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")
        self.x= IntVar()
        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")
        self.var = IntVar()
        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)
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
            
        else:
            tm.showerror("Login error", "Incorrect username or password")
            
            




root = Tk()
root.wm_title("Moodle Login")
root.geometry("250x100")
root.iconbitmap(r'D:\Python\favicon.png')
lf = LoginFrame(root)
root.mainloop()
