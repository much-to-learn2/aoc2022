import heapq


class Elf:
    def __init__(self, caloriesList):
        self.calories = caloriesList
        self.totalCalories = sum(self.calories)

with open("input.txt", "r") as f:
    calories = []
    elves = []
    heap = []
    for line in f.readlines():
        if line != "\n":
            calorieCount = int(line.rstrip("\n"))
            calories.append(calorieCount)
        else:
            elf = Elf(calories)
            elves.append(elf)
            heapq.heappush(heap, elf.totalCalories * -1)
            calories = []

solution1 = heapq.heappop(heap) * -1
print(f"{solution1=}")

solution2 = solution1 + heapq.heappop(heap) * -1 + heapq.heappop(heap) * -1
print(f"{solution2=}")

