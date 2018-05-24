import os
from Tkinter import *

root = Tk()

def callback(event):
    frame.focus_set()
    print "clicked at", event.x, event.y

def q(event):
    print "pressed q"
    os.system('mpg123 -q A.mp3 &')

def w(event):
    print "YOU PRESSED w"
    os.system('mpg123 -q B.mp3 &')

frame = Frame(root, width=100, height=100)
frame.bind("q", q)
frame.bind("w", w)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()
