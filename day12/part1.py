import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def combs(line, sizes, curr=""):
    if len(line) == 0:
        if len(sizes) == 0:
            yield ""
    elif line[0] == "#":
        if (
            len(sizes) > 0
            and len(line) >= sizes[0]
            and all(c != "." for c in line[: sizes[0]])
        ):
            if len(line) > sizes[0] and line[sizes[0]] in ".?":
                yield from (
                    ("#" * sizes[0]) + "." + rest
                    for rest in combs(
                        line[sizes[0] + 1 :], sizes[1:], curr + ("#" * sizes[0]) + "."
                    )
                )
            elif len(line) == sizes[0] and len(sizes) == 1:
                yield "#" * sizes[0]
    elif line[0] == "?":
        if len(sizes) == 0:
            yield from ("." + rest for rest in combs(line[1:], sizes, curr + "."))
        elif len(line) >= sizes[0] and all(c != "." for c in line[: sizes[0]]):
            if len(line) > sizes[0]:
                if line[sizes[0]] == "#":
                    # print('.', line, sizes)
                    yield from (
                        "." + rest for rest in combs(line[1:], sizes, curr + ".")
                    )
                else:
                    # print('apply', line, sizes)
                    yield from (
                        ("#" * sizes[0]) + "." + rest
                        for rest in combs(
                            line[sizes[0] + 1 :],
                            sizes[1:],
                            curr + ("#" * sizes[0] + "."),
                        )
                    )
                    yield from (
                        "." + rest for rest in combs(line[1:], sizes, curr + ".")
                    )
            elif len(sizes) == 1:
                yield "#" * sizes[0]
                yield from ("." + rest for rest in combs(line[1:], sizes))
        elif len(line) > sizes[0]:
            yield from ("." + rest for rest in combs(line[1:], sizes))
    else:
        yield from (line[0] + rest for rest in combs(line[1:], sizes))


s = 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for full_line in f.readlines():
        line, raw_sizes = full_line.strip().split(" ")
        sizes = [int(x) for x in raw_sizes.split(",")]
        s += sum(1 for x in combs(line, sizes))

print(s)
