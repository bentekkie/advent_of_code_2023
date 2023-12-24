import pathlib
import os
from networkx import DiGraph, all_simple_paths


THIS_DIR = pathlib.Path(__file__).parent.resolve()

g = DiGraph()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    grid = [line.strip() for line in f.readlines()]

    for row, line in enumerate(grid):
        for col, c in enumerate(line):
            if c == ">":
                g.add_edge((row, col), (row, col + 1))
            if c == "<":
                g.add_edge((row, col), (row, col - 1))
            if c == "^":
                g.add_edge((row, col), (row - 1, col))
            if c == "v":
                g.add_edge((row, col), (row + 1, col))
            if c == ".":
                if col + 1 < len(grid[row]) and grid[row][col + 1] != "#":
                    g.add_edge((row, col), (row, col + 1))
                if col - 1 >= 0 and grid[row][col - 1] != "#":
                    g.add_edge((row, col), (row, col - 1))
                if row - 1 >= 0 and grid[row - 1][col] != "#":
                    g.add_edge((row, col), (row - 1, col))
                if row + 1 < len(grid) and grid[row + 1][col] != "#":
                    g.add_edge((row, col), (row + 1, col))


print(
    max(
        len(p) - 1
        for p in all_simple_paths(g, (0, 1), (len(grid) - 1, len(grid[0]) - 2))
    )
)
