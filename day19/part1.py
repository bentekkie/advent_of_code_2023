import pathlib
import os
from dataclasses import dataclass, replace


THIS_DIR = pathlib.Path(__file__).parent.resolve()

rules = {}


@dataclass(frozen=True)
class State:
    x_min: int = 0
    x_max: int = 4001
    m_min: int = 0
    m_max: int = 4001
    a_min: int = 0
    a_max: int = 4001
    s_min: int = 0
    s_max: int = 4001

    def count(self):
        return (
            (self.x_max - self.x_min - 1)
            * (self.m_max - self.m_min - 1)
            * (self.a_max - self.a_min - 1)
            * (self.s_max - self.s_min - 1)
        )

    def valid(self):
        return self.count() > 0

    def apply(self, v, dir, bound):
        if dir == "<":
            return replace(
                self, **{f"{v}_max": min(self.__dict__[f"{v}_max"], bound)}
            ), replace(self, **{f"{v}_min": max(self.__dict__[f"{v}_min"], bound - 1)})
        else:
            return replace(
                self, **{f"{v}_min": max(self.__dict__[f"{v}_min"], bound)}
            ), replace(self, **{f"{v}_max": min(self.__dict__[f"{v}_max"], bound + 1)})

    def contains(self, x, m, a, s):
        return (
            self.x_min < x < self.x_max
            and self.m_min < m < self.m_max
            and self.a_min < a < self.a_max
            and self.s_min < s < self.s_max
        )


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    raw_rules = []
    raw_inputs: list[str] = []
    curr = raw_rules

    for row, line in enumerate(f.readlines()):
        if line.strip() == "":
            curr = raw_inputs
        else:
            curr.append(line.strip())

for rule in raw_rules:
    name, rest = rule.split("{")
    conds = []
    d = ""
    for part in rest[:-1].split(","):
        if ":" in part:
            cond, res = part.split(":")
            conds.append((cond[0], cond[1], int(cond[2:]), res))
        else:
            d = part
    rules[name] = (conds, d)

to_check = [("in", State())]
accepted = []

while len(to_check) > 0:
    new_to_check = []
    for curr, s in to_check:
        if curr == "A":
            accepted.append(s)
        elif curr != "R":
            conds, d = rules[curr]
            for v, dir, bound, res in conds:
                if not s.valid():
                    continue
                y, s = s.apply(v, dir, bound)
                if y.valid():
                    new_to_check.append((res, y))
            else:
                if s.valid():
                    new_to_check.append((d, s))
    to_check = new_to_check
total = 0
for raw_rating in raw_inputs:
    x, m, a, s = [
        int(t)
        for t in raw_rating.removeprefix("{x=")
        .removesuffix("}")
        .replace("m=", "")
        .replace("a=", "")
        .replace("s=", "")
        .split(",")
    ]
    if any(state.contains(x, m, a, s) for state in accepted):
        total += x + m + a + s
print(total)
