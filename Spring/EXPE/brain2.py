import Tkinter as tk

class BrainControl:
    def __init__(self, parent):
        parent.geometry("1920x1080")
        parent.title("TEAMO")
        self.parent = parent
        self.container = tk.Frame(parent)
        self.container.pack()

        self.mission = None # keep track of the mission
        self.image = None

        self.exit_button = tk.Button(self.container, text="Exit")
        self.exit_button.bind("<Button-1>", self.exit)
        self.exit_button.pack()

        self.image1_button = tk.Button(self.container, text="Image 1")
        self.image1_button.bind("<Button-1>", lambda event, image="images/mission1.png" : self.change_image(event, image))
        self.image1_button.pack()
        self.image2_button = tk.Button(self.container, text="Image 2")
        self.image2_button.bind("<Button-1>", lambda event, image="images/mission2.png" : self.change_image(event, image))
        self.image2_button.pack()

    def exit(self, event):
        self.parent.destroy()

    def change_image(self, event, image):
        self.image = image
        print("Current image is " + self.image)

root = tk.Tk()
brain = BrainControl(root)
root.mainloop()