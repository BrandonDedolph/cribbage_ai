import pytest
import random
from unittest.mock import patch
from cribbage.cards import Card, Deck


class TestCard:
    def test_card_creation(self):
        card = Card("K", "H")
        assert card.rank == "K"
        assert card.suit == "H"

    def test_card_string_representation(self):
        card = Card("10", "D")
        assert str(card) == "10D"

        card = Card("Q", "S")
        assert str(card) == "QS"

    def test_card_equality(self):
        card1 = Card("Q", "H")
        card2 = Card("Q", "S")
        card3 = Card("Q", "H")

        assert card1 != card2
        assert card1 == card3


class TestDeck:
    def test_deck_initialization(self):
        deck = Deck()
        assert len(deck.deck) == 52  # 4 suits × 13 ranks = 52 cards

        # Check if all cards are unique
        card_strings = [str(card) for card in deck.deck]
        assert len(card_strings) == len(set(card_strings))

        # Check if all suits and ranks are present
        ranks = set([card.rank for card in deck.deck])
        suits = set([card.suit for card in deck.deck])
        assert ranks == set(Deck.RANKS)
        assert suits == set(Deck.SUITS)

    def test_draw_card(self):
        deck = Deck()
        initial_count = len(deck.deck)

        # Draw a card
        card = deck.draw()
        assert isinstance(card, Card)
        assert len(deck.deck) == initial_count - 1

        # Draw all remaining cards
        for _ in range(initial_count - 1):
            deck.draw()

        # Deck should be empty now
        assert len(deck.deck) == 0

        # Drawing from empty deck should return None
        assert deck.draw() is None

    def test_reset_deck(self):
        deck = Deck()

        # Draw some cards
        for _ in range(10):
            deck.draw()

        assert len(deck.deck) == 42

        # Reset the deck
        deck.reset()
        assert len(deck.deck) == 52

    @patch("random.shuffle")
    def test_shuffle_deck(self, mock_shuffle):
        deck = Deck()
        deck.shuffle()

        # Verify that random.shuffle was called with the deck
        mock_shuffle.assert_called_once_with(deck.deck)

    def test_shuffle_randomizes_order(self):
        # This test may occasionally fail due to the nature of randomness
        # but the probability is extremely low
        deck1 = Deck()
        deck2 = Deck()

        # Get the initial order of cards
        cards1 = [str(card) for card in deck1.deck.copy()]

        # Shuffle the second deck
        deck2.shuffle()
        cards2 = [str(card) for card in deck2.deck]

        # The shuffled deck should have the same cards but in different order
        assert sorted(cards1) == sorted(cards2)

        # The probability of shuffling and getting the same order is 1/52!,
        # which is effectively zero for practical purposes
        assert cards1 != cards2

