import pathlib
import os
from dataclasses import dataclass, replace


THIS_DIR = pathlib.Path(__file__).parent.resolve()


rocks = set[complex]()
start = 0
last_row = 0
last_col = 0



with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for row, line in enumerate(f.readlines()):
        last_row = row
        last_col = len(line.strip()) - 1
        for col, c in enumerate(line.strip()):
            if c == "#":
                rocks.add(row + col * 1j)
            if c == "S":
                start = row + col * 1j

def neighbors(pos: complex):
    if pos.real > 0:
        yield pos - 1
    if pos.imag > 0:
        yield pos - 1j
    if pos.real < last_row:
        yield pos + 1
    if pos.real < last_col:
        yield pos + 1j


def step(curr_pos : set[complex]):
    return {n for p in curr_pos for n in neighbors(p) if n not in rocks}


curr = {start}
for i in range(64):
    curr = step(curr)
print(len(curr))