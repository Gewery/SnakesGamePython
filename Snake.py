import collections
from Coordinate import Coordinate


class Snake:
    elements = set()
    body = collections.deque()
    maze_size = Coordinate()

    def __init__(self, head, tail_direction, size, maze_size):
        self.maze_size = maze_size
        self.elements = set()
        self.body = collections.deque()

        p = head
        for i in range(size):
            self.body.append(p)
            self.elements.add(p)
            p = p.move_to(tail_direction)

    def get_head(self):
        return self.body[0]

    def move_to(self, d, grow):
        new_head = self.get_head().move_to(d)

        if not new_head.in_bounds(self.maze_size):
            return False

        if not grow:
            self.elements.remove(self.body[-1])
            self.body.remove(self.body[-1])

        if new_head in self.elements:
            return False

        self.body.appendleft(new_head)
        self.elements.add(new_head)

        return True

    def head_collides_with(self, other):
        return self.get_head() in other.elements
