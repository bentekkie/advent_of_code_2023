import pathlib
import os
from collections import defaultdict
import cmath

THIS_DIR = pathlib.Path(__file__).parent.resolve()

start = 0
neighbors = defaultdict[complex, set[complex]](set)
grid = dict[complex, str]()
cols, rows = 0, 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for row, line in enumerate(f.readlines()):
        rows += 1
        cols = len(line.strip())
        for col, c in enumerate(line.strip()):
            curr = complex(row, col)
            grid[curr] = c
            if c == "S":
                start = curr
            if c in "|LJ":
                neighbors[curr - 1].add(curr)
            if c in "|7F":
                neighbors[curr + 1].add(curr)
            if c in "-J7":
                neighbors[curr - 1j].add(curr)
            if c in "-LF":
                neighbors[curr + 1j].add(curr)


sns = sorted(neighbors[start], key=lambda x: x.real)
if sns[0].real == sns[1].real:
    grid[start] = "-"
elif sns[0].imag == sns[0].imag:
    grid[start] = "|"
elif sns[0].imag < start.imag:
    grid[start] = "7"
elif sns[0].imag > start.imag:
    grid[start] = "F"
elif sns[0].real < start.real:
    grid[start] = "L"
else:
    grid[start] = "J"


def far(start: complex):
    seen = {start}
    to_check = neighbors[start]
    seen.update(to_check)
    while len(to_check) > 0:
        seen.update(
            to_check := {
                n for p in to_check for n in (neighbors[p] - seen) if p in neighbors[n]
            }
        )
    return seen


def is_out_of_bounds(p: complex):
    return p.real <= 0 or p.imag <= 0 or p.real >= rows or p.imag >= cols


def grid_ns(p: complex):
    return {
        p - 0.5,
        p + 0.5,
        p - 0.5j,
        p + 0.5j,
    }


def filled(path: set[complex]):
    out = set()
    for p in path:
        if grid[p] != ".":
            out.add(p)
        if grid[p] in "|LJ":
            out.add(p - 0.5)
        if grid[p] in "|7F":
            out.add(p + 0.5)
        if grid[p] in "-J7":
            out.add(p - 0.5j)
        if grid[p] in "-LF":
            out.add(p + 0.5j)
    return out


path = far(start)
filled_poses = filled(path)
s = 0
outside = set()
inside = set()
for p in grid:
    if p not in path:
        to_check = {p}
        checked = set()
        is_outside = False
        while len(to_check) > 0 and not is_outside:
            if len(to_check & outside) > 0 or any(map(is_out_of_bounds, to_check)):
                is_outside = True
                break
            if len(to_check & inside) > 0:
                break
            checked.update(to_check)
            to_check = set.union(*map(grid_ns, to_check)) - filled_poses - checked
        if is_outside:
            outside.update(checked)
        else:
            s += 1
            inside.update(checked)
print(s)
