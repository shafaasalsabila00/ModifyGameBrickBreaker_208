import tkinter as tk
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.width = 500
        self.height = 400
        
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.running = True

        # paddle
        self.paddle = Paddle(self.canvas, self.width/2, self.height-30)

        # ball
        self.ball = Ball(self.canvas, self.paddle, [], "white")

        # brick list
        self.bricks = []
        self.create_bricks()

        root.bind("<Left>", lambda e: self.paddle.move(-20))
        root.bind("<Right>", lambda e: self.paddle.move(20))

        self.loop()

    def create_bricks(self):
        y = 50
        for row in range(3):
            x = 60
            for col in range(6):
                brick = Brick(self.canvas, x, y, 1)
                self.bricks.append(brick.get_id())
                x += 70
            y += 25

    def loop(self):
        status = self.ball.update()

        # collision
        pos = self.canvas.coords(self.ball.id)
        ball_items = self.canvas.find_overlapping(pos[0], pos[1], pos[2], pos[3])
        self.ball.collide(ball_items)

        if status == "lost_life":
            # reset posisi
            self.canvas.coords(self.ball.id,
                self.width/2, self.height/2,
                self.width/2 + self.ball.size, self.height/2 + self.ball.size)

        if self.running:
            self.after(16, self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Breakout Game")
    game = Game(root)
    game.pack()
    root.mainloop()
