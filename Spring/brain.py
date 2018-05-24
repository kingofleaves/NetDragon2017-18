'''
GROUPR: Controller
Glenn M. Davis (gmdavis1@gmail.com)
May 2018

Controls GROUPR's movements, face screen, and output (task) screen.
'''

# location (in degrees from -90 to 90, 0 = forward) of each seat
A_POSITION = -90
B_POSITION = -45
C_POSITION = 45
D_POSITION = 90

def bend_antenna(angle):
    pass

def change_antenna_light(light, status):
    pass

def rotate_head(direction):
    pass

# will the eyes keep playing after this function ends?
def change_eyes(image):
    pass

# don't clear the screen after, leave the last image up
def change_task_screen(image):
    pass

def speak(file):
    pass

# initialize task_screen to be a full-size window