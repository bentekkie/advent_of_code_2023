#%%
import pathlib
import os
from shapely import Polygon
from shapely.plotting import plot_polygon

THIS_DIR = pathlib.Path(__file__).parent.resolve()

x, y = 0, 0
points: list[tuple[int, int]] = [(x, y)]
with open(os.path.join(THIS_DIR, "input.txt")) as f:
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
        points.append((x, y))
p = Polygon(points)
print(p.area + p.length / 2 + 1)
plot_polygon(p, add_points=False)
# %%
