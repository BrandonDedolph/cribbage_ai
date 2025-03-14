from cribbage.cribbage_board import CribbageBoard

WINNING_SCORE = 121

# 2 Person Cribbage


class Cribbage:
    def __init__(self):
        self.board = CribbageBoard
        self.player_1_hand = None
        self.player_2_hand = None
        self.deck = Deck()
        self.deck.shuffle()

    def play(self):
        pass
