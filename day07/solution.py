import re
from typing import Optional, List, Union


class File:
    def __init__(self, name: str, size: int, directory: Optional["Directory"] = None):
        self.name = name
        self.size = size
        self.parent = directory


class Directory:
    def __init__(self, name: str, directory: Optional["Directory"] = None):
        self.name = name
        self.children = {}
        self.directory = directory
        self.size = 0


class FileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.cwd = self.root
        self.total = 70000000

    @property
    def unused(self):
        return self.total - self.root.size

    def register_content(self, content: Union["File", "Directory"]):
        self.cwd.children[content.name] = content
        content.directory = self.cwd
        
        # update sizes
        curr = self.cwd
        while curr is not None:
            curr.size += content.size
            curr = curr.directory
      
    def cd(self, directory: str):
        if directory == "..":
            self.cwd = self.cwd.directory
            return
        elif directory == "/":
            self.cwd = self.root
            return
        self.cwd = self.cwd.children[directory] 

    def filter_to_small_directories(self, n: int = 100000) -> List["Directory"]:
        """
        generic DFS applied to directory structure
        could be made better/more generic
        """
        stack = [self.root]
        res = []
        while stack:
            curr = stack.pop()
            if curr.size <= n:
                res.append(curr)
            for neighbor in curr.children.values():
                if isinstance(neighbor, Directory):
                    stack.append(neighbor)

        return res

    def find_smallest_directory_to_delete(self, n: int = 30000000) -> "Directory":
        threshhold = n - self.unused
        res = self.root
        stack = [self.root]
        while stack:
            curr = stack.pop()
            if curr.size < res.size:
                res = curr
            for neighbor in curr.children.values():
                if neighbor.size >= threshhold and isinstance(neighbor, Directory):
                    stack.append(neighbor)
        return res
            
 
with open("input.txt", "r") as f:
    fs = FileSystem()
    cd_re = r"\$ cd (.+)"
    file_re = r"(\d+) ([\w\d]+)" 
    dir_re = r"dir (\w+)" 
    # ls_re = r"$ ls ([\w\d]+)"
    for idx, command in enumerate(f.readlines()):
        command = command.rstrip("\n")
        if m := re.match(cd_re, command):
            name = m.group(1)
            fs.cd(name)
        elif m := re.match(file_re, command):
            name, size = m.group(2), int(m.group(1))
            obj = File(name, size)
            fs.register_content(obj)
        elif m := re.match(dir_re, command):
            name = m.group(1)
            obj = Directory(name)
            fs.register_content(obj)
        elif command == "$ ls": 
            continue 

solution1 = 0
for d in fs.filter_to_small_directories():
    solution1 += d.size

solution2 = fs.find_smallest_directory_to_delete().size

print(f"{solution1=}")
print(f"{solution2=}")
