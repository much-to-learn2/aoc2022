import sys
import re
from typing import Callable, List, Tuple


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class Monkey:
    def __init__(
        self, 
        items: List[int], 
        operator_args: Tuple[Callable[[int, int], int], int, int],
        divisor: int, 
        if_true: int, 
        if_false: int
    ):
        self.items = items
        self.operator_args = operator_args
        self.divisor = divisor
        self.if_true = if_true
        self.if_false = if_false

        def op(x: str) -> int:
            add = lambda x, y: x + y
            mul = lambda x, y: x * y
            f, term1, term2 = operator_args
            term1 = x if term1 == "old" else int(term1)
            term2 = x if term2 == "old" else int(term2)
            if f == "+":
                func = add
            elif f == "*":
                func = mul
            return func(term1, term2)
        self.op = op

class Monkeys:
    def __init__(self, monkeys: List["Monkey"]):
        self.monkeys = monkeys
        self.items_inspected = [0 for _ in monkeys]

    def resolve_monkey(self, monkey_key: int):
        monkey = self.monkeys[monkey_key]
        while monkey.items:
            self.items_inspected[monkey_key] += 1
            new_item = monkey.op(monkey.items.pop()) // 3
            if new_item % monkey.divisor == 0:
                self.monkeys[monkey.if_true].items.append(new_item)
            else:
                self.monkeys[monkey.if_false].items.append(new_item)

    def round(self):
        for i in range(len(self.monkeys)):
            self.resolve_monkey(i)
    
    @property
    def score(self):
        items = sorted(self.items_inspected, reverse=True)
        return items[0] * items[1]
                
            

with open(FILENAME, "r") as f:
    it = iter(f)
    monkeys = []
    while True:
        try:
            # monkey 
            monkey_re = r"Monkey (\d+)"
            monkey = next(it)
            monkey_num = int(re.match(monkey_re, monkey).group(1))
            print(f"{monkey_num=}")

            # starting_items 
            starting_re = r"\d+"
            starting = next(it)
            starting_items = []
            for item in re.findall(starting_re, starting):
                starting_items.append(int(item))
            print(f"{starting_items}")

            # operation
            op = next(it)
            header = "\s+Operation: new = "
            term = r"(old|\d+)"
            operator = r"([\+\*\-\\])"
            add = lambda x, y: x + y
            multiply = lambda x, y: x * y
            op_re = header + term + " " + operator + " " + term
            m = re.match(op_re, op)
            term1, operator, term2 = m.group(1), m.group(2), m.group(3)
            operator_args = (operator, term1, term2)
            print(f"{operator_args=}")
            
            # boolean test
            test = next(it)
            test_re = r"\s+Test: divisible by (\d+)"
            divisible_by = int(re.match(test_re, test).group(1))        
            print(f"{divisible_by=}")
    
            # if true
            if_true = next(it)
            if_true_re = r"\s+If true: throw to monkey (\d+)"
            if_true = int(re.match(if_true_re, if_true).group(1))

            # if false
            if_false = next(it)
            if_false_re = r"\s+If false: throw to monkey (\d+)"
            if_false = int(re.match(if_false_re, if_false).group(1))

            monkey = Monkey(starting_items, operator_args, divisible_by, if_true, if_false)
            monkeys.append(monkey)

            # divider
            next(it)
        except StopIteration:
            break
    monkeys = Monkeys(monkeys)
    for _ in range(20):
        monkeys.round()

solution1 = monkeys.score
print(f"{solution1=}")


