import os, sys
from Tkinter import *
import robot_control as rc

root = Tk()

A_POSITION = -90
B_POSITION = -45
C_POSITION = 45
D_POSITION = 90

curr_position = 0

def ask_A(event):
    print("pressed 1, asking A")
    # while curr_position > A_POSITION:
    #     turn_left()
    rc.display_emot('questioning')
    os.system('mpg123 -q A.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')
    

def ask_B(event):
    print("pressed 2, asking B")
    # turn to B
    rc.display_emot('questioning')
    os.system('mpg123 -q B.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_C(event):
    print("pressed 3, asking C")
    # turn to C
    rc.display_emot('questioning')
    os.system('mpg123 -q C.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def ask_D(event):
    print("pressed 4, asking D")
    # while curr_positon < D_POSITION:
    #     turn_right()
    rc.display_emot('questioning')
    os.system('mpg123 -q D.mp3')
    os.system('mpg123 -q can_you_answer.mp3 &')

def correct(event):
    print "pressed q, correct"
    rc.display_emot('happy')
    os.system('mpg123 -q thats_great.mp3 &')

def incorrect(event):
    print("pressed w, incorrect")
    rc.display_emot('sad')
    os.system('mpg123 -q thats_not_right.mp3 &')

def turn_left(event):
    print("pressed a, turn_left")
    rc.turn(0)
    # curr_position += 30 

def turn_right(event):
    print("pressed s, turn_right")
    rc.turn(1)
    # curr_position -= 30

def secret(event):
    os.system('mpg123 -q anaconda.mp3 &')

def exit(event):
    sys.exit()

os.system('mpg123 -q hello.mp3 &')
rc.display_emot('neutral')

frame = Frame(root, width = 1920, height = 1080)
frame.bind("1", ask_A)
frame.bind("2", ask_B)
frame.bind("3", ask_C)
frame.bind("4", ask_D)
frame.bind("q", correct)
frame.bind("w", incorrect)
frame.bind("a", turn_left)
frame.bind("s", turn_right)
frame.bind("x", exit)
frame.bind("m", secret)
frame.focus_set()
frame.pack()
label = Label(frame, pady = 400, font = ("Courier", 50), text = "Welcome to ME310 Hardware Bazaar!").pack()
frame.pack_propagate(False)

root.mainloop()
