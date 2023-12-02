from dataclasses import dataclass
import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass
class Round:
    red: int
    green: int
    blue : int

@dataclass
class Game:
    id_num: int
    rounds: list[Round]

def parse_round(line: str):
    red, green, blue = 0,0,0
    for part in line.split(","):
        num, color = part.strip().split(" ")
        if color == "red":
            red = int(num)
        elif color == "green":
            green = int(num)
        elif color == "blue":
            blue = int(num)
        else:
            raise ValueError(line, part)
    return Round(red, green, blue)

def parse_game(line: str):
    game_part, round_part = line.split(":")
    id_num = int(game_part.removeprefix("Game "))
    rounds = [parse_round(l) for l in round_part.strip().split(";")]
    return Game(id_num, rounds)

s = 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        game = parse_game(line)
        power = max(r.red for r in game.rounds)*max(r.green for r in game.rounds)*max(r.blue for r in game.rounds)
        s += power

print(s)