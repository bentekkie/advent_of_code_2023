import pathlib
import os
from collections import defaultdict

THIS_DIR = pathlib.Path(__file__).parent.resolve()

start = (0, 0)
neighbors = defaultdict(set)
grid = dict()
outside = set()
cols, rows = 0, 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for row, line in enumerate(f.readlines()):
        rows += 1
        cols = len(line.strip())
        for col, c in enumerate(line.strip()):
            curr = (row, col)
            grid[curr] = c
            if c == "S":
                start = curr
            if c in "|LJ":
                neighbors[(row - 1, col)].add(curr)
            if c in "|7F":
                neighbors[(row + 1, col)].add(curr)
            if c in "-J7":
                neighbors[(row, col - 1)].add(curr)
            if c in "-LF":
                neighbors[(row, col + 1)].add(curr)


sns = sorted(neighbors[start], key=lambda x: x[0])
if sns[0][0] == sns[0][1]:
    grid[start] = "-"
elif sns[0][1] == sns[0][1]:
    grid[start] = "|"
elif sns[0][1] < start[1]:
    grid[start] = "7"
elif sns[0][1] > start[1]:
    grid[start] = "F"
elif sns[0][0] < start[0]:
    grid[start] = "L"
else:
    grid[start] = "J"


def far(start):
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


def is_out_of_bounds(p):
    return p[0] <= 0 or p[1] <= 0 or p[0] >= rows or p[1] >= cols


def grid_ns(p):
    return {
        (p[0] - 0.5, p[1]),
        (p[0] + 0.5, p[1]),
        (p[0], p[1] - 0.5),
        (p[0], p[1] + 0.5),
    }


def filled(path: set[tuple[int, int]]):
    out = set()
    for p in path:
        if grid[p] != ".":
            out.add(p)
        if grid[p] in "|LJ":
            out.add((p[0] - 0.5, p[1]))
        if grid[p] in "|7F":
            out.add((p[0] + 0.5, p[1]))
        if grid[p] in "-J7":
            out.add((p[0], p[1] - 0.5))
        if grid[p] in "-LF":
            out.add((p[0], p[1] + 0.5))
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
