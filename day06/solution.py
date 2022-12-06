def n_unique_index(s: str, n: int) -> int:
    i, j = 0, 0
    hm = {s[0]: 0}
    while j < len(s):
        while (j-i)+1 < n:
            j += 1
            hm[s[j]] = j

        if len(hm) == n:
            return j+1

        if hm[s[i]] <= i:
            hm.pop(s[i])
        i += 1

        j += 1
        hm[s[j]] = j
        

with open("input.txt", "r") as f:
    s = f.readline().rstrip("\n")
    solution1 = n_unique_index(s, 4)
    solution2 = n_unique_index(s, 14)

print(f"{solution1=}")
print(f"{solution2=}")
