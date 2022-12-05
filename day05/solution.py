import re
from typing import List, Iterable

class Stacks:
    def __init__(self, *stacks: List[str]):
        self.stacks = stacks

    def move(self, n: int, fromStack: int, toStack: int):
        for _ in range(n):
            self.stacks[toStack].append(self.stacks[fromStack].pop())

    def move_9001(self, n: int, fromStack: int, toStack: int):
        buff = []
        for _ in range(n):
            buff.append(self.stacks[fromStack].pop())
        self.stacks[toStack].extend(reversed(buff))

    @property
    def tops(self):
        res = []
        for stack in self.stacks:
            if stack:
                res.append(stack[-1])
            else:
                res.append("")
        return res

    @classmethod
    def from_strings(cls, s: List[str]):
        """
        parse the input string into an instance of `Stacks` class.
        You could do this as a standalone parse function;
        I don't know which is more idiomatic.
        """
        stack_idxs = {}
        for i in range(len(s[-1])):
            if s[-1][i].isnumeric() and not s[-1][i+1].isnumeric():
                stack_idxs[int(s[-1][i]) - 1] = i

        stacks = [[] for _ in stack_idxs]
        for vals in reversed(s[:-1]):
            for i, j in stack_idxs.items():
                if vals[j] != " ":
                    stacks[i].append(vals[j])

        return cls(*stacks)

    @staticmethod
    def parse_command_string(s: str) -> Iterable[int]:
        pattern = r"move (\d+) from (\d) to (\d)" 
        match = re.match(pattern, s)
        n, fromStack, toStack = (int(match.group(i)) for i in (1,2,3))
        return n, fromStack-1, toStack-1
                

with open("input.txt", "r") as f:
    init = []
    curr = f.readline()
    while curr != "\n":
        init.append(curr.rstrip("\n"))
        curr = f.readline()
    stacks = Stacks.from_strings(init)
    stacks2 = Stacks.from_strings(init)

    for line in f.readlines():
        line = line.rstrip("\n")
        n, fromStack, toStack = stacks.parse_command_string(line)
        stacks.move(n, fromStack, toStack)
        stacks2.move_9001(n, fromStack, toStack)

solution1 = stacks.tops
print(f"{solution1=}")

solution2 = stacks2.tops
print(f"{solution2=}")
