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
        self.new_label = tk.Label(self.parent, image=self.image)
        self.old_label = None

        ### generate the window ###
        parent.geometry("1920x1080")
        parent.title("TEAMO")

        ### Frame and keyboard bindings ###
        self.container = tk.Frame(parent)
        self.container.bind("1", lambda event, image="images/mission1.png" : self.change_image(event, image))
        self.container.bind("2", lambda event, image="images/mission2.png" : self.change_image(event, image))
        self.container.bind("3", lambda event, image="images/mission3.png" : self.change_image(event, image))
        self.container.bind("4", lambda event, image="images/mission4.png" : self.change_image(event, image))
        self.container.bind("5", lambda event, image="images/mission5.png" : self.change_image(event, image))
        self.container.bind("<Escape>", self.exit)
        self.container.focus_set()
        self.container.pack()

    def exit(self, event):
        self.parent.destroy()

    def change_image(self, event, image):
        self.old_label = self.new_label
        new_image = Image.open(image)
        self.image = ImageTk.PhotoImage(new_image)
        self.new_label = tk.Label(self.parent, image=self.image)
        self.new_label.place(x=0, y=0)
        if self.old_label:
            self.old_label.destroy()
        print("Current image is " + image)

root = tk.Tk()
brain = BrainControl(root)
root.mainloop()