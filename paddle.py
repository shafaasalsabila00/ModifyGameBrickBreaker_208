import tkinter as tk

class Paddle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.width = 80
        self.height = 10
        self.ball = None

        self.item = canvas.create_rectangle(
            x - self.width/2, y - self.height/2,
            x + self.width/2, y + self.height/2,
            fill="blue"
        )

    def move(self, offset):
        coords = self.canvas.coords(self.item)
        left, top, right, bottom = coords

        if left + offset >= 0 and right + offset <= int(self.canvas['width']):
            self.canvas.move(self.item, offset, 0)
            if self.ball is not None:
                self.ball.update_position()

    def set_ball(self, ball):
        self.ball = ball

    def get_position(self):
        return self.canvas.coords(self.item)
