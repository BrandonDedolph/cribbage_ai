from cribbage.hand import Hand
from cribbage.cards import Card, Deck
from typing import List
from itertools import combinations
from collections import Counter


WINNING_SCORE = 121


# 2 Person Cribbage
class Cribbage:
    def __init__(self):
        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_hand = None
        self.player_2_hand = None
        self.deck = Deck()
        self.deck.shuffle()

    def play(self):
        pass

    def _rank_to_ordered_numerical(self, rank: str):
        match rank:
            case "J":
                return 11
            case "Q":
                return 12
            case "K":
                return 13
            case _:
                return self._rank_to_value(rank)

    def _rank_to_value(self, rank: str):
        match rank:
            case "A":
                return 1
            case "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10":
                return int(rank)
            case "J" | "Q" | "K":
                return 10

    def _score_15s(self, cards: List[Card]) -> int:
        total = 0

        for r in range(2, len(cards) + 1):
            for combo in combinations(cards, r):
                if sum(self._rank_to_value(card.rank) for card in combo) == 15:
                    total += 2

        return total

    def _score_runs(self, cards: List[Card]) -> int:
        ranks = [self._rank_to_ordered_numerical(card.rank) for card in cards]
        unique_ranks = sorted(set(ranks))

        # Return if length is less than or equal to 2, as 3 is needed to make a run
        if len(unique_ranks) <= 2:
            return 0

        rank_counter = Counter(ranks)

        largest_run = []

        for r in range(0, len(unique_ranks) - 2):
            if len(largest_run) > len(unique_ranks) - r:
                break
            current_run = [unique_ranks[r]]
            current = r
            run = True
            while run and current < len(unique_ranks) - 1:
                if unique_ranks[current] + 1 == unique_ranks[current + 1]:
                    current += 1
                    current_run.append(unique_ranks[current])
                    largest_run = max(largest_run, current_run)
                else:
                    run = False

        if len(largest_run) < 3:
            return 0

        pairs = 0
        triples = 0

        for card in largest_run:
            match rank_counter[card]:
                case 2:
                    pairs += 1
                case 3:
                    triples += 1

        return len(largest_run) * (2**pairs) * (3**triples)

    def _score_pairs(self, cards: List[Card]) -> int:
        rank_counter = Counter(card.rank for card in cards)

        return sum([total * (total - 1) for total in rank_counter.values()])

    def _score_flush(self, hand: Hand, cut_card: Card, crib: bool = False) -> int:
        total = 0

        suits_found_just_hand = set([card.suit for card in hand.cards])
        suits_found_with_cut = set([card.suit for card in hand.cards + [cut_card]])

        if len(suits_found_just_hand) == 1:
            total = 4
            if len(suits_found_with_cut) == 1:
                total = 5
            elif crib:
                total = 0

        return total

    def _score_nobs(self, hand: Hand, cut_card: Card) -> int:
        for card in hand.cards:
            if card.rank == "J" and card.suit == cut_card.suit:
                return 1

        return 0

    def score_hand(self, hand: Hand, cut_card: Card, crib: bool = False) -> int:
        return (
            self._score_15s(hand.cards + [cut_card])
            + self._score_runs(hand.cards + [cut_card])
            + self._score_pairs(hand.cards + [cut_card])
            + self._score_flush(hand, cut_card, crib)
            + self._score_nobs(hand, cut_card)
        )
