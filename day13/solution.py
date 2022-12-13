import sys

FILENAME = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"


class Packet:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def __lt__(self, other):
        return compare(self.data, other.data)


def compare(p1, p2) -> bool:
    if isinstance(p1, int) and isinstance(p2, int):
        if p1 == p2:
            return
        return p1 < p2
    elif isinstance(p1, list) and isinstance(p2, list):
        for i in range(len(p1)):
            try:
                comp = compare(p1[i], p2[i])
                if comp is not None:
                    return comp
            except IndexError:
                return False
        if len(p1) < len(p2):
            return True
    elif isinstance(p1, int):
        p1 = [p1]
        return compare(p1, p2)
    else:
        p2 = [p2]
        return compare(p1, p2)

def binary_search(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if x > arr[mid]:
            lo = mid + 1
        else:
            hi = mid
    return lo
            
         
with open(FILENAME, "r") as f:
    curr = " "
    i = 1
    correct = []
    packets = []
    while curr != "":
        p1 = Packet(eval(f.readline().rstrip("\n")))
        p2 = Packet(eval(f.readline().rstrip("\n")))
        if p1 < p2:
            correct.append(i)
        curr = f.readline()
        i += 1

        packets.insert(binary_search(packets, p1), p1)
        packets.insert(binary_search(packets, p2), p2)
    p1, p2 = Packet([[2]]), Packet([[6]])
    key1 = binary_search(packets, p1)
    packets.insert(key1, p1)
    key2 = binary_search(packets, p2) 
 
solution1 = sum(correct)
print(f"{solution1=}")

solution2 = (key1+1) * (key2+1)
print(f"{solution2=}")
