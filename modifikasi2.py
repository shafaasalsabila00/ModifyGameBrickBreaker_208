import tkinter as tk
from paddle import Paddle
from brick import Brick
from ball import Ball

class Game(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.width = 500
        self.height = 400

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # status game
        self.game_running = False
        self.level = 1

        # text overlay
        self.start_text = self.canvas.create_text(
            self.width/2, self.height/2,
            text="PRESS SPACE TO START",
            fill="white",
            font=("Arial", 18)
        )

        self.level_text = self.canvas.create_text(
            70, 20,
            text=f"LEVEL: {self.level}",
            fill="white",
            font=("Arial", 14)
        )

        # object
        self.paddle = Paddle(self.canvas, self.width/2, self.height-30)
        self.ball = Ball(self.canvas, self.width/2, self.height/2)

        self.bricks = []
        self.create_bricks()

        # kontrol
        root.bind("<Left>", lambda e: self.paddle.move(-20))
        root.bind("<Right>", lambda e: self.paddle.move(20))
        root.bind("<space>", self.start_game)

        self.update_game()

    # ---------------------------------------------------------

    def create_bricks(self):
        self.bricks.clear()
        y = 50
        for row in range(3 + self.level - 1):  # tiap level nambah 1 baris brick
            x = 60
            for col in range(6):
                brick = Brick(self.canvas, x, y, 1)
                self.bricks.append(brick)
                x += 70
            y += 25

    # ---------------------------------------------------------

    def start_game(self, event=None):
        if not self.game_running:
            self.game_running = True
            self.canvas.itemconfig(self.start_text, text="")  # hilangkan text mulai

    # ---------------------------------------------------------

    def game_over(self):
        self.game_running = False
        self.canvas.itemconfig(self.start_text, text="GAME OVER\nPRESS SPACE TO RESTART")
        self.reset_game()

    # ---------------------------------------------------------

    def next_level(self):
        self.level += 1
        self.canvas.itemconfig(self.level_text, text=f"LEVEL: {self.level}")
        self.game_running = False
        self.canvas.itemconfig(self.start_text, text=f"LEVEL {self.level}\nPRESS SPACE TO START")
        self.reset_game(new_level=True)

    # ---------------------------------------------------------

    def reset_game(self, new_level=False):
        self.ball.reset_position()
        self.paddle.reset_position()

        if new_level:
            self.create_bricks()
        else:
            # ulang level yang sama
            self.create_bricks()

    # ---------------------------------------------------------

    def check_collisions(self):
        bx1, by1, bx2, by2 = self.ball.get_position()
        items = self.canvas.find_overlapping(bx1, by1, bx2, by2)

        # brick collision
        for brick in self.bricks[:]:
            if brick.get_id() in items:
                brick.hit()
                self.bricks.remove(brick)
                self.ball.speed_y *= -1
                return

        # paddle collision
        if self.paddle.item in items:
            self.ball.speed_y = -abs(self.ball.speed_y)

    # ---------------------------------------------------------

    def update_game(self):
        if self.game_running:
            self.ball.update()
            self.check_collisions()

            # bola jatuh → game over
            if self.ball.y > self.height:
                self.game_over()

            # brick habis → next level
            if len(self.bricks) == 0:
                self.next_level()

        self.after(16, self.update_game)

# ---------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Breakout Modifikasi 2")
    game = Game(root)
    game.pack()
    root.mainloop()




