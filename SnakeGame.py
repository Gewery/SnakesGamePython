from ctypes import c_long
from ctypes import pythonapi
from random import randint

from Coordinate import Coordinate
from Snake import Snake
from SnakeRunner import SnakeRunner


class SnakeGame:
    TIMEOUT_THRESHOLD = 1000  # timeout threshold for taking a decision in millis

    snake0 = None
    snake1 = None
    bot0 = None
    bot1 = None
    maze_size = None
    apple_coordinate = None
    game_result = "0 - 0"
    apple_eaten0 = 0
    apple_eaten1 = 0
    snake_size = 0
    name0 = ""
    name1 = ""

    def __init__(self, maze_size, head0, tail_direction0, head1, tail_direction1, size, bot0, bot1):
        self.snake_size = size
        self.maze_size = maze_size
        self.snake0 = Snake(head0, tail_direction0, size, maze_size)
        self.snake1 = Snake(head1, tail_direction1, size, maze_size)
        self.bot0 = bot0
        self.bot1 = bot1

        self.apple_coordinate = self.random_non_occupied_cell()

    def random_non_occupied_cell(self):
        while True:
            c = Coordinate(randint(0, self.maze_size.x), randint(0, self.maze_size.y))
            if c in self.snake0.elements:
                continue
            if c in self.snake1.elements:
                continue

            return c

    def run(self, steps_allowed):
        while steps_allowed > 0 and self.run_one_step:
            steps_allowed -= 1

    @property
    def run_one_step(self):
        self.print_game()

        bot0_runner = SnakeRunner(self.bot0, self.snake0, self.snake1, self.maze_size, self.apple_coordinate)
        bot1_runner = SnakeRunner(self.bot1, self.snake1, self.snake0, self.maze_size, self.apple_coordinate)

        s0_timeout = False
        s1_timeout = False

        bot0_runner.start()
        bot0_runner.join(timeout=self.TIMEOUT_THRESHOLD)
        if bot0_runner.is_alive():
            pythonapi.PyThreadState_SetAsyncExc(c_long(bot0_runner))
            s0_timeout = True
            print("Bot " + self.bot0.name + " took too long to make a decision")

        bot1_runner.start()
        bot1_runner.join(timeout=self.TIMEOUT_THRESHOLD)
        if bot1_runner.is_alive():
            pythonapi.PyThreadState_SetAsyncExc(c_long(bot1_runner))
            s1_timeout = True
            print("Bot " + self.bot1.name + " took too long to make a decision")

        bot0_direction = bot0_runner.chosen_direction
        bot1_direction = bot1_runner.chosen_direction

        if s0_timeout or s1_timeout:
            self.game_result = ('0' if s0_timeout else '1') + " - " + ('0' if s1_timeout else '1')
            return False

        grow0 = self.snake0.get_head().move_to(bot1_direction) == self.apple_coordinate
        grow1 = self.snake1.get_head().move_to(bot1_direction) == self.apple_coordinate

        s0_dead = not self.snake0.move_to(bot0_direction, grow0)
        s1_dead = not self.snake1.move_to(bot1_direction, grow1)
        s0_dead |= self.snake0.head_collides_with(self.snake1)
        s1_dead |= self.snake1.head_collides_with(self.snake0)

        if grow0 or grow1 or self.apple_coordinate is None:
            self.apple_eaten0 = len(self.snake0.body) - self.snake_size
            self.apple_eaten1 = len(self.snake1.body) - self.snake_size
            self.apple_coordinate = self.random_non_occupied_cell()

        print("snake0 -> " + bot0_direction.name + " snake1 -> " + bot1_direction.name)
        print("Apples eaten: " + self.bot0.name + " : " + str(self.apple_eaten0) + " " +
              self.bot1.name + " : " + str(self.apple_eaten1))

        cont = not (s0_dead or s1_dead)

        if not cont:
            if s0_dead ^ s1_dead:
                self.game_result = ('0' if s0_dead else '1') + " - " + ('0' if s1_dead else '1')
            elif s0_dead and s1_dead:
                self.game_result = ('1' if self.apple_eaten0 > self.apple_eaten1 else '0') + " - " + ('1' if self.apple_eaten1 > self.apple_eaten0 else '0')

            print("Result: " + self.game_result)

        return cont

    def print_game(self):
        for i in range(self.maze_size.x):
            for j in range(self.maze_size.y):
                cur = Coordinate(i, j)
                if self.apple_coordinate == cur:
                    print('X', end='')
                elif self.snake0.get_head() == cur:
                    print('h', end='')
                elif cur in self.snake0.body:
                    print('b', end='')
                elif self.snake1.get_head() == cur:
                    print('H', end='')
                elif cur in self.snake1.body:
                    print('B', end='')
                else:
                    print('.', end='')
            print()
