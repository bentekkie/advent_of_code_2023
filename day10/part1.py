import pathlib
import os
from collections import defaultdict

THIS_DIR = pathlib.Path(__file__).parent.resolve()

start = None
neighbors = defaultdict(set)
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for row, line in enumerate(f.readlines()):
        for col, c in enumerate(line.strip()):
            curr = (row, col)
            if c == "S":
                start = curr
            if c == "|" or c == "L" or c == "J":
                neighbors[(row - 1, col)].add(curr)
            if c == "|" or c == "7" or c == "F":
                neighbors[(row + 1, col)].add(curr)
            if c == "-" or c == "J" or c == "7":
                neighbors[(row, col - 1)].add(curr)
            if c == "-" or c == "L" or c == "F":
                neighbors[(row, col + 1)].add(curr)


def far(start):
    seen = {start}
    to_check = neighbors[start]
    seen.update(to_check)
    steps = 1
    while True:
        steps += 1
        next_check = {
            n
            for p in to_check
            for n in neighbors[p]
            if n not in seen and p in neighbors[n]
        }
        if len(next_check) == 1:
            return steps
        seen.update(next_check)
        to_check = next_check


print(far(start))
