import pathlib
import os
from functools import cache
from collections import defaultdict

THIS_DIR = pathlib.Path(__file__).parent.resolve()


branch = defaultdict(int)


@cache
def combs(line: str, sizes: tuple[int, ...]):
    if len(line) == 0:
        branch["a"] += 1
        return len(sizes) == 0
    elif len(sizes) == 0:
        branch["b"] += 1
        return "#" not in line
    elif line[0] == "#":
        if len(line) >= sizes[0] and "." not in line[: sizes[0]]:
            if len(line) > sizes[0] and line[sizes[0]] != "#":
                branch["c"] += 1
                return combs(line[sizes[0] + 1 :], sizes[1:])
            branch["d"] += 1
            return len(line) == sizes[0] and len(sizes) == 1
    elif line[0] == "?":
        if len(line) >= sizes[0] and "." not in line[: sizes[0]]:
            if len(line) > sizes[0]:
                branch["e"] += 1
                return combs(line[1:], sizes) + (
                    0
                    if line[sizes[0]] == "#"
                    else combs(line[sizes[0] + 1 :], sizes[1:])
                )
            branch["f"] += 1
            return len(sizes) == 1
        elif len(line) > sizes[0]:
            branch["g"] += 1
            return combs(line[1:], sizes)
    else:
        branch["h"] += 1
        return combs(line[1:], sizes)
    branch["i"] += 1
    return 0


s = 0

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for full_line in f.readlines():
        line, raw_sizes = full_line.strip().split(" ")
        line = "?".join([line, line, line, line, line])
        raw_sizes = ",".join([raw_sizes, raw_sizes, raw_sizes, raw_sizes, raw_sizes])
        sizes = tuple(int(x) for x in raw_sizes.split(","))
        s += combs(line, sizes)

print(s)
print(branch)
print(combs.cache_info())
