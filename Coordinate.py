class Coordinate:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, a, b):
        return Coordinate(a.x + b.x, a.y + b.y)

    def move_to(self, d):
        return self.add(self, d.value)

    def in_bounds(self, maze_size):
        return 0 <= self.x <= maze_size.x and 0 <= self.y <= maze_size.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 100 + self.y
