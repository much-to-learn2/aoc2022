import sys
import re
from typing import Tuple, Iterable, List

FILENAME = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"


class Cavern:
    def __init__(self):
        self.sand_location = (500, 0)
        self.rocks = set()
        self.sand = set()
        self.abyss = 0
        self.floor = 0

    @classmethod
    def from_paths(cls, paths: List[List["Point"]]):
        cavern = cls()
        for path in paths:
            if len(path) == 1:
                cavern.rocks.add(path[0])
            for i in range(1, len(path)):
                p1 = path[i-1]
                p2 = path[i]
                for point in cls.get_points_from_line(p1, p2):
                    cavern.rocks.add(point)
        cavern.abyss = max(y for x, y in cavern.rocks)
        cavern.floor = cavern.abyss + 2
        return cavern

    def drop_sand(self, floor: bool = False) -> bool:
        curr = self.next_location(self.sand_location, floor)
        prev = self.sand_location
        if curr in self.sand:
            return False
        while prev != curr:
            prev = curr
            curr = self.next_location(curr, floor)

            if not floor and curr[1] == self.abyss:
                return False
        self.sand.add(curr)
        return True

    def fill_sand(self, floor: bool = False) -> int:
        curr = True
        i = 0
        while curr:
            if i % 1000 == 0:
                self.print()
            curr = self.drop_sand(floor)
            i += 1
        return len(self.sand)

    def next_location(self, location: "Point", floor: bool = False) -> "Point":
        """
        where does the sand go next?
        """
        x, y = location
        blocked = self.rocks | self.sand
        if floor and y == self.floor - 1:
            return x, y
        elif (p := (x, y+1)) not in blocked:
            return p
        elif (p := (x-1, y+1)) not in blocked:
            return p
        elif (p := (x+1, y+1)) not in blocked:
            return p
        else:
            return x, y

    @staticmethod
    def get_points_from_line(p1: "Point", p2: "Point") -> Iterable["Point"]:
        x_diff, y_diff = p2[0] - p1[0], p2[1] - p1[1]
        if x_diff and y_diff:
            raise ValueError("Diagonal line")
        if x_diff:
            step = 1 if x_diff > 0 else -1
            for i in range(p1[0], p2[0] + step, step):
                yield (i, p1[1])
        if y_diff:
            step = 1 if y_diff > 0 else -1
            for i in range(p1[1], p2[1] + step, step):
                yield(p1[0], i)

    def print(self):
        blocked = self.rocks | self.sand | {self.sand_location}
        x_min = min(x for x, y in blocked) - 1
        x_max = max(x for x, y in blocked) + 1
        y_min = min(y for x, y in blocked)
        y_max = max(y for x, y in blocked) + 1
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if (x, y) in self.sand:
                    c = "o"
                elif (x, y) == self.sand_location:
                    c = "+"
                elif (x, y) in self.rocks:
                    c = "#"
                else:
                    c = "."
                print(c, end="")
            print()


Point = Tuple[int, int]

with open(FILENAME, "r") as f:
    pattern = r"(\d+),(\d+)"
    paths = []
    for line in f.readlines():
        matches = re.finditer(pattern, line)
        path = []
        for match in matches:
            x, y = int(match.group(1)), int(match.group(2))
            path.append((x, y))
        paths.append(path)
    cavern = Cavern.from_paths(paths)

solution1 = cavern.fill_sand()
print(f"{solution1=}")

solution2 = cavern.fill_sand(floor=True)
print(f"{solution2=}")
