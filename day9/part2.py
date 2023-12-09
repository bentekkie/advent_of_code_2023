import pathlib
import os
from operator import sub

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def extrap(s: list[int]):
    return 0 if not any(s) else s[0] - extrap(list(map(sub, s[1:], s)))


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    print(sum(extrap([int(x) for x in line.strip().split()]) for line in f.readlines()))
