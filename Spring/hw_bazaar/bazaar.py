import os, sys
from Tkinter import *

root = Tk()

def ask_A(event):
    print "pressed 1, asking A"
    # turn to A
    # question face
    os.system('mpg123 -q A.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_B(event):
    print "pressed 2, asking B"
    # turn to B
    # question face
    os.system('mpg123 -q B.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_C(event):
    print "pressed 3, asking C"
    # turn to C
    # question face
    os.system('mpg123 -q C.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_D(event):
    print "pressed 4, asking D"
    # turn to D
    # question face
    os.system('mpg123 -q D.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def correct(event):
    print "pressed q, correct"
    # happy face
    os.system('mpg123 -q thats_great.mp3 &')

def incorrect(event):
    print "pressed w, incorrect"
    # sad face
    os.system('mpg123 -q thats_not_right.mp3 &')

def exit(event):
    sys.exit()

os.system('mpg123 -q hello.mp3 &')

frame = Frame(root, width=1920, height=1080)
frame.bind("1", ask_A)
frame.bind("2", ask_B)
frame.bind("3", ask_C)
frame.bind("4", ask_D)
frame.bind("q", correct)
frame.bind("w", incorrect)
frame.bind("x", exit)
frame.focus_set()
frame.pack()

root.mainloop()
