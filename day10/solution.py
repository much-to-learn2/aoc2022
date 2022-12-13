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

    def noop(self):
        self.cycle += 1
        self.record()

    def addx(self, val: int):
        self.cycle += 1
        self.record()
        self.cycle += 1
        self.record()
        self.val += val

    def record(self):
        if (self.cycle - self.start_cycle) % self.n_cycles == 0:
            self.watched_cycles[self.cycle] = self.val


with open(FILENAME, "r") as f:
    pattern = r"(noop|addx)(?: )?(-?\d*)?"
    register = Register()
    for line in f.readlines():
        line = line.rstrip("\n")
        m = re.match(pattern, line)
        op = m.group(1)
        if op == "noop":
            register.noop()
        else:
            val = int(m.group(2))
            register.addx(val)


solution1 = 0
for k, v in register.watched_cycles.items():
    solution1 += k * v
print(f"{register.watched_cycles=}")
print(f"{solution1=}")
