import pathlib
import os
import cmath
from functools import cache

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def hash_step(step: str):
    curr = 0
    for c in step:
        curr += ord(c)
        curr *= 17
        curr %= 256
    return curr


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    raw = f.read()
    steps = raw.strip().split(",")
    print(sum(hash_step(s) for s in steps))
print("rm-"[:-1])
