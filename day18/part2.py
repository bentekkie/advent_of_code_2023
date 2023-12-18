import pathlib
import os
from shapely import Polygon

THIS_DIR = pathlib.Path(__file__).parent.resolve()

x, y = 0, 0
points: list[tuple[int, int]] = [(x, y)]
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        _, _, hex_raw = line.strip().split()
        hex_raw = hex_raw.removeprefix("(#").removesuffix(")")
        dist = int(hex_raw[:5], base=16)
        direction = hex_raw[5]
        if direction == "0":
            x += dist
        elif direction == "2":
            x -= dist
        elif direction == "1":
            y += dist
        elif direction == "3":
            y -= dist
        else:
            print("parse error", line)
        points.append((x, y))
p = Polygon(points)
print(p.area + p.length / 2 + 1)
