from dataclasses import dataclass
import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()

grid : list[str]= []

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        grid.append(line.strip())

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
                candidate += row[start]
            end = j
            if end < len(row):
                end += 1
                candidate += row[end - 1]
            if i > 0:
                candidate += grid[i-1][start:end]
            if i + 1 < len(grid):
                candidate += grid[i+1][start:end]
            
            if any(not c.isdigit() and c != "." for c in candidate):
                s += num

        else:
            j += 1
print(s)