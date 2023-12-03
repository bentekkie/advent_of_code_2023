import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()

fixdict = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def all_nums(line: str):
    nums = []
    for i, c in enumerate(line):
        if c.isdigit():
            nums.append(c)
        for s, d in fixdict.items():
            if line[i:].startswith(s):
                nums.append(d)
    return nums


s = 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        nums = all_nums(line)
        s += int(nums[0] + nums[-1])

print(s)
