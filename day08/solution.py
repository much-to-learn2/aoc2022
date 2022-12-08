from typing import Dict, Tuple, List


direction_map = {
    "left": "right",
    "right": "left",
    "up": "down",
    "down": "up",
}


class Node:
    def __init__(self, x: int, y: int, value: int, edge: bool = False, visible: bool = True):
        self.x = x
        self.y = y
        self.value = value
        self.edge = edge
        self.visible = visible
        self.neighbors = {}
  
    def __hash__(self):
        return hash((self.x, self.y))
  
    def __repr__(self):
        return f"Node({self.value}) at ({self.x}, {self.y})"
  
    def set_visibility(self):
        if self.edge:
            return
        for direction in direction_map:
            curr = self.neighbors[direction]
            while curr.value < self.value:
                if curr.edge:
                    return
                curr = curr.neighbors[direction]
        self.visible = False

    @property
    def scenic_score(self):
        res = 1
        for direction in direction_map:
            if direction not in self.neighbors:
                continue
            score = 1
            curr = self.neighbors[direction]
            while curr.value < self.value and not curr.edge:
                score += 1
                curr = curr.neighbors[direction]
            res *= score
        return res
            
                     
class Graph:
    def __init__(self, points: List[List[int]]):
        self.x_len = len(points)
        self.y_len = len(points[0]) 
        self.nodes: Dict[Tuple[int, int], "Node"] = {}
        for x in range(self.x_len):
            for y in range(self.y_len):
                self.create_node(x, y, points[x][y]) 
        for node in self.nodes.values():
            node.set_visibility()
                
    def create_node(self, x: int, y: int, value: int):
        """
        recursive approach doesn't work for large input,
        because python recursive limit is ~1000
        """
        edge = False
        if x in {0, self.x_len - 1} or y in {0, self.y_len - 1}:
            edge = True
        node = Node(x, y, value, edge, True) # default visible
        self.nodes[(x, y)] = node
        
        neighbor_coords = {
            direction: (x, y) for (direction, (x, y)) in [
                ("left", (x+1, y)), 
                ("right", (x-1, y)), 
                ("down", (x, y-1)), 
                ("up", (x, y+1)),
            ]
            if x >= 0 and x <= self.x_len and y >= 0 and y <= self.y_len
        } 
        for direction, coord in neighbor_coords.items():
            if coord in self.nodes:
                inverse = direction_map[direction]
                self.nodes[coord].neighbors[direction] = node
                node.neighbors[inverse] = self.nodes[coord]
        
        return node

    @property
    def n_visible(self):
        res = 0
        for node in self.nodes.values():
            if node.visible:
                res += 1
        return res
             
        
with open("input.txt", "r") as f:
    coords = []
    for line in f.readlines():
        line = line.rstrip("\n")
        line_coords = []
        for c in line:
            line_coords.append(int(c))
        coords.append(line_coords) 
    g = Graph(coords)

solution1 = g.n_visible
print(f"{solution1=}")

solution2 = max(node.scenic_score for node in g.nodes.values())
print(f"{solution2=}")
