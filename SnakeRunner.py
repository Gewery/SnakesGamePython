from threading import Thread


class SnakeRunner(Thread):

    bot = None
    snake = None
    opponent = None
    maze_size = None
    apple = None
    chosen_direction = None

    def __init__(self, bot, snake, opponent, maze_size, apple):
        super().__init__()
        self.bot = bot
        self.snake = snake
        self.opponent = opponent
        self.maze_size = maze_size
        self.apple = apple

    def run(self):
        self.chosen_direction = self.bot.choose_direction(self.snake, self.opponent, self.maze_size, self.apple)