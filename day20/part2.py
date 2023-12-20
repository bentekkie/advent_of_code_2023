import pathlib
import os
from dataclasses import dataclass, field
from enum import Enum
from math import lcm


THIS_DIR = pathlib.Path(__file__).parent.resolve()

children: dict[str, list[str]] = {}
broadcast = "broadcaster"
flip_flops: list[str] = []
conjunctions: list[str] = []

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
all_children = {c for cs in children.values() for c in cs}
parents = {f: [p for p, cs in children.items() if f in cs] for f in all_children}


@dataclass
class FlipFlop:
    children: list[str]
    mem: bool = False

    def process(self, p: str, pulse: bool):
        if not pulse:
            self.mem = not self.mem
            return [(c, self.mem) for c in self.children]
        return []


@dataclass
class Conjunction:
    children: list[str]
    parents: dict[str, bool]
    mem: bool = False

    def process(self, p: str, pulse: bool):
        self.parents[p] = pulse
        res = not all(self.parents.values())
        return [(c, res) for c in self.children]


@dataclass
class Broadcast:
    children: list[str]

    def process(self, p: str, pulse: bool):
        return [(c, pulse) for c in self.children]


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
    c_highs = set()
    while len(to_process) > 0:
        new_to_process = []
        for f, dest, pulse in to_process:
            if f in ps and pulse:
                c_highs.add(f)
            for new_dest, new_pulse in all_nodes[dest].process(f, pulse):
                if new_dest in all_nodes:
                    new_to_process.append((dest, new_dest, new_pulse))
        to_process = new_to_process
    return c_highs

pushes = 0
periods = {p: 0 for p in parents[parents["rx"][0]]}
while not all(periods.values()):
    pushes += 1
    c_high = push_button(periods.keys())
    for p, v in periods.items():
        if v == 0 and p in c_high:
            periods[p] = pushes

print(lcm(*periods.values()))
