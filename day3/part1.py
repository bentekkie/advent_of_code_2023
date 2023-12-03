from dataclasses import dataclass
import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()

grid: list[str] = []

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        grid.append(line.strip())


def neighbors(i: int, j_start: int, j_end: int):
    if j_start > 0:
        j_start -= 1
        yield grid[i][j_start]
    if j_end < len(grid[i]):
        yield grid[i][j_end]
        j_end += 1
    if i > 0:
        yield from grid[i - 1][j_start:j_end]
    if i + 1 < len(grid):
        yield from grid[i + 1][j_start:j_end]


s = 0
for i, row in enumerate(grid):
    j = 0
    while j < len(row):
        if row[j].isdigit():
            start = j
            while j < len(row) and row[j].isdigit():
                j += 1
            if any(not c.isdigit() and c != "." for c in neighbors(i, start, j)):
                s += int(row[start:j])
        else:
            j += 1
print(s)
