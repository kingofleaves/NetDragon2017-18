import RPi.GPIO as GPIO
from time import sleep
import serial
import sys

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
           'confused': (0,0,1,0),
           'curious': (0,0,0,1)}

# Antenna Speed Tuning
ANT_SPEED = {'fast':100,'slow':10,'med':25}



# ************** Robot Movement Commands *************** #

def display_emot(input_emot):
    "Takes input emotion and displays in onto LCD screen"
    GPIO.output(FACE, EMOTION[input_emot])

def turn(rot_dir):
    "Turns to face the adjacent student on the right"
    
    stepcount = int(SPR*2)
    delay = 0.005/6
    GPIO.output(DIR1, rot_dir)
    for x in range(stepcount):
        GPIO.output(STEP1, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP1, GPIO.LOW)
        sleep(delay)
    sleep(.5)

def flex(rot_dir, speed):
    "Turns to face the adjacent student on the right"
    
    stepcount = int(SPR*6)
    delay = 0.005/(ANT_SPEED[speed])
    GPIO.output(DIR2, rot_dir)
    for x in range(stepcount):
        GPIO.output(STEP2, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP2, GPIO.LOW)
        sleep(delay)

def fullFlex(speed, rot_num):
    "Turns to face the adjacent student on the right"
    stepcount = int(SPR*6)
    delay = 0.005/(ANT_SPEED[speed])
    for i in range(0, rot_num):
        GPIO.output(DIR2, 1)
        for x in range(stepcount):
            GPIO.output(STEP2, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP2, GPIO.LOW)
            sleep(delay)
        GPIO.output(DIR2, 0)
        for x in range(stepcount):
            GPIO.output(STEP2, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP2, GPIO.LOW)
            sleep(delay)

def LED(mode):
    # LED Light set-up
    #'1' = breathing
    #'2' = single light sweep
    #'3' = light relay
    #'0' = off/sleep
    if len(sys.argv) == 2:
        ser = serial.Serial(sys.argv[1])
        ser.write(mode)
        


# ************** Robot Interaction Commands *************** #

def askRequest():
    display_emot('curious')
    fullFlex('slow')
    
def listen():
    display_emot('curious')

def processing():
    display_emot('neutral')
    

def acknowledge():
    display_emot('happy')
    fullFlex('med', 2)

def huh():
    display_emot('confused')
    fullFlex('slow', 3)
    LED(1)

def call():
    display_emot('curious')
    fullFlex('fast', 3)
    ## color: orange, flash 3 times, pause, flash again 3 times
    



turn(1)
turn(0)

##turn(1)
##turn(0)
##turn(0)
##turn(1)
##display_emot('happy')
##flex(1,'fast')
##flex(0,'fast')
##flex(1,'fast')
##flex(0,'fast')
##flex(1,'fast')
##flex(0,'fast')
##display_emot('neutral')
##
##display_emot('happy')
##flex(1,'fast')
##flex(0,'fast')
##flex(1,'fast')
##flex(0,'fast')
##flex(1,'fast')
##flex(0,'fast')
##display_emot('questioning')
##flex(1,'med')
##flex(0,'med')
##flex(1,'med')
##flex(0,'med')
##flex(1,'med')
##flex(0,'med')
##display_emot('sad')
##flex(1,'slow')
##flex(0,'slow')
##flex(1,'slow')
##flex(0,'slow')
##flex(1,'slow')
##flex(0,'slow')
##display_emot('neutral')
