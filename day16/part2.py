import pathlib
import os
from functools import cache

THIS_DIR = pathlib.Path(__file__).parent.resolve()


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    grid = [line.strip() for line in f.readlines()]


def num_energized(start):
    seen = set()
    energized = set()
    to_check = [start]

    while len(to_check):
        new_to_check = []
        for p in to_check:
            if p not in seen:
                seen.add(p)
                row, col, dir = p
                energized.add((row, col))
                if dir == "r" and col + 1 < len(grid[row]):
                    newc = grid[row][col + 1]
                    if newc in ".-":
                        new_to_check.append((row, col + 1, dir))
                    if newc in "/|":
                        new_to_check.append((row, col + 1, "u"))
                    if newc in "\\|":
                        new_to_check.append((row, col + 1, "d"))
                elif dir == "l" and col - 1 >= 0:
                    newc = grid[row][col - 1]
                    if newc in ".-":
                        new_to_check.append((row, col - 1, dir))
                    if newc in "\\|":
                        new_to_check.append((row, col - 1, "u"))
                    if newc in "/|":
                        new_to_check.append((row, col - 1, "d"))
                elif dir == "u" and row - 1 >= 0:
                    newc = grid[row - 1][col]
                    if newc in ".|":
                        new_to_check.append((row - 1, col, dir))
                    if newc in "\\-":
                        new_to_check.append((row - 1, col, "l"))
                    if newc in "/-":
                        new_to_check.append((row - 1, col, "r"))
                elif dir == "d" and row + 1 < len(grid):
                    newc = grid[row + 1][col]
                    if newc in ".|":
                        new_to_check.append((row + 1, col, dir))
                    if newc in "\\-":
                        new_to_check.append((row + 1, col, "r"))
                    if newc in "/-":
                        new_to_check.append((row + 1, col, "l"))
        to_check = new_to_check

    return len(energized)


starts = (
    [(-1, c, "d") for c in range(len(grid[0]))]
    + [(r, -1, "r") for r in range(len(grid))]
    + [(len(grid), c, "u") for c in range(len(grid[0]))]
    + [(r, len(grid[0]), "l") for r in range(len(grid))]
)

print(max(num_energized(start) for start in starts))
