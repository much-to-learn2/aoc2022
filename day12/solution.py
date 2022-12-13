import sys
from typing import List, Tuple, Callable, Iterable
from collections import deque

FILENAME = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"


class Node:
    def __init__(self, val: int, x: int, y: int):
        self.x = x
        self.y = y
        self.val = val
        self.neighbors = []

class Graph:
    def __init__(self, points: List[List[int]], start: "Point", end: "Point"):
        self.start = start
        self.end = end
        self.x_len = len(points)
        self.y_len = len(points[0])
        self.nodes = {}
        for x in range(self.x_len):
            for y in range(self.y_len):
                self.create_node(points[x][y], x, y)

    def create_node(self, val: int, x: int, y: int):
        node = Node(val, x, y)
        self.nodes[(x,y)] = node
        neighbor_coords = [
            (x, y) for (x, y) in [
                (x+1, y),
                (x-1, y),
                (x, y+1),
                (x, y-1),
            ]
            if x >= 0 and x <= self.x_len and y >= 0 and y <= self.y_len
        ]
        for coord in neighbor_coords:
            if coord in self.nodes:
                self.nodes[coord].neighbors.append(node)
                node.neighbors.append(self.nodes[coord])
        return node

    def get_paths(self, 
        start: "Point", 
        terminal_condition: Callable[["Point"], bool],
        neighbors: Callable[["Point"], Iterable["Point"]],
    ) -> Iterable["Point"]:
        visited = set()
        node = self.nodes[start]
        path = []
        q = deque([(node, path)])
        while q:
            curr, path = q.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            if terminal_condition(curr):
                yield path
            path = path + [curr]
            for neighbor in neighbors(curr):
                q.append((neighbor, path))

    def shortest_path_up(self, start: "Point", end: "Point") -> List["Point"]:
        terminal_condition = lambda x: x == self.nodes[end]  
        neighbors = lambda x: [neighbor for neighbor in x.neighbors if neighbor.val <= x.val + 1]
        return next(self.get_paths(start, terminal_condition, neighbors))

    def shortest_path_down(self, start: "Point") -> List["Point"]:
        terminal_condition = lambda x: x.val == 0
        neighbors = lambda x: [neighbor for neighbor in x.neighbors if neighbor.val >= x.val - 1]
        return next(self.get_paths(start, terminal_condition, neighbors))
            

Point = Tuple[int, int]
        


with open(FILENAME, "r") as f:
    points = []
    start, end = (0,0), (0,0)
    for x, line in enumerate(f.readlines()):
        line = line.rstrip("\n")
        curr_line = []
        for y, c in enumerate(line): 
            if c == "S":
                start = (x, y)
                c = "a"
            if c == "E":
                end = (x, y)
                c = "z"
            val = ord(c) - ord("a")
            curr_line.append(val)
        points.append(curr_line) 
    g = Graph(points, start, end)

solution1 = len(g.shortest_path_up(g.start, g.end))
print(f"{solution1=}")

solution2 = len(g.shortest_path_down(g.end))
print(f"{solution2=}")
