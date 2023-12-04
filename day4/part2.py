import pathlib
import os
from dataclasses import dataclass
from functools import cached_property

THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass
class Card:
    id_num : int
    nums : list[int]
    winning_nums : list[int]
    count: int = 0

    @cached_property
    def matches(self):
        return len(set(self.nums).intersection(set(self.winning_nums)))


def parse_card(line : str):
    line = line.strip()
    line = line.removeprefix("Card ")
    id_part, rest = line.split(":")
    winning_part, nums_part = rest.split("|")
    winning_nums = [int(s.strip()) for s in winning_part.split()]
    nums = [int(s.strip()) for s in nums_part.split()]
    return Card(int(id_part), nums, winning_nums)

cards: dict[int,Card] = dict()
to_process : list[int] = []
with open(os.path.join(THIS_DIR, "input.txt")) as f:
        for line in f.readlines():
             c = parse_card(line)
             cards[c.id_num] = c
             to_process.append(c.id_num)

while len(to_process) > 0:
    new_process = []
    for id in to_process:
          cards[id].count += 1
          m = cards[id].matches
          if m > 0:
               new_process.extend(id+x for x in range(1,m+1))
    to_process = new_process

print(sum(c.count for c in cards.values()))

