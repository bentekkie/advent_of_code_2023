import pathlib
import os
from collections import Counter
from functools import cached_property, cache
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()

card_order = "AKQT98765432J"
j_cards = card_order[:-1]

def expand_jokers(cards: str):
    out = [""]
    for c in cards:
        out = [s+k for s in out for k in (j_cards if c == "J" else c)]
    return out

@cache
def hand_rank(cards: str):
    if "J" in cards:
        return max(hand_rank(c) for c in expand_jokers(cards))
    c = Counter(cards)
    l = c.most_common(2)
    f = l[0][1]
    if f == 5:
        return 7
    s = l[1][1]
    if f == 4:
        return 6
    if f == 3:
        return 4 + (s == 2)
    if f == 2:
        return 2 + (s == 2)
    return 1


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int

    @property
    def hand_type(self):
        return hand_rank(self.cards)

    @cached_property
    def ordinals(self):
        return tuple(card_order.index(s) for s in self.cards)

    def __lt__(self, other: "Hand"):
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type > other.hand_type:
            return False
        for s, o in zip(self.ordinals, other.ordinals):
            if s > o:
                return True
            if s < o:
                return False
        return False


hands = []
with open(os.path.join(THIS_DIR, "input.txt")) as f:
    for line in f.readlines():
        raw_hand, raw_bid = line.strip().split()
        hands.append(Hand(raw_hand.strip(), int(raw_bid)))

hands.sort()

print(sum((i + 1) * h.bid for i, h in enumerate(hands)))
