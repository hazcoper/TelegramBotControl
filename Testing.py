'''Called using the main program, it creater a window saying the computer has been lost os stolen'''
from tkinter import *
import tkinter.font as font


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master  # main frame

        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="THIS COMPUTER HAS BEEN LOST OR STOLEN, PLEASE CONTACT THE FOLLOWING NUMBER")
        quitButton['font'] = myFont
        quitButton.place(x=0, y=0)
        SecondButton = Button(self, text="969229936")
        SecondButton["font"] = myFont2
        SecondButton.place(x=0, y=60)


root = Tk()
myFont = font.Font(family='Helvetica', size=19, weight='bold')
myFont2 = font.Font(family='Helvetica', size=30, weight='bold')

root.geometry("1200x400")

app = Window(root)
root.mainloop()

