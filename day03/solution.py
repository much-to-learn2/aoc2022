def get_priority(*args) -> int:
    intersect = set(args[0])
    for s in args:
        intersect = intersect & set(s)
    res = 0
    # 'a' = 97, 'A' = 65
    for c in intersect:
        res += (ord(c) - ord("a") + 1) % 58
        #res += ord(c)
        #if c.isupper():
        #    res -= 38
        #else:
        #    res -= 96
    return res

with open("input.txt", "r") as f:
    solution1, solution2 = 0, 0
    group = []
    for i, line in enumerate(f.readlines()):
        line = line.rstrip("\n")
        n = len(line) // 2
        first, second = line[:n], line[n:]
        solution1 += get_priority(first, second)

        group.append(line)
        if (i+1) % 3 == 0:
            solution2 += get_priority(*group)
            group = []

print(f"{solution1=}") 
print(f"{solution2=}")
