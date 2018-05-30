import os, sys
import Tkinter as tk

root = tk.Tk()

A_POSITION = -90
B_POSITION = -45
C_POSITION = 45
D_POSITION = 90

curr_position = 0

def ask_A(event):
    print("pressed 1, asking A")
    os.system('mpg123 -q A.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_B(event):
    print("pressed 2, asking B")
    os.system('mpg123 -q B.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_C(event):
    print("pressed 3, asking C")
    os.system('mpg123 -q C.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_D(event):
    print("pressed 4, asking D")
    os.system('mpg123 -q D.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def correct(event):
    print "pressed q, correct"
    os.system('mpg123 -q thats_great.mp3 &')

def incorrect(event):
    print("pressed w, incorrect")
    os.system('mpg123 -q thats_not_right.mp3 &')

def exit(event):
    sys.exit()

os.system('mpg123 -q hello.mp3 &')

frame = tk.Frame(root, width = 1920, height = 1080)
frame.bind("1", ask_A)
frame.bind("2", ask_B)
frame.bind("3", ask_C)
frame.bind("4", ask_D)
frame.bind("q", correct)
frame.bind("w", incorrect)
frame.bind("x", exit)
frame.focus_set()
frame.pack()
label = tk.Label(frame, pady = 400, font = ("Courier", 50), text = "Welcome to ME310 Hardware Bazaar!").pack()
frame.pack_propagate(False)

root.mainloop()
