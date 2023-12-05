import pathlib
import os
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass
class Card:
    id_num: int
    nums: set[int]
    winning_nums: set[int]

    def matches(self):
        return len(self.nums.intersection(self.winning_nums))


def parse_card(line: str):
    line = line.strip()
    line = line.removeprefix("Card ")
    id_part, rest = line.split(":")
    winning_part, nums_part = rest.split("|")
    winning_nums = {int(s.strip()) for s in winning_part.split()}
    nums = {int(s.strip()) for s in nums_part.split()}
    return Card(int(id_part), nums, winning_nums)


s = 0
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        m = parse_card(line).matches()
        s += (m > 0) * (2 ** (m - 1))

print(s)
