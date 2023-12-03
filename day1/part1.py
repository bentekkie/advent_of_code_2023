import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def first_num(line: str):
    for c in line:
        if c.isdigit():
            return c


def last_num(line: str):
    for c in line[::-1]:
        if c.isdigit():
            return c


s = 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        s += int(first_num(line) + last_num(line))

print(s)
