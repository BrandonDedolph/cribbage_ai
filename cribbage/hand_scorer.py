from cribbage.hand import Hand
from cribbage.cards import Card
from typing import List
from itertools import combinations
from collections import Counter


class HandScorer:
    @classmethod
    def _rank_to_ordered_numerical(cls, rank: str):
        match rank:
            case "J":
                return 11
            case "Q":
                return 12
            case "K":
                return 13
            case _:
                return cls._rank_to_value(rank)

    @staticmethod
    def _rank_to_value(rank: str):
        match rank:
            case "A":
                return 1
            case "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10":
                return int(rank)
            case "J" | "Q" | "K":
                return 10

    @classmethod
    def _score_15s(cls, cards: List[Card]) -> int:
        total = 0

        for r in range(2, len(cards) + 1):
            for combo in combinations(cards, r):
                if sum(cls._rank_to_value(card.rank) for card in combo) == 15:
                    total += 2
        return total

    @classmethod
    def _score_runs(cls, cards: List[Card]) -> int:
        ranks = [cls._rank_to_ordered_numerical(card.rank) for card in cards]
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
                    largest_run = max(largest_run, current_run, key=len)
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

    @staticmethod
    def _score_pairs(cards: List[Card]) -> int:
        rank_counter = Counter(card.rank for card in cards)

        return sum([total * (total - 1) for total in rank_counter.values()])

    @staticmethod
    def _score_flush(hand: Hand, cut_card: Card, crib: bool = False) -> int:
        total = 0

        if len(hand.cards) < 4:
            return total

        suits_found_just_hand = set([card.suit for card in hand.cards])
        suits_found_with_cut = set(
            [card.suit for card in hand.cards + [cut_card]])

        if len(suits_found_just_hand) == 1:
            total = 4
            if len(suits_found_with_cut) == 1:
                total = 5
            elif crib:
                total = 0

        return total

    @staticmethod
    def _score_nobs(hand: Hand, cut_card: Card) -> int:
        for card in hand.cards:
            if card.rank == "J" and card.suit == cut_card.suit:
                return 1

        return 0

    @classmethod
    def score_hand(cls, hand: Hand, cut_card: Card, crib: bool = False) -> int:
        return (
            cls._score_15s(hand.cards + [cut_card])
            + cls._score_runs(hand.cards + [cut_card])
            + cls._score_pairs(hand.cards + [cut_card])
            + cls._score_flush(hand, cut_card, crib)
            + cls._score_nobs(hand, cut_card)
        )
