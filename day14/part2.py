import pathlib
import os
import cmath
from functools import cache


THIS_DIR = pathlib.Path(__file__).parent.resolve()

s_rocks = set()
south_end = 0
east_end = 0


def spin(prev_r: frozenset[complex]):
    eastl = [set() for _ in range(south_end)]
    for old in prev_r:
        eastl[int(old.real)].add(old)
    northl = [set() for _ in range(east_end + 1)]
    for olds in eastl:
        for old in olds:
            while old.real > 0 and old - 1 not in s_rocks and old - 1 not in northl[int(old.imag)]:
                old -= 1
            northl[int(old.imag)].add(old)
    for x in eastl:
        x.clear()
    for olds in northl:
        for old in olds:
            while old.imag > 0 and old - 1j not in s_rocks and old - 1j not in eastl[int(old.real)]:
                old -= 1j
            eastl[int(old.real)].add(old)
    for x in northl:
        x.clear()
    for olds in eastl[::-1]:
        for old in olds:
            while old.real < south_end - 1 and old + 1 not in s_rocks and old + 1 not in northl[int(old.imag)]:
                old += 1
            northl[int(old.imag)].add(old)
    east = set[complex]()
    for olds in northl[::-1]:
        for old in olds:
            while old.imag < east_end and old + 1j not in s_rocks and old + 1j not in east:
                old += 1j
            east.add(old)
    return frozenset(east)

r_rocks = set()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for row, line in enumerate(f.readlines()):
        south_end += 1
        east_end = len(line.strip()) - 1
        for col, c in enumerate(line.strip()):
            if c == "#":
                s_rocks.add(row + col*1j)
            if c == "O":
                p = row + col * 1j
                r_rocks.add(p)


r_rocks = frozenset(r_rocks)
loop = [r_rocks]
n = None
while (n := spin(loop[-1])) not in loop:
    loop.append(n)
print("done")
loop_start = loop.index(n)
idx = loop_start + (1000000000 - loop_start) % (len(loop) - loop_start)
print(loop_start, len(loop))
print(sum(south_end-p.real for p in loop[idx]))
