def get_priority(s: str) -> int:
    n = len(s) // 2
    first, second = s[:n], s[n:]
    intersect = set(first) & set(second)
    res = 0
    # 'a' = 97, 'A' = 65
    for c in intersect:
        res += ord(c)
        if c.isupper():
            res -= 38
        else:
            res -= 96
    return res

with open("input.txt", "r") as f:
    solution1 = 0
    for line in f.readlines():
        solution1 += get_priority(line.rstrip("\n"))

print(f"{solution1=}") 
