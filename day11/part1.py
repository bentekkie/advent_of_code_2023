import pathlib
import os
from collections import defaultdict
from itertools import combinations

THIS_DIR = pathlib.Path(__file__).parent.resolve()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    raw_grid = [l.strip() for l in f.readlines()]
    galaxies = []
    row = 0
    effective_row = 0
    while row < len(raw_grid):
        if all(c == "." for c in raw_grid[row]):
            effective_row += 1
        else:
            col = 0
            effective_col = 0
            while col < len(raw_grid[row]):
                if all(raw_grid[r][col] == "." for r in range(len(raw_grid))):
                    effective_col += 1
                else:
                    if raw_grid[row][col] == "#":
                        galaxies.append((effective_row, effective_col))
                col += 1
                effective_col += 1
        row += 1
        effective_row += 1


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


print(sum(dist(a, b) for a, b in combinations(galaxies, 2)))
