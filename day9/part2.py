import pathlib
import os
from collections import Counter
from functools import cached_property, cache
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def extrap(seq: list[int]):
    return 0 if not any(seq) else seq[0] - extrap([n - c for c, n in zip(seq, seq[1:])])


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    print(sum(extrap([int(x) for x in line.strip().split()]) for line in f.readlines()))
