import Tkinter as tk

class BrainControl:
    def __init__(self, parent):
        self.parent = parent
        self.container = tk.Frame(parent, width=640, height=480)
        self.container.pack()
        self.container.pack_propagate(False)

        self.mission = None

        self.exit_button = tk.Button(self.container, text="Exit")
        self.exit_button.bind("<Button-1>", self.exit)
        self.exit_button.pack()

    def exit(self, event):
        self.parent.destroy()

root = tk.Tk()
brain = BrainControl(root)
root.mainloop()