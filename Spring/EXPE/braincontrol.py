"""
braincontrol.py
Glenn M. Davis
June 2018

Controls the TEAMO robot for ME310 EXPE.
"""

### Python 2 or 3: for some reason, runs only in 3 on RPi and 2 on Mac OS ###
try:
    import Tkinter as tk
except:
    import tkinter as tk

from PIL import ImageTk, Image
import os
import random
import robot_control as rc
import serial
import time

ser = serial.Serial("/dev/ttyACM0")

class BrainControl:
    def __init__(self, parent):
        ### class variables ###
        self.parent = parent
        self.mission = None
        self.hint = None
        self.images = {}
        self.labels = {}
        self.current_pos = 0

        ### generate the window and frames ###
        # fullscreen window #
        parent.geometry("1920x1080")
        parent.title("TEAMO")
        parent.background="#dcdcdc"

        # topmost frame #
        self.container = tk.Frame(self.parent, borderwidth=0, highlightthickness=0)
        self.container.pack(expand=1, fill="both")
        self.left = tk.Frame(self.container, width=1200, height=1080, borderwidth=0, highlightthickness=0)
        self.left.pack(side="left", expand=0, fill="y")
        self.right = tk.Frame(self.container, width=720, height=1080, borderwidth=0, highlightthickness=0)
        self.right.pack(side="right", expand=0, fill="y")

        # frame for hint #
        self.hint_frame = tk.Frame(self.right, width=720, height=720, borderwidth=0, highlightthickness=0)
        self.hint_frame.pack(side="top", expand=0, fill="none")
        self.change_image(self.hint_frame, "images/hint-none.png", None)

        # frame for TEAMO #
        self.teamo_frame = tk.Frame(self.right, width=720, height=360, borderwidth=0, highlightthickness=0)
        self.teamo_frame.pack(side="bottom", expand=0, fill="none")
        self.change_image(self.teamo_frame, "images/teamo.png", None)

        # # frame for mission #
        self.mission_frame = tk.Frame(self.left, width=1200, height=1080, borderwidth=0, highlightthickness=0)
        self.mission_frame.pack(expand=0, fill="none")
        self.change_image(self.mission_frame, "images/splash.png", None)

        ### keyboard bindings ###
        # <ESC> to quit #
        self.parent.bind_all("<Escape>", self.exit)

        # <F1-5> for the different missions #
        self.parent.bind_all("<F1>", lambda event, mission=1 : self.introduce_mission(mission))
        self.parent.bind_all("<F2>", lambda event, mission=2 : self.introduce_mission(mission))
        self.parent.bind_all("<F3>", lambda event, mission=3 : self.introduce_mission(mission))
        self.parent.bind_all("<F4>", lambda event, mission=4 : self.introduce_mission(mission))
        self.parent.bind_all("<F5>", lambda event, mission=5 : self.introduce_mission(mission))

        # `-5 for the hints (0-5) #
        self.parent.bind_all("`", lambda event, new_hint_level=None : self.change_hint(new_hint_level))
        self.parent.bind_all("1", lambda event, new_hint_level=1 : self.change_hint(new_hint_level))
        self.parent.bind_all("2", lambda event, new_hint_level=2 : self.change_hint(new_hint_level))
        self.parent.bind_all("3", lambda event, new_hint_level=3 : self.change_hint(new_hint_level))
        self.parent.bind_all("4", lambda event, new_hint_level=4 : self.change_hint(new_hint_level))
        self.parent.bind_all("5", lambda event, new_hint_level=5 : self.change_hint(new_hint_level))

        # 6 for teacher alert #
        self.parent.bind_all("6", self.call_teacher_helper)
        self.parent.bind_all("7", self.teacher_alert_helper)

        # qwer turns to A, B, C, D and says name #
        self.parent.bind_all("q", lambda event, student="A" : self.look_student(student))
        self.parent.bind_all("w", lambda event, student="B" : self.look_student(student))
        self.parent.bind_all("e", lambda event, student="C" : self.look_student(student))
        self.parent.bind_all("r", lambda event, student="D" : self.look_student(student))

        # asdf says A, B, C, D name #
        self.parent.bind_all("a", lambda event, filename="A.mp3" : self.speak(filename))
        self.parent.bind_all("s", lambda event, filename="B.mp3" : self.speak(filename))
        self.parent.bind_all("d", lambda event, filename="C.mp3" : self.speak(filename))
        self.parent.bind_all("f", lambda event, filename="D.mp3" : self.speak(filename))

        # <Tab> turns to center #
        self.parent.bind_all("<Tab>", lambda event, student="center" : self.turn_to_student(student))

        # t/y turns left/right #
        self.parent.bind_all("t", self.turn_left_helper)
        self.parent.bind_all("y", self.turn_right_helper)

        # introductions, <F8> to start and then <F9-12> for each student #
        self.parent.bind_all("<F8>", self.intro_helper)
        self.parent.bind_all("<F9>", lambda event, student="A" : self.intro_student(student))
        self.parent.bind_all("<F10>", lambda event, student="B" : self.intro_student(student))
        self.parent.bind_all("<F11>", lambda event, student="C" : self.intro_student(student))
        self.parent.bind_all("<F12>", lambda event, student="D" : self.intro_student(student))

        ### randomized responses ###
        # , for (S ->) asking for help #
        self.parent.bind_all(",", lambda event, filename="sounds/ask-", emotion='confused', randomize_max_num=3 : self.speak_with_face(filename, emotion, randomize_max_num))

        # / for (S ->) "yes" #
        self.parent.bind_all("/", lambda event, filename="sounds/yes-", emotion='happy', randomize_max_num=7 : self.speak_with_face(filename, emotion, randomize_max_num))
        # . for (S ->) "no" #
        self.parent.bind_all(".", lambda event, filename="sounds/no-", emotion='neutral', randomize_max_num=3 : self.speak_with_face(filename, emotion, randomize_max_num))

        # l for S -> "great job" #
        self.parent.bind_all("l", lambda event, filename="sounds/great-", emotion='happy', randomize_max_num=3 : self.speak_with_face(filename, emotion, randomize_max_num))

        # ; for S -> "explain" -> S #
        self.parent.bind_all(";", lambda event, filename="sounds/explainto-", emotion='neutral', randomize_max_num=2 : self.speak_with_face(filename, emotion, randomize_max_num))

        # ' for S -> "ask" -> S
        self.parent.bind_all("'", lambda event, filename="sounds/askto-", emotion='neutral', randomize_max_num=2 : self.speak_with_face(filename, emotion, randomize_max_num))

        # ### testing robot ###
        # self.parent.bind_all("7", lambda event, emotion='neutral' : self.change_face(emotion))
        # self.parent.bind_all("8", lambda event, emotion='happy' : self.change_face(emotion))
        # self.parent.bind_all("9", lambda event, emotion='confused' : self.change_face(emotion))
        # self.parent.bind_all("0", lambda event, emotion='curious' : self.change_face(emotion))
        # self.parent.bind_all("j", lambda event, mode='1' : self.antenna_lights(mode))
        # self.parent.bind_all("k", lambda event, mode='2' : self.antenna_lights(mode))
        # self.parent.bind_all("l", lambda event, mode='3' : self.antenna_lights(mode))
        # self.parent.bind_all(";", lambda event, mode='0' : self.antenna_lights(mode))
        # self.parent.bind_all("o", lambda event, direction=1, speed='fast' : self.move_antenna(direction, speed))
        # self.parent.bind_all("p", lambda event, direction=0, speed='fast' : self.move_antenna(direction, speed))
        # self.parent.bind_all("[", lambda event, direction=1, speed='slow' : self.move_antenna(direction, speed))
        # self.parent.bind_all("]", lambda event, direction=0, speed='slow' : self.move_antenna(direction, speed))
        # self.parent.bind_all("'", lambda event, speed='med', times=3 : self.loop_antenna(speed, times))

