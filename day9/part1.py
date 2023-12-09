import pathlib
import os
from collections import Counter
from functools import cached_property, cache
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def extrapolate(seq: list[int]):
    if all(x == 0 for x in seq):
        return 0
    else:
        return seq[-1] + extrapolate([seq[i + 1] - seq[i] for i in range(len(seq) - 1)])


s = 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        seq = [int(x) for x in line.strip().split()]
        s += extrapolate(seq)

print(s)
