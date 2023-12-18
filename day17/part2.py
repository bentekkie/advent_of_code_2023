import pathlib
import os
from dijkstar import Graph, find_path

THIS_DIR = pathlib.Path(__file__).parent.resolve()


g = Graph()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    grid = [[int(c) for c in line.strip()] for line in f.readlines()]

for row, line in enumerate(grid):
    for col, _ in enumerate(line):
        for n in range(4, 11):
            if col + n < len(line):
                cost = sum(grid[row][col + 1 + i] for i in range(n))
                g.add_edge((row, col, "r"), (row, col + n, "d"), cost)
                g.add_edge((row, col, "r"), (row, col + n, "u"), cost)
            if col - n >= 0:
                cost = sum(grid[row][col - 1 - i] for i in range(n))
                g.add_edge((row, col, "l"), (row, col - n, "d"), cost)
                g.add_edge((row, col, "l"), (row, col - n, "u"), cost)
            if row + n < len(grid):
                cost = sum(grid[row + 1 + i][col] for i in range(n))
                g.add_edge((row, col, "d"), (row + n, col, "l"), cost)
                g.add_edge((row, col, "d"), (row + n, col, "r"), cost)
            if row - n >= 0:
                cost = sum(grid[row - 1 - i][col] for i in range(n))
                g.add_edge((row, col, "u"), (row - n, col, "l"), cost)
                g.add_edge((row, col, "u"), (row - n, col, "r"), cost)

start = "start"
end = "end"
for dir in ("r", "d"):
    g.add_edge(start, (0, 0, dir), 0)
for dir in ("r", "l", "u", "d"):
    g.add_edge((len(grid) - 1, len(grid[0]) - 1, dir), end, 0)
print(g.node_count, g.edge_count)
print(find_path(g, start, end).total_cost)
