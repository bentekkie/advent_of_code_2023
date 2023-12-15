import pathlib
import os
import cmath
from functools import cache, cached_property
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def hash_step(step: str):
    curr = 0
    for c in step:
        curr += ord(c)
        curr *= 17
        curr %= 256
    return curr


@dataclass
class Lense:
    label: str
    focal: int

    def __eq__(self, value: "Lense") -> bool:
        return self.label == value.label

    @cached_property
    def h(self):
        return hash_step(self.label)


boxes: list[list[Lense]] = [[] for _ in range(256)]

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    raw = f.read()
    steps = raw.strip().split(",")
    for step in steps:
        if "=" in step:
            label, raw_val = step.split("=")
            l = Lense(label, int(raw_val))
            try:
                boxes[l.h][boxes[l.h].index(l)] = l
            except ValueError:
                boxes[l.h].append(l)
        else:
            l = Lense(step[:-1], 0)
            try:
                boxes[l.h].remove(l)
            except ValueError:
                pass

s = 0
for i, box in enumerate(boxes):
    for j, l in enumerate(box):
        s += (i + 1) * (j + 1) * l.focal

print(s)
