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

class BrainControl:
    def __init__(self, parent):
        ### class variables ###
        self.parent = parent
        self.mission = None
        self.hint = None
        self.images = {}
        self.labels = {}

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
        self.parent.bind_all("<F1>", lambda event, frame=self.mission_frame, image="images/mission1.png", mission=1 : self.change_image(frame, image, mission))
        self.parent.bind_all("<F2>", lambda event, frame=self.mission_frame, image="images/mission2.png", mission=2 : self.change_image(frame, image, mission))
        self.parent.bind_all("<F3>", lambda event, frame=self.mission_frame, image="images/mission3.png", mission=3 : self.change_image(frame, image, mission))
        self.parent.bind_all("<F4>", lambda event, frame=self.mission_frame, image="images/mission4.png", mission=4 : self.change_image(frame, image, mission))
        self.parent.bind_all("<F5>", lambda event, frame=self.mission_frame, image="images/mission5.png", mission=5 : self.change_image(frame, image, mission))
        self.parent.bind_all("`", lambda event, new_hint_level=None : self.change_hint(new_hint_level))
        self.parent.bind_all("1", lambda event, new_hint_level=1 : self.change_hint(new_hint_level))
        self.parent.bind_all("2", lambda event, new_hint_level=2 : self.change_hint(new_hint_level))
        self.parent.bind_all("<Escape>", self.exit)

    ### exits the GUI ###
    def exit(self, event):
        self.parent.destroy()

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
            self.change_image(self.teamo_frame, "images/teamo-hint.png", None)
            self.change_image(self.hint_frame, "images/hint-" + str(self.mission) + "-" + str(new_hint_level) + ".png", None)
        self.hint = new_hint_level

root = tk.Tk()
root.attributes("-fullscreen", True)
brain = BrainControl(root)
root.mainloop()