from cribbage.hand import Hand
from cribbage.cards import Deck, Card
from cribbage.hand_scorer import HandScorer
from itertools import combinations
from typing import Tuple, List


class DiscardAnalyzer:
    @staticmethod
    def _calculate_missing_cards(hand: Hand) -> Deck:
        full_deck = Deck()
        return [card for card in full_deck.deck if card not in hand.cards]

    @classmethod
    def evaluate(cls, hand: Hand, crib: bool = False) -> Tuple[List[Card], float]:
        possible_cut_cards = cls._calculate_missing_cards(hand)
        length_of_possible_cut_cards = len(possible_cut_cards)

        discard_options_averaged = []

        for i, discard_choices in enumerate(
            combinations(hand.cards, len(hand.cards) - 4)
        ):
            scores = 0
            discard_choices = list(discard_choices)

            keep_cards = [card for card in hand.cards if card not in discard_choices]

            for cut_card in possible_cut_cards:
                keep_hand = Hand(keep_cards)
                discard_hand = Hand(discard_choices)

                keep_score = HandScorer.score_hand(keep_hand, cut_card)
                discard_score = HandScorer.score_hand(discard_hand, cut_card)
                if not crib:
                    discard_score *= -1

                scores += keep_score + discard_score

            discard_options_averaged.append(
                (discard_choices, scores / length_of_possible_cut_cards)
            )

        return max(discard_options_averaged, key=lambda x: x[1])
