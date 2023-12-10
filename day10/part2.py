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


def far(start):
    seen = {start}
    to_check = neighbors[start]
    seen.update(to_check)
    steps = 1
    while True:
        steps += 1
        next_check = {
            n
            for p in to_check
            for n in neighbors[p]
            if n not in seen and p in neighbors[n]
        }
        seen.update(next_check)
        if len(next_check) == 1:
            return seen

        to_check = next_check


path = far(start)

start_c = ""
sns = sorted(neighbors[start], key=lambda x: x[0])
if sns[0][0] == sns[0][1]:
    start_c = "-"
elif sns[0][1] == sns[0][1]:
    start_c = "|"
elif sns[0][1] < start[1]:
    start_c = "7"
elif sns[0][1] > start[1]:
    start_c = "F"
elif sns[0][0] < start[0]:
    start_c = "L"
else:
    start_c = "J"


def grid_ns(p):
    yield (p[0] - 0.5, p[1])
    yield (p[0] + 0.5, p[1])
    yield (p[0], p[1] - 0.5)
    yield (p[0], p[1] + 0.5)


def filled(path: set[tuple[int, int]]):
    out = set()
    for p in path:
        c = grid[p] if p != start else start_c
        if c != ".":
            out.add(p)
        if c in "|LJ":
            out.add((p[0] - 0.5, p[1]))
        if c in "|7F":
            out.add((p[0] + 0.5, p[1]))
        if c in "-J7":
            out.add((p[0], p[1] - 0.5))
        if c in "-LF":
            out.add((p[0], p[1] + 0.5))
    return out


filled_poses = filled(path)
s = 0
outside = set.union(
    {(x, 0) for x in range(rows)},
    {(x, cols) for x in range(rows)},
    {(0, x) for x in range(cols)},
    {(rows, x) for x in range(cols)},
)
inside = set()
for p in grid:
    if p not in path:
        to_check = {p}
        checked = set()
        is_outside = False
        while len(to_check) > 0 and not is_outside:
            new_to_check = set()
            for q in to_check:
                checked.add(q)
                if q in outside:
                    is_outside = True
                elif q in inside:
                    break
                else:
                    new_to_check.update(
                        n
                        for n in grid_ns(q)
                        if n not in filled_poses and n not in checked
                    )
            to_check = new_to_check
        if is_outside:
            outside.update(checked)
        else:
            s += 1
            inside.update(checked)
print(s)
