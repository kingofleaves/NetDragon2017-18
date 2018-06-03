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
        self.image = None

        ### generate the window and frames ###
        # fullscreen window #
        parent.geometry("1920x1080")
        parent.title("TEAMO")

        # topmost frame #
        self.container = tk.Frame(self.parent)
        self.container.pack(expand=tk.YES, fill=tk.BOTH)

        # frame for mission #
        self.mission_frame = tk.Frame(self.container, width=768)
        self.mission_frame.pack(side=tk.LEFT, expand=0, fill=tk.Y)
        self.new_label = tk.Label(self.mission_frame, image=self.image)
        self.old_label = None
        self.change_image("images/splash.png")

        ### keyboard bindings ###
        self.parent.bind_all("<F1>", lambda event, image="images/mission1.png" : self.change_image(image))
        self.parent.bind_all("<F2>", lambda event, image="images/mission2.png" : self.change_image(image))
        self.parent.bind_all("<F3>", lambda event, image="images/mission3.png" : self.change_image(image))
        self.parent.bind_all("<F4>", lambda event, image="images/mission4.png" : self.change_image(image))
        self.parent.bind_all("<F5>", lambda event, image="images/mission5.png" : self.change_image(image))
        self.parent.bind_all("<Escape>", self.exit)

    ### exits the GUI ###
    def exit(self, event):
        self.parent.destroy()

    ### changes the image displayed to the supplied filepath (use 1920x1080 images) ###
    def change_image(self, image):
        self.old_label = self.new_label
        new_image = Image.open(image)
        self.image = ImageTk.PhotoImage(new_image)
        self.new_label = tk.Label(self.mission_frame, image=self.image)
        self.new_label.pack()
        if self.old_label:
            self.old_label.destroy()
        print("Current image is " + image)

root = tk.Tk()
brain = BrainControl(root)
root.mainloop()