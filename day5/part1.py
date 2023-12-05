import pathlib
import os
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()


@dataclass
class TransRange:
    from_start: int
    to_start: int
    length: int

    def __contains__(self, key):
        return key >= self.from_start and key <= self.from_start + self.length
    
    def convert(self, input):
        return self.to_start + (input - self.from_start)
    

category_map : dict[str,(str, list[TransRange])] = dict()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    raw = f.readlines()
    seeds = [int(s) for s in raw[0].strip().removeprefix("seeds: ").split()]
    raw = raw[2:]
    curr_ranges = []
    curr_from = ""
    curr_to = ""
    for line in raw:
        if "map:" in line:
            curr_from, curr_to = line.strip().replace(" map:","").split("-to-")
        elif len(line.strip()) == 0:
            category_map[curr_from] = (curr_to, curr_ranges)
            curr_from = ""
            curr_to = ""
            curr_ranges = []
        else:
            parts = line.strip().split()
            curr_ranges.append(TransRange(int(parts[1]), int(parts[0]), int(parts[2])))
    category_map[curr_from] = (curr_to, curr_ranges)

def seed_to_location(seed):
    curr = seed
    curr_cat = "seed"
    while curr_cat != "location":
        curr_cat, rs = category_map[curr_cat]
        r = next((r for r in rs if curr in r), None)
        if r is not None:
            curr = r.convert(curr)
    return curr

print(min([seed_to_location(seed) for seed in seeds]))