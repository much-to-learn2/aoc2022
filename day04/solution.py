from typing import Tuple


def parseLine(line: str) -> Tuple[int, int, int, int]:
    line = line.rstrip("\n")
    x, y = line.split(",")
    x1, x2 = x.split("-")
    y1, y2 = y.split("-")
    return (int(point) for point in (x1, x2, y1, y2))    

def overlaps(x1: int, x2: int, y1: int, y2: int) -> bool:
    return (x1 <= y1 and x2 >= y2) or (y1 <= x1 and y2 >= x2)

with open("input.txt", "r") as f:
    solution1 = 0
    for line in f.readlines():
        x1, x2, y1, y2 = parseLine(line)
        if overlaps(x1, x2, y1, y2):
            solution1 += 1

print(f"{solution1=}")
