import pathlib
import os
from dataclasses import dataclass
from functools import cached_property, cache


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
for brick in brick_order:
    block_by_id[brick].curr_z_min = (
        max(
            (
                block_by_id[b].z_max
                for b in intersecting_blocks(brick)
                if block_by_id[b].z_min < block_by_id[brick].z_min
            ),
            default=0,
        )
        + 1
    )


supporting = {b: [] for b in block_by_id}
supported_by = {b: [] for b in block_by_id}
for brick in brick_order:
    for b in intersecting_blocks(brick):
        if block_by_id[b].z_max + 1 == block_by_id[brick].z_min:
            supporting[b].append(brick)
            supported_by[brick].append(b)

print(sum(all(len(supported_by[c]) - 1 for c in supporting[b]) for b in block_by_id))
