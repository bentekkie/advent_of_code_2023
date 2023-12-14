import pathlib
import os
from functools import cache

THIS_DIR = pathlib.Path(__file__).parent.resolve()

grids: list[list[str]] = []

curr = []


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        if line.strip() == "":
            grids.append(curr)
            curr = []
        else:
            curr.append(line.strip())
if len(curr):
    grids.append(curr)


def trans(grid: list[str]) -> list[str]:
    return ["".join(l) for l in zip(*grid)]


def is_pal(s: str):
    return s == s[::-1]


def score(grid: list[str]):
    for i in range(1, len(grid[0])):
        size = min(i, len(grid[0]) - i)
        if all(is_pal(row[i - size : i + size]) for row in grid):
            return i
    return 0


print(sum(score(grid) + 100 * score(trans(grid)) for grid in grids))
