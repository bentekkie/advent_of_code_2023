import pathlib
import os
from dataclasses import dataclass
from functools import cached_property, cache
from networkx import DiGraph, descendants, all_simple_paths
from collections import defaultdict
from itertools import combinations, permutations


THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass
class Block:
    bid: int
    coords: tuple[tuple[int, int, int], tuple[int, int, int]]
    curr_z_min: int

    @property
    def z_dist(self):
        return abs(self.coords[0][2] - self.coords[1][2])

    @property
    def z_min(self):
        return self.curr_z_min

    @property
    def z_max(self):
        return self.curr_z_min + self.z_dist

    @cached_property
    def x_min(self):
        return min(self.coords[0][0], self.coords[1][0])

    @cached_property
    def x_max(self):
        return max(self.coords[0][0], self.coords[1][0])

    @cached_property
    def y_min(self):
        return min(self.coords[0][1], self.coords[1][1])

    @cached_property
    def y_max(self):
        return max(self.coords[0][1], self.coords[1][1])


block_by_id: dict[int, Block] = {}


@cache
def intersecting_blocks(a):
    return [b for b in block_by_id.keys() if a != b and xy_intersects(a, b)]


@cache
def xy_intersects(a_id: int, b_id: int):
    a = block_by_id[a_id]
    b = block_by_id[b_id]
    return intersects(a.x_min, a.x_max, b.x_min, b.x_max) and intersects(
        a.y_min, a.y_max, b.y_min, b.y_max
    )


def intersects(a_min: int, a_max: int, b_min: int, b_max: int):
    return (
        a_min <= b_min <= a_max
        or a_min <= b_max <= a_max
        or (b_min <= a_min and a_max <= b_max)
    )


def parse_coord(s: str):
    p0, p1, p2 = s.split(",")
    return (int(p0), int(p1), int(p2))


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for row, line in enumerate(f.readlines()):
        p0, p1 = line.strip().split("~")
        c0, c1 = parse_coord(p0), parse_coord(p1)
        block_by_id[row] = Block(row, (c0, c1), min(c0[2], c1[2]))


brick_order = sorted(block_by_id, key=lambda b: block_by_id[b].z_min)
for i, brick in enumerate(brick_order):
    block_by_id[brick].curr_z_min = (
        max(
            (block_by_id[b].z_max for b in brick_order[:i] if xy_intersects(brick, b)),
            default=0,
        )
        + 1
    )


supporting = {
    a: [
        b
        for b in block_by_id
        if a != b
        and xy_intersects(a, b)
        and block_by_id[a].z_max + 1 == block_by_id[b].z_min
    ]
    for a in block_by_id
}

ground = "ground"
g = DiGraph()

for b in block_by_id:
    if block_by_id[b].z_min == 1:
        g.add_edge(ground, b)
    for c in supporting[b]:
        g.add_edge(b, c)

paths: dict[int, set] = {}
for path in all_simple_paths(g, ground, block_by_id):
    if path[-1] in paths:
        paths[path[-1]].intersection_update(path)
    else:
        paths[path[-1]] = set(path)
print(sum(b in paths[c] for b, c in permutations(block_by_id, 2)))
