import pathlib
import os
import cmath
from functools import cache

THIS_DIR = pathlib.Path(__file__).parent.resolve()


r_rocks = set()
s_rocks = set()
south = 0

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for row, line in enumerate(f.readlines()):
        south += 1
        for col, c in enumerate(line.strip()):
            if c == "#":
                s_rocks.add(row + col * 1j)
            if c == "O":
                p = row + col * 1j
                while p.real > 0 and p - 1 not in r_rocks and p - 1 not in s_rocks:
                    p -= 1
                r_rocks.add(p)

print(sum(south - p.real for p in r_rocks))
