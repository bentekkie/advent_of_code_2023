import pathlib
import os
from dataclasses import dataclass
from math import sqrt, floor, ceil, prod

THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass
class Record:
    time: int
    distance: int


def find_roots(rec: Record):
    a = 1
    b = -rec.time
    c = rec.distance
    d = (b**2) - (4 * a * c)
    return (-b - sqrt(d)) / 2 * a, (-b + sqrt(d)) / 2 * a


def num_sols(rec: Record):
    roota, rootb = find_roots(rec)
    return floor(rootb) - floor(roota) + (rootb.is_integer() * -1)


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    raw = f.readlines()
    times = raw[0].removeprefix("Time:").strip().split()

    distances = raw[1].removeprefix("Distance:").strip().split()
    records = [Record(int(t), int(d)) for t, d in zip(times, distances)]
    sols = [num_sols(r) for r in records]
    print(prod(sols))
