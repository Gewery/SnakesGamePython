from bots.RandomBot import RandomBot
from Direction import Direction
from SnakeGame import SnakeGame
from bots.RandomBot import RandomBot
from Coordinate import Coordinate


class Main:
    STEPS_ALLOWED = 120

    bot0 = RandomBot()
    bot1 = RandomBot()

    maze_size = Coordinate(8, 8)
    head0 = Coordinate(2, 2)
    head1 = Coordinate(5, 5)
    size=3

    tail_direction0 = Direction.DOWN
    tail_direction1 = Direction.UP

    game = SnakeGame(maze_size, head0, tail_direction0, head1, tail_direction1, size, bot0, bot1)
    game.run(STEPS_ALLOWED)
