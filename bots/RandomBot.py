from Bot import Bot
from random import choice
from Direction import Direction
from Coordinate import Coordinate


class RandomBot(Bot):

    def choose_direction(self, snake, opponent, maze_size, apple):
        d = None
        x = -1
        y = -1
        while not self.check(x, y, snake, opponent, maze_size):
            d = choice(list(Direction))
            coord = snake.get_head()
            coord = coord.move_to(d)
            x = coord.x
            y = coord.y
        return d

    def check(self, x, y, snake, opponent, maze_size):
        if not (0 <= x < maze_size.x and 0 <= y < maze_size.y):
            return False
        coord = Coordinate(x, y)
        if coord in snake.elements or coord in opponent.elements:
            return False

        return True
