import sys
import re
from typing import Tuple, Optional


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class Rope:
    direction_map = {
        "R": (0, 1),
        "L": (0, -1),
        "U": (-1, 0),
        "D": (1, 0),
    }

    def __init__(self):
        self.head = (0, 0)
        self.tail = (0, 0)
        self.head_locations = [self.head]
        self.tail_locations = [self.tail]
        self.next_rope = None
        self.last_rope = None

    def move(self, direction: str, magnitude: int):
        x, y = self.direction_map[direction]
        for _ in range(magnitude):
            self.head = self.head[0] + x, self.head[1] + y
            self.head_locations.append(self.head)
            self.chase()

    def chase(self):
        """
        move the tail towards the head
        """
        x_diff = self.head[0] - self.tail[0]
        y_diff = self.head[1] - self.tail[1] 
        if abs(x_diff) <= 1 and abs(y_diff) <= 1:
            return
        x, y = self.tail
        if x_diff:
            x += (1 if x_diff > 0 else -1)
        if y_diff:
            y += (1 if y_diff > 0 else -1)
        self.tail = (x, y)
        self.tail_locations.append(self.tail)
        if self.next_rope:
            self.next_rope.head = self.tail
            self.next_rope.head_locations.append(self.next_rope.head)
            self.next_rope.chase() 

    @classmethod
    def build_compound_rope(cls, size: int):
        head = cls()
        prev = head
        for _ in range(size):
            curr = cls()
            prev.next_rope = curr
            prev = curr
        last = curr
        curr = head
        while curr is not None:
            curr.last_rope = last
            curr = curr.next_rope
        return head


with open(FILENAME, "r") as f:
    pattern = r"([RLUD]) (\d+)"
    r1 = Rope()
    r2 = Rope.build_compound_rope(9)
    for line in f.readlines():
        line = line.rstrip("\n")
        m = re.match(pattern, line) 
        direction, magnitude = m.group(1), int(m.group(2))
        r1.move(direction, magnitude)
        r2.move(direction, magnitude)

solution1 = len(set(r1.tail_locations))
print(f"{solution1=}")

solution2 = len(set(r2.last_rope.head_locations))
print(f"{solution2=}")
