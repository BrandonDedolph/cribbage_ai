# Objective is to create a deck of cards that understands what's in the deck, it can be shuffled, drawn / delt from, etc.
import random
from typing import List


class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + self.suit

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __repr__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    SUITS = ["H", "D", "S", "C"]  # Heart, Diamond, Spade, Club
    RANKS = [
        "A",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "J",  # Jack
        "Q",  # Queen
        "K",  # King
    ]

    def __init__(self):
        self.reset()

    def draw(self) -> Card:
        if self.deck:
            return self.deck.pop()

    def reset(self):
        self.deck: List[Card] = []
        for suit in self.SUITS:
            for rank in self.RANKS:
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.deck)