########################## MOVIE CONTROLS (SPECIAL) ##########################
    #     self.parent.bind_all("<F9>", self.movie_received_mission)
    #     self.parent.bind_all("<F10>", self.movie_hint)
    #     self.parent.bind_all("<F11>", self.movie_teacher_alert)
    #     self.parent.bind_all("<F12>", self.movie_solution)

    # def movie_received_mission(self, event):
    #     self.change_image(self.mission_frame, "images/mission2.png", "movie")
    #     self.change_hint(0)
    #     self.speak("sounds/S3-1.mp3")

    # def movie_hint(self, event):
    #     self.mission = "movie"
    #     self.change_hint(1)
    #     self.speak("sounds/S4-1.mp3")

    # def movie_teacher_alert(self, event):
    #     self.mission = "movie"
    #     self.change_hint(2)
    #     self.speak("sounds/S6-2.mp3")

    # def movie_solution(self, event):
    #     self.mission = "movie"
    #     self.change_hint(3)
    #     self.speak("sounds/S7-1.mp3")
##############################################################################

    ############### KEYBOARD CONTROL FUNCTIONS ###############

    def introduce_mission(self, mission):
        self.change_image(self.mission_frame, "images/mission" + str(mission) + ".png", mission)
        self.speak_with_face("sounds/mission" + str(mission) + "-0.mp3", 'happy', None)
        self.speak_with_face("sounds/mission" + str(mission) + "-1.mp3", 'confused', None)

    ### looks at student X and says his/her name ###
    def look_student(self, student):
        self.turn_to_student(student)
        student_filename = student + '.mp3'
        self.speak(student_filename)

    ### changes the image displayed to the supplied filepath ###
    def change_image(self, frame, image, mission):
        if frame not in self.images:
            self.images[frame] = []
        if frame not in self.labels:
            self.labels[frame] = []
        if mission:
            self.mission = mission
        new_image = Image.open(image)
        self.images[frame].append(ImageTk.PhotoImage(new_image))
        self.labels[frame].append(tk.Label(frame, image=self.images[frame][-1], borderwidth=0, highlightthickness=0))
        if len(self.labels[frame]) > 1:
            self.labels[frame][-2].destroy()
        self.labels[frame][-1].pack()

    ### pass the current mission and new hint level, hint images formatted as "hint-MISSION-LEVEL.png" ###
    def change_hint(self, new_hint_level):
        if new_hint_level == None or self.mission == None:
            self.change_image(self.teamo_frame, "images/teamo.png", None)
            self.change_image(self.hint_frame, "images/hint-none.png", None)
        else:
            self.change_image(self.teamo_frame, "images/teamo-hint.png", self.mission)
            try:
                self.change_image(self.hint_frame, "images/hint-" + str(self.mission) + "-" + str(new_hint_level) + ".png", self.mission)
                if new_hint_level == 5:
                    self.speak_with_face("sounds/hint-" + str(self.mission) + "-" + str(new_hint_level) + ".mp3", 'happy', None)
                else:
                    self.speak_with_face("sounds/hint-" + str(self.mission) + "-" + str(new_hint_level) + ".mp3", 'neutral', None)
            except:
                self.change_hint(None)
                return
        self.hint = new_hint_level

    def call_teacher(self):
        self.speak_with_face("sounds/callteacher.mp3", 'confused', None)

    def teacher_alert(self):
        self.speak_with_face("sounds/teacheralert1.mp3", 'neutral', None)
        self.antenna_lights('2')
        self.loop_antenna('fast', 1)
        self.change_image(self.teamo_frame, "images/teamo.png", self.mission)
        self.change_image(self.hint_frame, "images/teacher-alert.png", self.mission)
        self.speak_with_face("sounds/teacheralert2.mp3", 'confused', None)

    def turn_to_student(self, student):
        positions = {}
        positions['A'] = -2
        positions['B'] = -1
        positions['C'] = 1
        positions['D'] = 2
        positions['center'] = 0
        to_change = self.current_pos - positions[student]
        while to_change > 0:
            self.turn_left()
            to_change = self.current_pos - positions[student]
        while to_change < 0:
            self.turn_right()
            to_change = self.current_pos - positions[student]

    def intro(self):
        self.antenna_lights('1')
        self.speak_with_face("sounds/intro.mp3", 'happy', None)
        self.loop_antenna('med', 2)

    def intro_student(self, student):
        self.turn_to_student(student)
        self.antenna_lights('3')
        self.loop_antenna('fast', 1)
        self.speak_with_face("sounds/intro", 'happy', 3)
        self.speak(student + ".mp3")
        self.antenna_lights('1')

    ############### SUBFUNCTIONS ###############

    # mode: '1' = breathing, '2' = single light sweep, '3' = light relay, '0' = off/sleep
    def antenna_lights(self, mode):
        ser.write(mode.encode())

    # direction: 1 = down, 0 = up
    # speed: 'high', 'med', 'low'
    def move_antenna(self, direction, speed):
        rc.flex(direction, speed)

    # speed: 'high', 'med', 'low'
    # number of times to repeat
    def loop_antenna(self, speed, times):
        rc.fullFlex(speed, times)

    # emotion: neutral, happy, confused, curious
    def change_face(self, emotion):
        rc.display_emot(emotion)
        if emotion == 'happy':
            self.antenna_lights('3')
            self.loop_antenna('fast', 1)
        elif emotion == 'confused':
            self.antenna_lights('1')
            self.move_antenna(1, 'slow')
            self.move_antenna(0, 'med')
        elif emotion == 'curious':
            self.antenna_lights('2')
            self.loop_antenna('med', 1)
        self.antenna_lights('1')

    def call_teacher_helper(self, event):
        self.call_teacher()

    def intro_helper(self, event):
        self.intro()

    def teacher_alert_helper(self, event):
        self.teacher_alert()

    def turn_right_helper(self, event):
        self.turn_right()

    def turn_left_helper(self, event):
        self.turn_left()

    def turn_right(self):
        rc.turn(1)
        self.current_pos = self.current_pos + 1

    def turn_left(self):
        rc.turn(0)
        self.current_pos = self.current_pos - 1

    def speak_randomizer(self, filename, max_num):
        num = random.randint(1, max_num)
        self.speak(filename + str(num) + ".mp3")

    def speak_with_face(self, filename, emotion, randomize_max_num):
        self.change_face(emotion)
        if randomize_max_num:
            self.speak_randomizer(filename, randomize_max_num)
        else:
            self.speak(filename)

    def speak(self, filename):
        os.system('mpg123 -q ' + filename)

    def exit(self, event):
        self.speak_with_face('sounds/goodbye.mp3', 'happy', None)
        self.antenna_lights('0')
        self.change_face('neutral')
        self.turn_to_student('center')
        self.parent.destroy()

root = tk.Tk()
root.attributes("-fullscreen", True)
brain = BrainControl(root)
root.mainloop()
