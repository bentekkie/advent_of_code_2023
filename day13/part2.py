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


def smudge(grid: list[str]):
    original_v, original_h = rels(grid), rels(trans(grid))
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            new_grid = (
                grid[:i]
                + [line[:j] + ("#" if c == "." else ".") + line[j + 1 :]]
                + grid[i + 1 :]
            )
            for r in rels(new_grid):
                if r not in original_v:
                    return r
            for r in rels(trans(new_grid)):
                if r not in original_h:
                    return r * 100
    return 0


def is_pal(s: str):
    return s == s[::-1]


def rels(grid: list[str]):
    return [
        i
        for i in range(1, len(grid[0]))
        if all(
            is_pal(row[i - min(i, len(row) - i) : i + min(i, len(row) - i)])
            for row in grid
        )
    ]


print(sum(smudge(grid) for grid in grids))
