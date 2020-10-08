from enum import Enum
from Coordinate import Coordinate


class Direction(Enum):
    RIGHT = Coordinate(0, 1)
    LEFT = Coordinate(0, -1)
    DOWN = Coordinate(1, 0)
    UP = Coordinate(-1, 0)
