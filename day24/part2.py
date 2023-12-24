import pathlib
import os
from dataclasses import dataclass

from sympy import solve, symbols
from time import time


THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass(frozen=True)
class Hailstone:
    x0: int
    y0: int
    z0: int
    vx: int
    vy: int
    vz: int


hailstones: list[Hailstone] = []


me_x0 = symbols("me_x0", integer=True)
me_y0 = symbols("me_y0", integer=True)
me_z0 = symbols("me_z0", integer=True)
me_vx = symbols("me_vx", integer=True)
me_vy = symbols("me_vy", integer=True)
me_vz = symbols("me_vz", integer=True)

eqs = []

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        ps, vs = [[int(p) for p in ps.split(", ")] for ps in line.strip().split(" @ ")]
        eqs.append(
            (ps[0] - me_x0) / (me_vx - vs[0]) - (ps[1] - me_y0) / (me_vy - vs[1])
        )
        eqs.append(
            (ps[0] - me_x0) / (me_vx - vs[0]) - (ps[2] - me_z0) / (me_vz - vs[2])
        )

res = solve(eqs, [me_x0, me_y0, me_z0, me_vx, me_vy, me_vz], dict=True, check=False)
print(res[0][me_x0] + res[0][me_y0] + res[0][me_z0])
