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
        self.hint_frame.pack(side="top", expand=0, fill="both")
        self.change_image(self.hint_frame, "images/hint1.png")

        # frame for TEAMO #
        self.teamo_frame = tk.Frame(self.right, width=720, height=360, borderwidth=0, highlightthickness=0)
        self.teamo_frame.pack(side="bottom", expand=0, fill="both")
        self.change_image(self.teamo_frame, "images/teamo.png")

        # # frame for mission #
        self.mission_frame = tk.Frame(self.left, width=1200, height=1080, borderwidth=0, highlightthickness=0)
        self.mission_frame.pack(expand=0, fill="both")
        self.change_image(self.mission_frame, "images/splash.png")

        ### keyboard bindings ###
        self.parent.bind_all("<F1>", lambda event, frame=self.mission_frame, image="images/mission1.png" : self.change_image(frame, image))
        self.parent.bind_all("<F2>", lambda event, frame=self.mission_frame, image="images/mission2.png" : self.change_image(frame, image))
        self.parent.bind_all("<F3>", lambda event, frame=self.mission_frame, image="images/mission3.png" : self.change_image(frame, image))
        self.parent.bind_all("<F4>", lambda event, frame=self.mission_frame, image="images/mission4.png" : self.change_image(frame, image))
        self.parent.bind_all("<F5>", lambda event, frame=self.mission_frame, image="images/mission5.png" : self.change_image(frame, image))
        self.parent.bind_all("1", lambda event, frame=self.teamo_frame, image="images/teamo.png" : self.change_image(frame, image))
        self.parent.bind_all("2", lambda event, frame=self.teamo_frame, image="images/teamo-hint.png" : self.change_image(frame, image))
        self.parent.bind_all("<Escape>", self.exit)

    ### exits the GUI ###
    def exit(self, event):
        self.parent.destroy()

    ### changes the image displayed to the supplied filepath ###
    def change_image(self, frame, image):
        if frame not in self.images:
            self.images[frame] = []
        if frame not in self.labels:
            self.labels[frame] = []
        new_image = Image.open(image)
        self.images[frame].append(ImageTk.PhotoImage(new_image))
        self.labels[frame].append(tk.Label(frame, image=self.images[frame][-1], borderwidth=0, highlightthickness=0))
        if len(self.labels[frame]) > 1:
            self.labels[frame][-2].destroy()
        self.labels[frame][-1].pack()

        print(str(frame) + " current image is " + image)

root = tk.Tk()
brain = BrainControl(root)
root.mainloop()