import logging
import Tkinter as Tkinter

class TraceConsole():

    def __init__(self):
        # Init the main GUI window
        self._logFrame = Tkinter.Frame()
        self._log      = Tkinter.Text(self._logFrame, wrap=Tkinter.NONE, setgrid=True)
        self._scrollb  = Tkinter.Scrollbar(self._logFrame, orient=Tkinter.VERTICAL)
        self._scrollb.config(command = self._log.yview) 
        self._log.config(yscrollcommand = self._scrollb.set)
        # Grid & Pack
        self._log.grid(column=0, row=0)
        self._scrollb.grid(column=1, row=0, sticky=Tkinter.S+Tkinter.N)
        self._logFrame.pack()


    def log(self, msg, level=None):
        # Write on GUI
        self._log.insert('end', msg + '\n')

    def exitWindow(self):
        # Exit the GUI window and close log file
        print('exit..')

m = Tkinter.Tk()
t = TraceConsole()
t.log('hello world!')
m.mainloop()
