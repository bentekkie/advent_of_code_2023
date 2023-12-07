import pathlib
import os
from collections import Counter
from functools import cached_property
from dataclasses import dataclass

THIS_DIR = pathlib.Path(__file__).parent.resolve()

card_order = "AKQT98765432J"


def hand_rank(cards: str):
    if "J" in cards:
        return max(hand_rank(cards.replace("J", c, 1)) for c in card_order[:-1])
    c = Counter(cards)
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


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int

    @cached_property
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
