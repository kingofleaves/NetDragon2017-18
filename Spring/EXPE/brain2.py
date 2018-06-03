### Python 2 or 3 ###
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
        # self.new_image = None
        # self.old_label = None

        ### generate the window and frames ###
        # fullscreen window #
        parent.geometry("1920x1080")
        parent.title("TEAMO")

        # topmost frame #
        self.container = tk.Frame(self.parent)
        self.container.pack(expand="yes", fill="both")

        # # frame for mission #
        # self.mission_frame = tk.Frame(self.container, height=1080, width=1200, background="black")
        # self.mission_frame.pack(side="left", expand=0, fill="y")
        # self.change_image(self.mission_frame, "images/splash.png")

        # frame for TEAMO #
        self.teamo_frame = tk.Frame(self.container, height=405, width=720, background="black")
        self.teamo_frame.pack(side="right", expand=0, fill="none", anchor="s")
        self.change_image(self.teamo_frame, "images/teamo.png")

        ### keyboard bindings ###
        # self.parent.bind_all("<F1>", lambda event, frame=self.mission_frame, image="images/mission1.png" : self.change_image(frame, image))
        # self.parent.bind_all("<F2>", lambda event, frame=self.mission_frame, image="images/mission2.png" : self.change_image(frame, image))
        # self.parent.bind_all("<F3>", lambda event, frame=self.mission_frame, image="images/mission3.png" : self.change_image(frame, image))
        # self.parent.bind_all("<F4>", lambda event, frame=self.mission_frame, image="images/mission4.png" : self.change_image(frame, image))
        # self.parent.bind_all("<F5>", lambda event, frame=self.mission_frame, image="images/mission5.png" : self.change_image(frame, image))
        self.parent.bind_all("1", lambda event, frame=self.teamo_frame, image="images/teamo.png" : self.change_image(frame, image))
        self.parent.bind_all("2", lambda event, frame=self.teamo_frame, image="images/teamo-hint.png" : self.change_image(frame, image))
        self.parent.bind_all("<Escape>", self.exit)

    ### exits the GUI ###
    def exit(self, event):
        self.parent.destroy()

    ### changes the image displayed to the supplied filepath ###
    def change_image(self, frame, image):
        # self.old_label = self.new_label
        if frame not in self.images:
            self.images[frame] = []
            self.labels[frame] = []
        new_image = Image.open(image)
        self.images[frame].append(ImageTk.PhotoImage(new_image))
        self.labels[frame].append(tk.Label(frame, image=self.images[frame][-1]))
        self.labels[frame][-1].pack()
        if len(self.labels[frame]) > 1:
            self.labels[frame][-2].destroy()
        print(str(frame) + " current image is " + image)

root = tk.Tk()
brain = BrainControl(root)
root.mainloop()