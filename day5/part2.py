import pathlib
import os
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()

@dataclass(frozen=True)
class SimpleRange:
    start: int
    length: int



@dataclass
class TransRange:
    from_start: int
    to_start: int
    length: int
    
    def convert_int(self, input):
        return self.to_start + (input - self.from_start)

    def convert_range(self, input: SimpleRange):
        if input.start >= self.from_start and input.start + input.length <= self.from_start + self.length:
            return SimpleRange(self.convert_int(input.start), input.length),[]
        if input.start < self.from_start and input.start + input.length > self.from_start+self.length:
            return SimpleRange(self.to_start, self.length), [
                SimpleRange(input.start, self.from_start - input.start),
                SimpleRange(self.from_start, (input.start + input.length) - (self.from_start + self.length))
            ]
        if input.start < self.from_start and input.start + input.length > self.from_start:
            return SimpleRange(self.to_start, input.length - (self.from_start - input.start)), [
                SimpleRange(input.start, self.from_start - input.start)
            ]
        if input.start < self.from_start + self.length and input.start + input.length > self.from_start + self.length:
            return SimpleRange(self.convert_int(input.start), (self.from_start + self.length) - input.start), [
                SimpleRange(self.from_start + self.length, input.length - ((self.from_start + self.length) - input.start ))
            ]
        return None, [input]
        
    

category_map : dict[str,(str, list[TransRange])] = dict()

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    raw = f.readlines()
    seeds = [int(s) for s in raw[0].strip().removeprefix("seeds: ").split()]
    seed_ranges = [SimpleRange(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
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

def seed_range_to_location(seed_range):
    curr = {seed_range}
    curr_cat = "seed"
    while curr_cat != "location":
        to_process = curr
        curr = set()
        curr_cat, rs = category_map[curr_cat]
        for tr in rs:
            new_to_process = set()
            for r in to_process:
                nr, rem = tr.convert_range(r)
                new_to_process.update(rem)
                if nr is not None:
                    curr.add(nr)
            to_process = new_to_process
        curr.update(to_process)
    return curr



print(min(lr.start for sr in seed_ranges for lr in seed_range_to_location(sr)))