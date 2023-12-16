import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()


with open(os.path.join(THIS_DIR, "input.txt")) as f:
    grid = [line.strip() for line in f.readlines()]

seen = set()
start = (0, -1, "r")
to_check = [start]


def print_seen():
    max_row = max(r for r, _, _ in seen)
    max_col = max(c for _, c, _ in seen)
    for row, line in enumerate(grid):
        if row > max_row + 1:
            continue
        for col, c in enumerate(line):
            if col > max_col + 1:
                continue
            cs = []
            if (row, col, "u") in seen:
                cs.append("^")
            if (row, col, "d") in seen:
                cs.append("v")
            if (row, col, "l") in seen:
                cs.append("<")
            if (row, col, "r") in seen:
                cs.append(">")
            if len(cs) == 0:
                print(c, end="")
            elif len(cs) == 1:
                print(cs[0], end="")
            else:
                print(str(len(cs)), end="")
        print()
    print()


while len(to_check):
    new_to_check = []
    for p in to_check:
        if p not in seen:
            seen.add(p)
            row, col, dir = p
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

energized = {(r, c) for r, c, _ in seen - {start}}

print(len(energized))
