import RPi.GPIO as GPIO
from time import sleep

# Motor setup
DIR1 = 21       # Motor 1 controls head rotation
STEP1 = 20
DIR2 = 17       # Motor 2 controls antenna flexion
STEP2 = 27
CW = 1
CCW = 0
SPR = 200 #Steps per full rotation
# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)

# Initiate microstepping
MODE1 = (25,24,23)
GPIO.setup(MODE1, GPIO.OUT)
MODE2 = (26,19,13)
GPIO.setup(MODE2, GPIO.OUT)
RESOLUTION = {'Full':(0,0,0),
              'Half': (1,0,0),
              '1/4': (0,1,0),
              '1/8': (1,1,0),
              '1/16': (1,1,1)}
GPIO.output(MODE1, RESOLUTION['1/16'])
GPIO.output(MODE2, RESOLUTION['1/16'])

# LCD Face setup
FACE = (12, 16, 6, 5)
GPIO.setup(FACE, GPIO.OUT)
#Make emotions dictionary 
EMOTION = {'neutral':(1,0,0,0),
           'happy': (0,1,0,0),
           'sad': (0,0,1,0),
           'questioning': (0,0,0,1)}



# ************** Robot Commands *************** #

def display_emot(input_emot):
    "Takes input emotion and displays in onto LCD screen"
    GPIO.output(FACE, EMOTION[input_emot])

def turn(rot_dir):
    "Turns to face the adjacent student on the right"
    
    stepcount = int(SPR*2.5)
    delay = 0.005/7
    GPIO.output(DIR1, rot_dir)
    for x in range(stepcount):
        GPIO.output(STEP1, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP1, GPIO.LOW)
        sleep(delay)
    sleep(.5)



