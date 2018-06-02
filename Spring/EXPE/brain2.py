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
        # self.new_label = tk.Label(self.parent, image=self.image)
        # self.old_label = None
        self.display = tk.Canvas(self.parent)
        self.display.create_image(0, 0, image=self.image, anchor=tk.NW, tags="IMG")
        self.display.grid(row=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.display.pack()

        ### generate the window ###
        parent.geometry("1920x1080")
        parent.title("TEAMO")

        ### Frame and keyboard bindings ###
        self.container = tk.Frame(parent)
        self.container.bind("<F1>", lambda event, image="images/mission1.png" : self.change_image(event, image))
        self.container.bind("<F2>", lambda event, image="images/mission2.png" : self.change_image(event, image))
        self.container.bind("<F3>", lambda event, image="images/mission3.png" : self.change_image(event, image))
        self.container.bind("<F4>", lambda event, image="images/mission4.png" : self.change_image(event, image))
        self.container.bind("<F5>", lambda event, image="images/mission5.png" : self.change_image(event, image))
        self.container.bind("<Escape>", self.exit)
        self.container.focus_set()
        self.container.pack()

    def exit(self, event):
        self.parent.destroy()

    def change_image(self, event, image):
        # self.old_label = self.new_label
        print event.width, event.height
        size = (event.width, event.height)
        new_image = Image.open(image)
        resized_image = new_image.resize(size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized_image)
        # self.new_label = tk.Label(self.parent, image=self.image)
        # self.new_label.place(x=0, y=0)
        # if self.old_label:
        #     self.old_label.destroy()
        if self.display.image:
            self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")


        print("Current image is " + image)

root = tk.Tk()
brain = BrainControl(root)
root.mainloop()