import pathlib
import os
from functools import cached_property
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
    for step in f.read().strip().split(","):
        if "=" in step:
            label, raw_val = step.split("=")
            val = int(raw_val)
            h = hash_step(label)
            for x in boxes[h]:
                if x.label == label:
                    x.focal = val
                    break
            else:
                boxes[h].append(Lense(label, val))
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
