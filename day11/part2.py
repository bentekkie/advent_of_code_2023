import pathlib
import os
from collections import defaultdict
from itertools import combinations
from typing import Iterable, TypeVar

THIS_DIR = pathlib.Path(__file__).parent.resolve()
scale = 1000000


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def enumerate_2d(grid: Iterable[Iterable]):
    for r, row in enumerate(grid):
        for c, entry in enumerate(row):
            yield r, c, entry


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    grid = [l.strip() for l in f.readlines()]
    ers = [r for r, line in enumerate(grid) if not line.count("#")]
    ecs = [c for c, line in enumerate(zip(*grid)) if not line.count("#")]
    print(
        sum(
            map(
                dist,
                *zip(
                    *combinations(
                        (
                            (
                                r + (scale - 1) * sum(er < r for er in ers),
                                c + (scale - 1) * sum(ec < c for ec in ecs),
                            )
                            for r, c, e in enumerate_2d(grid)
                            if e == "#"
                        ),
                        2,
                    )
                )
            )
        )
    )
