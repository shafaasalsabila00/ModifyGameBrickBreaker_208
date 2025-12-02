import tkinter as tk

class Brick:
    COLORS = {1: 'blue', 2: 'green', 3: 'red'}

    def __init__(self, canvas, x, y, hits):
        self.canvas = canvas
        self.hits = hits
        color = self.COLORS[hits]

        self.item = canvas.create_rectangle(
            x-35, y-10, x+35, y+10,
            fill=color,
            tags='brick'   # ← INI PENTING BANGET
        )

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.canvas.delete(self.item)
        else:
            self.canvas.itemconfig(self.item, fill=self.COLORS[self.hits])

    def get_id(self):
        return self.item

