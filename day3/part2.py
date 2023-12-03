import pathlib
import os
from collections import defaultdict

THIS_DIR = pathlib.Path(__file__).parent.resolve()

grid: list[str] = []

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        grid.append(line.strip())


def neighbors(i: int, j_start: int, j_end: int):
    if j_start > 0:
        j_start -= 1
        yield (grid[i][j_start], (i, j_start))
    if j_end < len(grid[i]):
        yield (grid[i][j_end], (i, j_end))
        j_end += 1
    if i > 0:
        yield from (
            (c, (i - 1, x)) for x, c in enumerate(grid[i - 1][j_start:j_end], j_start)
        )
    if i + 1 < len(grid):
        yield from (
            (c, (i + 1, x)) for x, c in enumerate(grid[i + 1][j_start:j_end], j_start)
        )


gears = defaultdict(list[int])

s = 0
for i, row in enumerate(grid):
    j = 0
    while j < len(row):
        if row[j].isdigit():
            start = j
            while j < len(row) and row[j].isdigit():
                j += 1
            num = int(row[start:j])
            for c, gear in neighbors(i, start, j):
                if c == "*":
                    gears[gear].append(num)
        else:
            j += 1

for g, nums in gears.items():
    if len(nums) == 2:
        s += nums[0] * nums[1]
print(s)
