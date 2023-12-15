import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def hash_step(step: str):
    curr = 0
    for c in step:
        curr += ord(c)
        curr *= 17
        curr %= 256
    return curr


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    print(sum(hash_step(s) for s in f.read().strip().split(",")))
