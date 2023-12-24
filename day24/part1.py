import pathlib
import os
from dataclasses import dataclass
from itertools import combinations


THIS_DIR = pathlib.Path(__file__).parent.resolve()


def intersect(
    x0_a: int,
    y0_a: int,
    vx_a: int,
    vy_a: int,
    x0_b: int,
    y0_b: int,
    vx_b: int,
    vy_b: int,
):
    if vy_a / vx_a == vy_b / vx_b:
        return "par", 0, 0
    x = (-(vy_b / vx_b) * x0_b + y0_b + (vy_a / vx_a) * x0_a - y0_a) / (
        vy_a / vx_a - vy_b / vx_b
    )
    y = (vy_a / vx_a) * x - (vy_a / vx_a) * x0_a + y0_a
    if (
        (x < x0_a) != (vx_a < 0)
        or (y < y0_a) != (vy_a < 0)
        or (x < x0_b) != (vx_b < 0)
        or (y < y0_b) != (vy_b < 0)
    ):
        return "past", x, y
    return "inter", x, y


@dataclass(frozen=True)
class Hailstone:
    x0: int
    y0: int
    z0: int
    vx: int
    vy: int
    vz: int


hailstones: list[Hailstone] = []

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        ps, vs = line.strip().split(" @ ")
        ps = [int(p) for p in ps.split(", ")]
        vs = [int(p) for p in vs.split(", ")]
        hailstones.append(Hailstone(ps[0], ps[1], ps[2], vs[0], vs[1], vs[2]))

tmin, tmax = 200000000000000, 400000000000000

s = 0
for a, b in combinations(hailstones, 2):
    t, x, y = intersect(a.x0, a.y0, a.vx, a.vy, b.x0, b.y0, b.vx, b.vy)
    if t == "inter" and tmin <= x <= tmax and tmin <= y <= tmax:
        s += 1

print(s)
