import pathlib
import os
from collections import defaultdict
from dataclasses import dataclass
from math import lcm
from typing import Iterable


THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass
class FlipFlop:
    children: list[str]
    mem: bool = False

    def process(self, p: str, pulse: bool) -> Iterable[tuple[str, bool]]:
        if not pulse:
            self.mem = not self.mem
            return ((c, self.mem) for c in self.children)
        return iter(())


@dataclass
class Conjunction:
    children: list[str]
    parents: dict[str, bool]

    def process(self, p: str, pulse: bool):
        self.parents[p] = pulse
        res = not all(self.parents.values())
        return ((c, res) for c in self.children)


@dataclass
class Broadcast:
    children: list[str]

    def process(self, p: str, pulse: bool):
        return ((c, pulse) for c in self.children)


children = dict[str, list[str]]()
parents = defaultdict(list[str])
broadcast = "broadcaster"
flip_flops = list[str]()
conjunctions = list[str]()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        f, t = line.strip().split(" -> ")
        if f.startswith("%"):
            f = f.removeprefix("%")
            flip_flops.append(f)
        if f.startswith("&"):
            f = f.removeprefix("&")
            conjunctions.append(f)
        children[f] = [s.strip() for s in t.split(",")]
        for c in children[f]:
            parents[c].append(f)

all_nodes = (
    {broadcast: Broadcast(children[broadcast])}
    | {n: FlipFlop(children[n]) for n in flip_flops}
    | {
        n: Conjunction(children[n], {p: False for p in parents[n]})
        for n in conjunctions
    }
)


def push_button(ps):
    to_process = [("button", broadcast, False)]
    c_highs: set[str] = set()
    while to_process:
        c_highs.update(f for f, _, p in to_process if p and f in ps)
        to_process = [
            (d, nd, np)
            for f, d, p in to_process
            for nd, np in all_nodes[d].process(f, p)
            if nd in all_nodes
        ]
    return c_highs


def find_min(ps: set[str]):
    pushes = 0
    while ps:
        pushes += 1
        if not ps.isdisjoint(c_high := push_button(ps)):
            print(pushes)
            print(bin(pushes))
            yield pushes
        ps = ps - c_high


print(lcm(*find_min(set(parents[parents["rx"][0]]))))
