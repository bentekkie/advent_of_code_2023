import pathlib
import os
from functools import cache

THIS_DIR = pathlib.Path(__file__).parent.resolve()


@cache
def combs(line: str, sizes: tuple[int, ...]):
    if len(line) == 0:
        return len(sizes) == 0
    elif line[0] == "#":
        if len(sizes) > 0 and len(line) >= sizes[0] and not line[: sizes[0]].count("."):
            if len(line) > sizes[0] and line[sizes[0]] in ".?":
                return combs(line[sizes[0] + 1 :], sizes[1:])
            elif len(line) == sizes[0] and len(sizes) == 1:
                return 1
        return 0
    elif line[0] == "?":
        if len(sizes) == 0:
            return combs(line[1:], sizes)
        elif len(line) >= sizes[0] and not line[: sizes[0]].count("."):
            if len(line) > sizes[0]:
                if line[sizes[0]] == "#":
                    return combs(line[1:], sizes)
                else:
                    return combs(line[sizes[0] + 1 :], sizes[1:]) + combs(
                        line[1:], sizes
                    )
            elif len(sizes) == 1:
                return 1 + combs(line[1:], sizes)
            return 0
        elif len(line) > sizes[0]:
            return combs(line[1:], sizes)
        return 0
    else:
        return combs(line[1:], sizes)


s = 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for full_line in f.readlines():
        line, raw_sizes = full_line.strip().split(" ")
        sizes = [int(x) for x in raw_sizes.split(",")]
        s += combs(line, sizes)

print(s)
