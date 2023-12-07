import pathlib
import os
from collections import Counter
from functools import cached_property
from dataclasses import dataclass
from math import sqrt, floor, ceil, prod

THIS_DIR = pathlib.Path(__file__).parent.resolve()

card_order = "AKQJT98765432"

@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int

    @cached_property
    def hand_type(self):
        c = Counter(self.cards)
        l = c.most_common(2)
        if l[0][1] == 5:
             return 7
        if l[0][1] == 4:
             return 6
        if l[0][1] == 3 and l[1][1] == 2:
             return 5
        if l[0][1] == 3:
             return 4
        if l[0][1] == 2 and l[1][1] == 2:
             return 3
        if l[0][1] == 2:
             return 2
        return 1
    
    @cached_property
    def ordinals(self):
        return tuple(card_order.index(s) for s in self.cards)

    
    def __lt__(self, other: "Hand"):
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type > other.hand_type:
            return False
        for s,o in zip(self.ordinals, other.ordinals):
             if s > o:
                  return True
             if s < o: 
                  return False
        print("eq")
        return False
        
hands = []
with open(os.path.join(THIS_DIR, "input.txt")) as f:
        for line in f.readlines():
             raw_hand, raw_bid = line.strip().split()
             hands.append(Hand(raw_hand.strip(), int(raw_bid)))

hands.sort()

print(sum((i+1)*h.bid for i, h in enumerate(hands)))