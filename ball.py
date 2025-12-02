import tkinter as tk

class Ball:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.size = 15

        self.item = canvas.create_oval(
            x - self.size, y - self.size,
            x + self.size, y + self.size,
            fill="white"
        )

        # bola awalnya diam
        self.speed_x = 0
        self.speed_y = 0
        self.started = False

    def start(self, level):
        """Mulai game setelah tekan SPACE"""
        if not self.started:
            base_speed = 3 + (level - 1)  # makin tinggi level makin cepat
            self.speed_x = base_speed
            self.speed_y = -base_speed
            self.started = True

    def reset_position(self, x, y):
        """Untuk reset bola pas level naik"""
        self.canvas.coords(
            self.item,
            x - self.size, y - self.size,
            x + self.size, y + self.size
        )
        self.started = False
        self.speed_x = 0
        self.speed_y = 0

    def get_position(self):
        return self.canvas.coords(self.item)

    def update(self):
        if not self.started:
            return

        self.canvas.move(self.item, self.speed_x, self.speed_y)
        x1, y1, x2, y2 = self.get_position()

        # pantul kiri kanan
        if x1 <= 0 or x2 >= int(self.canvas['width']):
            self.speed_x *= -1

        # pantul atas
        if y1 <= 0:
            self.speed_y *= -1







