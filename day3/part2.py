from dataclasses import dataclass
import pathlib
import os
from collections import defaultdict

THIS_DIR = pathlib.Path(__file__).parent.resolve()

grid : list[str]= []

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        grid.append(line.strip())

gears = defaultdict(list)

s = 0
for i, row in enumerate(grid):
    j = 0
    while j < len(row):
        if row[j].isdigit():
            start = j
            while j < len(row) and row[j].isdigit():
                j += 1
            candidate = ""
            num = int(row[start:j])
            if start > 0:
                start -= 1
                if row[start] == "*":
                    gears[(i,start)].append(num)
            end = j
            if end < len(row):
                end += 1
                if row[end - 1] == "*":
                    gears[(i,end-1)].append(num)
            if i > 0:
                for tj in range(start, end):
                    if grid[i-1][tj] == "*":
                        gears[(i-1, tj)].append(num)
            if i + 1 < len(grid):
                for tj in range(start,end):
                    if grid[i+1][tj] == "*":
                        gears[(i+1, tj)].append(num)
        else:
            j += 1

for g, nums in gears.items():
    if len(nums) == 2:
        s += nums[0]*nums[1]
print(s)