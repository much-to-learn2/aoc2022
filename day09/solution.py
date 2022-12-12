import sys
import re


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
        self.tail_locations=  [self.tail]

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


with open(FILENAME, "r") as f:
    pattern = r"([RLUD]) (\d+)"
    rope = Rope()
    for line in f.readlines():
        line = line.rstrip("\n")
        m = re.match(pattern, line) 
        direction, magnitude = m.group(1), int(m.group(2))
        rope.move(direction, magnitude)

solution1 = len(set(rope.tail_locations))
print(f"{solution1=}")
