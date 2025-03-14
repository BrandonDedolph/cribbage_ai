from cribbage.cards import Card
from typing import List


class Hand:
    def __init__(self, cards: List[Card] = None):
        self.cards = cards if cards else []

    def draw(self, card: Card):
        self.cards.append(card)

    def play(self, card_index: int):
        return self.cards.pop(card_index)

    def show_hand(self):
        for index, card in enumerate(self.cards):
            print(f"{index}:{card}")
