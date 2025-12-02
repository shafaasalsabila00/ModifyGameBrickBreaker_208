class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3

        ### === MODIFIKASI: Tambah sistem level ===
        self.level = 1            # level awal
        self.max_level = 3        # total level

        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#D6D1F5',
                                width=self.width,
                                height=self.height,)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle

        self.hud = None

        ### === MODIFIKASI: Load brick berdasarkan level ===
        self.load_level()

        self.setup_game()

        self.canvas.focus_set()
        self.canvas.bind('<Left>',
                         lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',
                         lambda _: self.paddle.move(10))

    # ==========================================================
    #                 SISTEM LEVEL BARU (DITAMBAHKAN)
    # ==========================================================
    def load_level(self):
        ### === MODIFIKASI: hapus brick lama saat pindah level ===
        for item_id in list(self.items):
            if isinstance(self.items[item_id], Brick):
                self.canvas.delete(item_id)
                del self.items[item_id]

        ### === MODIFIKASI: Level 1 layout ===
        if self.level == 1:
            for x in range(5, self.width - 5, 75):
                self.add_brick(x + 37.5, 50, 3)
                self.add_brick(x + 37.5, 70, 2)
                self.add_brick(x + 37.5, 90, 1)

        ### === MODIFIKASI: Level 2 layout (lebih sulit) ===
        elif self.level == 2:
            for x in range(5, self.width - 5, 75):
                self.add_brick(x + 37.5, 40, 3)
                self.add_brick(x + 37.5, 60, 2)
                self.add_brick(x + 37.5, 80, 2)
                self.add_brick(x + 37.5, 100, 1)

        ### === MODIFIKASI: Level 3 layout (random hits) ===
        elif self.level == 3:
            import random
            for x in range(5, self.width - 5, 75):
                for y in (40, 60, 80, 100, 120):
                    hits = random.choice([1, 2, 3])
                    self.add_brick(x + 37.5, y, hits)

    # ==========================================================
    #                   FUNGSI GAME ASLI
    # ==========================================================
    def setup_game(self):
        self.add_ball()
        self.update_lives_text()

        ### === MODIFIKASI: tampilkan level di teks awal ===
        self.text = self.draw_text(300, 200,
                                   f'Level {self.level} - Press Space')
        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)

    def update_lives_text(self):
        ### === MODIFIKASI: HUD menampilkan Level ===
        text = f'Lives: {self.lives} | Level: {self.level}'

        if self.hud is None:
            self.hud = self.draw_text(80, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))

        ### === MODIFIKASI: Brick habis → naik level, bukan langsung win ===
        if num_bricks == 0:
            self.ball.speed = None

            if self.level < self.max_level:
                self.level += 1
                self.draw_text(300, 200, f'Level {self.level - 1} Complete!')

                ### === MODIFIKASI: delay lalu lanjut level ===
                self.after(1500, self.next_level)
            else:
                self.draw_text(300, 200, 'You Win! You Broke All Bricks!')
            return

        # bola jatuh
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'You Lose! Game Over!')
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    # ==========================================================
    #                 TRANSISI LEVEL BARU (DITAMBAHKAN)
    # ==========================================================
    def next_level(self):
        ### === MODIFIKASI: Reset canvas untuk level baru ===
        self.canvas.delete('all')
        self.canvas = tk.Canvas(self, bg='#D6D1F5',
                                width=self.width, height=self.height)
        self.canvas.pack()

        self.items = {}
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle

        ### === MODIFIKASI: Load layout level berikutnya ===
        self.load_level()

        self.setup_game()

        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)
