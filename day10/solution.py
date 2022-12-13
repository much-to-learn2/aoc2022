import sys
import re
from typing import Optional, Iterable
from functools import wraps


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

class Register:
    def __init__(self, start_cycle: int = 20, n_cycles: int = 40):
        self.val = 1
        self.cycle = 0
        self.start_cycle = start_cycle
        self.n_cycles = n_cycles
        self.watched_cycles = {}
        self.crt = []

    def noop(self):
        self.increment()

    def addx(self, val: int):
        self.increment()
        self.increment()
        self.val += val

    def increment(self):
        self.draw()
        self.cycle += 1
        if (self.cycle - self.start_cycle) % self.n_cycles == 0:
            self.watched_cycles[self.cycle] = self.val

    @property
    def row_number(self):
        return (self.cycle - self.start_cycle) // self.n_cycles

    @property
    def col_number(self):
        return (self.cycle - self.start_cycle) % self.n_cycles 

    def draw(self): 
        if len(self.crt) < (self.row_number + 1):
            self.crt.append([])
        c = "."
        if abs(self.col_number - self.val) <= 1:
            c = "#"
        if self.row_number >= 0:
            self.crt[self.row_number].append(c)
    
    def print_crt(self):
        for row in self.crt:
            for c in row:
                print(c, end="")
            print()


with open(FILENAME, "r") as f:
    pattern = r"(noop|addx)(?: )?(-?\d*)?"
    r1 = Register(start_cycle=20, n_cycles=40)
    r2 = Register(start_cycle=0, n_cycles=40)
    for line in f.readlines():
        line = line.rstrip("\n")
        m = re.match(pattern, line)
        op = m.group(1)
        if op == "noop":
            r1.noop()
            r2.noop()
        else:
            val = int(m.group(2))
            r1.addx(val)
            r2.addx(val)


solution1 = 0
for k, v in r1.watched_cycles.items():
    solution1 += k * v
print(f"{solution1=}")

r2.print_crt()
