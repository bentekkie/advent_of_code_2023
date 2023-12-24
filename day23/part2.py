import pathlib
import os
from networkx import Graph, all_simple_edge_paths


THIS_DIR = pathlib.Path(__file__).parent.resolve()

g = Graph()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    grid = [line.strip() for line in f.readlines()]
    for row, line in enumerate(grid):
        for col, c in enumerate(line):
            if c != "#":
                if col + 1 < len(grid[row]) and grid[row][col + 1] != "#":
                    g.add_edge((row, col), (row, col + 1))
                if col - 1 >= 0 and grid[row][col - 1] != "#":
                    g.add_edge((row, col), (row, col - 1))
                if row - 1 >= 0 and grid[row - 1][col] != "#":
                    g.add_edge((row, col), (row - 1, col))
                if row + 1 < len(grid) and grid[row + 1][col] != "#":
                    g.add_edge((row, col), (row + 1, col))
sg = Graph()


def visit(last_intersection: tuple[int, int], curr: tuple[int, int]):
    seen = {last_intersection}
    ns = list(g.neighbors(curr))
    while len(ns) == 2:
        seen.add(curr)
        curr = next(n for n in ns if n not in seen)
        ns = list(g.neighbors(curr))
    already_processed_curr = sg.has_node(curr)
    sg.add_edge(last_intersection, curr, weight=len(seen))
    if not already_processed_curr:
        for n in ns:
            if n not in seen:
                visit(curr, n)


visit((0, 1), (1, 1))
print(
    max(
        sum(sg.get_edge_data(*e)["weight"] for e in p)
        for p in all_simple_edge_paths(sg, (0, 1), (len(grid) - 1, len(grid[0]) - 2))
    )
)
