import pytest
from unittest.mock import patch, MagicMock
from cribbage.cards import Card, Deck
from cribbage.hand import Hand
from cribbage.discard_analyzer import DiscardAnalyzer


@pytest.fixture
def sample_hand():
    """Fixture that provides a hand with specific cards for testing discards."""
    hand = Hand()
    hand.cards = [
        Card("5", "H"),
        Card("5", "S"),
        Card("J", "D"),
        Card("K", "C"),
        Card("A", "H"),
        Card("4", "S"),
    ]
    return hand


class TestDiscardAnalyzer:
    def test_calculate_missing_cards(self, sample_hand):
        """Test that missing cards are correctly identified."""
        # Create a smaller hand for this test
        test_hand = Hand()
        test_hand.cards = [Card("A", "H"), Card("K", "S")]

        # Get missing cards
        missing_cards = DiscardAnalyzer._calculate_missing_cards(test_hand)

        # Should have 52 - 2 = 50 cards
        assert len(missing_cards) == 50

        # Check that the hand cards are not in the missing cards
        for card in test_hand.cards:
            assert card not in missing_cards

        # Check a few specific cards that should be in the missing cards
        assert Card("2", "H") in missing_cards
        assert Card("Q", "D") in missing_cards
        assert Card("10", "C") in missing_cards

    def test_evaluate_crib_parameter(self):
        """Test that the crib parameter affects the evaluation with 30 different hands."""
        # Test case 1: Original test case with mixed values
        hand = Hand()
        hand.cards = [
            Card("5", "H"),
            Card("6", "S"),
            Card("J", "D"),
            Card("K", "C"),
            Card("A", "H"),
            Card("4", "S"),
        ]
        expected_discard_my_crib = [Card("J", "D"), Card("A", "H")]
        expected_discared_opp_crib = [Card("K", "C"), Card("A", "H")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 2: Hand with pairs
        hand = Hand()
        hand.cards = [
            Card("7", "H"),
            Card("7", "S"),
            Card("10", "D"),
            Card("10", "C"),
            Card("J", "H"),
            Card("Q", "S"),
        ]
        expected_discard_my_crib = [Card("7", "H"), Card("7", "S")]
        expected_discared_opp_crib = [Card("7", "H"), Card("7", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 3: Hand with potential run
        hand = Hand()
        hand.cards = [
            Card("4", "H"),
            Card("5", "S"),
            Card("6", "D"),
            Card("7", "C"),
            Card("9", "H"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("7", "C"), Card("9", "H")]
        expected_discared_opp_crib = [Card("7", "C"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 4: Hand with potential flush
        hand = Hand()
        hand.cards = [
            Card("4", "H"),
            Card("6", "H"),
            Card("9", "H"),
            Card("J", "H"),
            Card("5", "D"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("5", "D"), Card("K", "S")]
        expected_discared_opp_crib = [Card("5", "D"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 5: Hand with all face cards
        hand = Hand()
        hand.cards = [
            Card("J", "H"),
            Card("J", "S"),
            Card("Q", "D"),
            Card("Q", "C"),
            Card("K", "H"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("Q", "D"), Card("Q", "C")]
        expected_discared_opp_crib = [Card("K", "H"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 6: Hand with all low cards
        hand = Hand()
        hand.cards = [
            Card("A", "H"),
            Card("2", "S"),
            Card("3", "D"),
            Card("4", "C"),
            Card("5", "H"),
            Card("6", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("2", "S")]
        expected_discared_opp_crib = [Card("A", "H"), Card("6", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 7: Hand with fives and faces (good for fifteens)
        hand = Hand()
        hand.cards = [
            Card("5", "H"),
            Card("5", "S"),
            Card("10", "D"),
            Card("J", "C"),
            Card("Q", "H"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("Q", "H"), Card("K", "S")]
        expected_discared_opp_crib = [Card("Q", "H"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 8: Hand with multiple same rank cards
        hand = Hand()
        hand.cards = [
            Card("7", "H"),
            Card("7", "S"),
            Card("7", "D"),
            Card("A", "C"),
            Card("2", "H"),
            Card("3", "S"),
        ]
        expected_discard_my_crib = [Card("A", "C"), Card("2", "H")]
        expected_discared_opp_crib = [Card("A", "C"), Card("3", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 9: Hand with near-run cards
        hand = Hand()
        hand.cards = [
            Card("A", "H"),
            Card("3", "S"),
            Card("4", "D"),
            Card("5", "C"),
            Card("7", "H"),
            Card("8", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("7", "H")]
        expected_discared_opp_crib = [Card("A", "H"), Card("8", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 10: Hand with high-value cards only
        hand = Hand()
        hand.cards = [
            Card("8", "H"),
            Card("9", "S"),
            Card("10", "D"),
            Card("J", "C"),
            Card("Q", "H"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("8", "H"), Card("Q", "H")]
        expected_discared_opp_crib = [Card("Q", "H"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 11: Hand with all medium-value cards
        hand = Hand()
        hand.cards = [
            Card("4", "H"),
            Card("5", "S"),
            Card("6", "D"),
            Card("7", "C"),
            Card("8", "H"),
            Card("9", "S"),
        ]
        expected_discard_my_crib = [Card("4", "H"), Card("9", "S")]
        expected_discared_opp_crib = [Card("4", "H"), Card("5", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 12: Hand with potential straight flush
        hand = Hand()
        hand.cards = [
            Card("6", "H"),
            Card("7", "H"),
            Card("8", "H"),
            Card("9", "H"),
            Card("A", "D"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("A", "D"), Card("K", "S")]
        expected_discared_opp_crib = [Card("A", "D"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 13: Hand with all fives (optimal for fifteens)
        hand = Hand()
        hand.cards = [
            Card("5", "H"),
            Card("5", "S"),
            Card("5", "D"),
            Card("5", "C"),
            Card("A", "H"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("K", "S")]
        expected_discared_opp_crib = [Card("A", "H"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 14: Hand with mixed suits but same ranks
        hand = Hand()
        hand.cards = [
            Card("4", "H"),
            Card("4", "S"),
            Card("8", "D"),
            Card("8", "C"),
            Card("J", "H"),
            Card("J", "S"),
        ]
        expected_discard_my_crib = [Card("8", "D"), Card("8", "C")]
        expected_discared_opp_crib = [Card("J", "H"), Card("J", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 15: Hand with cards that form multiple fifteens
        hand = Hand()
        hand.cards = [
            Card("5", "H"),
            Card("10", "S"),
            Card("5", "D"),
            Card("10", "C"),
            Card("A", "H"),
            Card("4", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("4", "S")]
        expected_discared_opp_crib = [Card("A", "H"), Card("4", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 16: Hand with potential double run
        hand = Hand()
        hand.cards = [
            Card("6", "H"),
            Card("7", "S"),
            Card("7", "D"),
            Card("8", "C"),
            Card("9", "H"),
            Card("A", "S"),
        ]
        expected_discard_my_crib = [Card("A", "S"), Card("9", "H")]
        expected_discared_opp_crib = [Card("A", "S"), Card("6", "H")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 17: Hand with three pairs
        hand = Hand()
        hand.cards = [
            Card("3", "H"),
            Card("3", "S"),
            Card("6", "D"),
            Card("6", "C"),
            Card("9", "H"),
            Card("9", "S"),
        ]
        expected_discard_my_crib = [Card("3", "H"), Card("3", "S")]
        expected_discared_opp_crib = [Card("9", "H"), Card("9", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 18: Hand with good nobs potential
        hand = Hand()
        hand.cards = [
            Card("J", "H"),
            Card("J", "S"),
            Card("J", "D"),
            Card("J", "C"),
            Card("8", "H"),
            Card("9", "S"),
        ]
        expected_discard_my_crib = [Card("8", "H"), Card("9", "S")]
        expected_discared_opp_crib = [Card("8", "H"), Card("9", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 19: Hand with alternating high-low values
        hand = Hand()
        hand.cards = [
            Card("A", "H"),
            Card("K", "S"),
            Card("2", "D"),
            Card("Q", "C"),
            Card("3", "H"),
            Card("J", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("2", "D")]
        expected_discared_opp_crib = [Card("K", "S"), Card("J", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 20: Hand with near sequential order
        hand = Hand()
        hand.cards = [
            Card("2", "H"),
            Card("4", "S"),
            Card("6", "D"),
            Card("8", "C"),
            Card("10", "H"),
            Card("Q", "S"),
        ]
        expected_discard_my_crib = [Card("2", "H"), Card("Q", "S")]
        expected_discared_opp_crib = [Card("10", "H"), Card("Q", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 21: Hand with A-5 combination (good for runs)
        hand = Hand()
        hand.cards = [
            Card("A", "H"),
            Card("2", "S"),
            Card("3", "D"),
            Card("4", "C"),
            Card("5", "H"),
            Card("10", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("10", "S")]
        expected_discared_opp_crib = [Card("2", "S"), Card("10", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 22: Hand with evenly distributed values
        hand = Hand()
        hand.cards = [
            Card("3", "H"),
            Card("6", "S"),
            Card("9", "D"),
            Card("J", "C"),
            Card("K", "H"),
            Card("A", "S"),
        ]
        expected_discard_my_crib = [Card("3", "H"), Card("A", "S")]
        expected_discared_opp_crib = [Card("K", "H"), Card("A", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 23: Hand with all Aces and face cards
        hand = Hand()
        hand.cards = [
            Card("A", "H"),
            Card("A", "S"),
            Card("J", "D"),
            Card("Q", "C"),
            Card("K", "H"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("A", "S")]
        expected_discared_opp_crib = [Card("K", "H"), Card("K", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 24: Hand with all clubs
        hand = Hand()
        hand.cards = [
            Card("2", "C"),
            Card("5", "C"),
            Card("8", "C"),
            Card("J", "C"),
            Card("Q", "C"),
            Card("K", "C"),
        ]
        expected_discard_my_crib = [Card("J", "C"), Card("K", "C")]
        expected_discared_opp_crib = [Card("Q", "C"), Card("K", "C")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 25: Hand with cards that add to fifteen
        hand = Hand()
        hand.cards = [
            Card("5", "H"),
            Card("10", "S"),
            Card("6", "D"),
            Card("9", "C"),
            Card("7", "H"),
            Card("8", "S"),
        ]
        expected_discard_my_crib = [Card("10", "S"), Card("9", "C")]
        expected_discared_opp_crib = [Card("10", "S"), Card("5", "H")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 26: Hand with triple run potential
        hand = Hand()
        hand.cards = [
            Card("7", "H"),
            Card("7", "S"),
            Card("8", "D"),
            Card("8", "C"),
            Card("9", "H"),
            Card("9", "S"),
        ]
        expected_discard_my_crib = [Card("7", "H"), Card("7", "S")]
        expected_discared_opp_crib = [Card("9", "H"), Card("9", "S")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 27: Hand with all values below 5
        hand = Hand()
        hand.cards = [
            Card("A", "H"),
            Card("2", "S"),
            Card("2", "D"),
            Card("3", "C"),
            Card("3", "H"),
            Card("4", "S"),
        ]
        expected_discard_my_crib = [Card("A", "H"), Card("4", "S")]
        expected_discared_opp_crib = [Card("2", "D"), Card("3", "H")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 28: Hand with multiple potential fifteens
        hand = Hand()
        hand.cards = [
            Card("5", "H"),
            Card("5", "S"),
            Card("5", "D"),
            Card("10", "C"),
            Card("J", "H"),
            Card("K", "S"),
        ]
        expected_discard_my_crib = [Card("K", "S"), Card("J", "H")]
        expected_discared_opp_crib = [Card("K", "S"), Card("J", "H")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib
