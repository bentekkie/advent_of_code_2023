import pathlib
import os
from shapely import Polygon, Point, BufferCapStyle

THIS_DIR = pathlib.Path(__file__).parent.resolve()

x, y = 0, 0
points: list[tuple[int, int]] = [(x, y)]
min_x, max_x = 0,0
min_y,max_y = 0,0
with open(os.path.join(THIS_DIR, "example.txt")) as f:
    for line in f.readlines():
        direction, dist_raw, _ = line.strip().split()
        dist = int(dist_raw)
        if direction == "R":
            x += dist
        elif direction == "L":
            x -= dist
        elif direction == "D":
            y += dist
        elif direction == "U":
            y -= dist
        else:
            print("parse error", line)
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
        points.append((x, y))
p = Polygon(points)
print(p.area + p.length / 2 + 1)