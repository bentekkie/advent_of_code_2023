import pathlib
import os
from collections import Counter
from functools import cached_property
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()


def run_path(start, end, graph, instructions):
    steps = 0
    curr = start
    while curr != end:
        if instructions[(steps % len(instructions))] == "L":
            curr = graph[curr][0]
        else:
            curr = graph[curr][1]
        steps += 1
    return steps


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    lines = f.readlines()
    instructions = lines[0].strip()

    graph = {}
    for line in lines[2:]:
        s, to = line.strip().split(" = ")
        l, r = to[1:-1].split(", ")
        graph[s] = (l, r)

print(run_path("AAA", "ZZZ", graph, instructions))
