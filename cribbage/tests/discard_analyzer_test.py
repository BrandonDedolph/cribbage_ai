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
        Card("H", "5"),
        Card("S", "5"),
        Card("D", "J"),
        Card("C", "K"),
        Card("H", "A"),
        Card("S", "4"),
    ]
    return hand


class TestDiscardAnalyzer:
    def test_calculate_missing_cards(self, sample_hand):
        """Test that missing cards are correctly identified."""
        # Create a smaller hand for this test
        test_hand = Hand()
        test_hand.cards = [Card("H", "A"), Card("S", "K")]

        # Get missing cards
        missing_cards = DiscardAnalyzer._calculate_missing_cards(test_hand)

        # Should have 52 - 2 = 50 cards
        assert len(missing_cards) == 50

        # Check that the hand cards are not in the missing cards
        for card in test_hand.cards:
            assert card not in missing_cards

        # Check a few specific cards that should be in the missing cards
        assert Card("H", "2") in missing_cards
        assert Card("D", "Q") in missing_cards
        assert Card("C", "10") in missing_cards

    def test_evaluate_crib_parameter(self):
        """Test that the crib parameter affects the evaluation with 30 different hands."""
        # Test case 1: Original test case with mixed values
        hand = Hand()
        hand.cards = [
            Card("H", "5"),
            Card("S", "6"),
            Card("D", "J"),
            Card("C", "K"),
            Card("H", "A"),
            Card("S", "4"),
        ]
        expected_discard_my_crib = [Card("D", "J"), Card("H", "A")]
        expected_discared_opp_crib = [Card("C", "K"), Card("H", "A")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 2: Hand with pairs
        hand = Hand()
        hand.cards = [
            Card("H", "7"),
            Card("S", "7"),
            Card("D", "10"),
            Card("C", "10"),
            Card("H", "J"),
            Card("S", "Q"),
        ]
        expected_discard_my_crib = [Card("H", "7"), Card("S", "7")]
        expected_discared_opp_crib = [Card("H", "7"), Card("S", "7")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 3: Hand with potential run
        hand = Hand()
        hand.cards = [
            Card("H", "4"),
            Card("S", "5"),
            Card("D", "6"),
            Card("C", "7"),
            Card("H", "9"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("C", "7"), Card("H", "9")]
        expected_discared_opp_crib = [Card("C", "7"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 4: Hand with potential flush
        hand = Hand()
        hand.cards = [
            Card("H", "4"),
            Card("H", "6"),
            Card("H", "9"),
            Card("H", "J"),
            Card("D", "5"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("D", "5"), Card("S", "K")]
        expected_discared_opp_crib = [Card("D", "5"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 5: Hand with all face cards
        hand = Hand()
        hand.cards = [
            Card("H", "J"),
            Card("S", "J"),
            Card("D", "Q"),
            Card("C", "Q"),
            Card("H", "K"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("D", "Q"), Card("C", "Q")]
        expected_discared_opp_crib = [Card("H", "K"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 6: Hand with all low cards
        hand = Hand()
        hand.cards = [
            Card("H", "A"),
            Card("S", "2"),
            Card("D", "3"),
            Card("C", "4"),
            Card("H", "5"),
            Card("S", "6"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("S", "2")]
        expected_discared_opp_crib = [Card("H", "A"), Card("S", "6")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 7: Hand with fives and faces (good for fifteens)
        hand = Hand()
        hand.cards = [
            Card("H", "5"),
            Card("S", "5"),
            Card("D", "10"),
            Card("C", "J"),
            Card("H", "Q"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("H", "Q"), Card("S", "K")]
        expected_discared_opp_crib = [Card("H", "Q"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 8: Hand with multiple same rank cards
        hand = Hand()
        hand.cards = [
            Card("H", "7"),
            Card("S", "7"),
            Card("D", "7"),
            Card("C", "A"),
            Card("H", "2"),
            Card("S", "3"),
        ]
        expected_discard_my_crib = [Card("C", "A"), Card("H", "2")]
        expected_discared_opp_crib = [Card("C", "A"), Card("S", "3")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 9: Hand with near-run cards
        hand = Hand()
        hand.cards = [
            Card("H", "A"),
            Card("S", "3"),
            Card("D", "4"),
            Card("C", "5"),
            Card("H", "7"),
            Card("S", "8"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("H", "7")]
        expected_discared_opp_crib = [Card("H", "A"), Card("S", "8")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 10: Hand with high-value cards only
        hand = Hand()
        hand.cards = [
            Card("H", "8"),
            Card("S", "9"),
            Card("D", "10"),
            Card("C", "J"),
            Card("H", "Q"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("H", "8"), Card("H", "Q")]
        expected_discared_opp_crib = [Card("H", "Q"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 11: Hand with all medium-value cards
        hand = Hand()
        hand.cards = [
            Card("H", "4"),
            Card("S", "5"),
            Card("D", "6"),
            Card("C", "7"),
            Card("H", "8"),
            Card("S", "9"),
        ]
        expected_discard_my_crib = [Card("H", "4"), Card("S", "9")]
        expected_discared_opp_crib = [Card("H", "4"), Card("S", "5")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 12: Hand with potential straight flush
        hand = Hand()
        hand.cards = [
            Card("H", "6"),
            Card("H", "7"),
            Card("H", "8"),
            Card("H", "9"),
            Card("D", "A"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("D", "A"), Card("S", "K")]
        expected_discared_opp_crib = [Card("D", "A"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 13: Hand with all fives (optimal for fifteens)
        hand = Hand()
        hand.cards = [
            Card("H", "5"),
            Card("S", "5"),
            Card("D", "5"),
            Card("C", "5"),
            Card("H", "A"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("S", "K")]
        expected_discared_opp_crib = [Card("H", "A"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 14: Hand with mixed suits but same ranks
        hand = Hand()
        hand.cards = [
            Card("H", "4"),
            Card("S", "4"),
            Card("D", "8"),
            Card("C", "8"),
            Card("H", "J"),
            Card("S", "J"),
        ]
        expected_discard_my_crib = [Card("D", "8"), Card("C", "8")]
        expected_discared_opp_crib = [Card("H", "J"), Card("S", "J")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 15: Hand with cards that form multiple fifteens
        hand = Hand()
        hand.cards = [
            Card("H", "5"),
            Card("S", "10"),
            Card("D", "5"),
            Card("C", "10"),
            Card("H", "A"),
            Card("S", "4"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("S", "4")]
        expected_discared_opp_crib = [Card("H", "A"), Card("S", "4")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 16: Hand with potential double run
        hand = Hand()
        hand.cards = [
            Card("H", "6"),
            Card("S", "7"),
            Card("D", "7"),
            Card("C", "8"),
            Card("H", "9"),
            Card("S", "A"),
        ]
        expected_discard_my_crib = [Card("S", "A"), Card("H", "9")]
        expected_discared_opp_crib = [Card("S", "A"), Card("H", "6")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 17: Hand with three pairs
        hand = Hand()
        hand.cards = [
            Card("H", "3"),
            Card("S", "3"),
            Card("D", "6"),
            Card("C", "6"),
            Card("H", "9"),
            Card("S", "9"),
        ]
        expected_discard_my_crib = [Card("H", "3"), Card("S", "3")]
        expected_discared_opp_crib = [Card("H", "9"), Card("S", "9")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 18: Hand with good nobs potential
        hand = Hand()
        hand.cards = [
            Card("H", "J"),
            Card("S", "J"),
            Card("D", "J"),
            Card("C", "J"),
            Card("H", "8"),
            Card("S", "9"),
        ]
        expected_discard_my_crib = [Card("H", "8"), Card("S", "9")]
        expected_discared_opp_crib = [Card("H", "8"), Card("S", "9")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 19: Hand with alternating high-low values
        hand = Hand()
        hand.cards = [
            Card("H", "A"),
            Card("S", "K"),
            Card("D", "2"),
            Card("C", "Q"),
            Card("H", "3"),
            Card("S", "J"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("D", "2")]
        expected_discared_opp_crib = [Card("S", "K"), Card("S", "J")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 20: Hand with near sequential order
        hand = Hand()
        hand.cards = [
            Card("H", "2"),
            Card("S", "4"),
            Card("D", "6"),
            Card("C", "8"),
            Card("H", "10"),
            Card("S", "Q"),
        ]
        expected_discard_my_crib = [Card("H", "2"), Card("S", "Q")]
        expected_discared_opp_crib = [Card("H", "10"), Card("S", "Q")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 21: Hand with A-5 combination (good for runs)
        hand = Hand()
        hand.cards = [
            Card("H", "A"),
            Card("S", "2"),
            Card("D", "3"),
            Card("C", "4"),
            Card("H", "5"),
            Card("S", "10"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("S", "10")]
        expected_discared_opp_crib = [Card("S", "2"), Card("S", "10")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 22: Hand with evenly distributed values
        hand = Hand()
        hand.cards = [
            Card("H", "3"),
            Card("S", "6"),
            Card("D", "9"),
            Card("C", "J"),
            Card("H", "K"),
            Card("S", "A"),
        ]
        expected_discard_my_crib = [Card("H", "3"), Card("S", "A")]
        expected_discared_opp_crib = [Card("H", "K"), Card("S", "A")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 23: Hand with all Aces and face cards
        hand = Hand()
        hand.cards = [
            Card("H", "A"),
            Card("S", "A"),
            Card("D", "J"),
            Card("C", "Q"),
            Card("H", "K"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("S", "A")]
        expected_discared_opp_crib = [Card("H", "K"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 24: Hand with all clubs
        hand = Hand()
        hand.cards = [
            Card("C", "2"),
            Card("C", "5"),
            Card("C", "8"),
            Card("C", "J"),
            Card("C", "Q"),
            Card("C", "K"),
        ]
        expected_discard_my_crib = [Card("C", "J"), Card("C", "K")]
        expected_discared_opp_crib = [Card("C", "Q"), Card("C", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 25: Hand with cards that add to fifteen
        hand = Hand()
        hand.cards = [
            Card("H", "5"),
            Card("S", "10"),
            Card("D", "6"),
            Card("C", "9"),
            Card("H", "7"),
            Card("S", "8"),
        ]
        expected_discard_my_crib = [Card("S", "10"), Card("C", "9")]
        expected_discared_opp_crib = [Card("S", "10"), Card("H", "5")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 26: Hand with triple run potential
        hand = Hand()
        hand.cards = [
            Card("H", "7"),
            Card("S", "7"),
            Card("D", "8"),
            Card("C", "8"),
            Card("H", "9"),
            Card("S", "9"),
        ]
        expected_discard_my_crib = [Card("H", "7"), Card("S", "7")]
        expected_discared_opp_crib = [Card("H", "9"), Card("S", "9")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 27: Hand with all values below 5
        hand = Hand()
        hand.cards = [
            Card("H", "A"),
            Card("S", "2"),
            Card("D", "2"),
            Card("C", "3"),
            Card("H", "3"),
            Card("S", "4"),
        ]
        expected_discard_my_crib = [Card("H", "A"), Card("S", "4")]
        expected_discared_opp_crib = [Card("D", "2"), Card("H", "3")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 28: Hand with multiple potential fifteens
        hand = Hand()
        hand.cards = [
            Card("H", "5"),
            Card("S", "5"),
            Card("D", "5"),
            Card("C", "10"),
            Card("H", "J"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("S", "K"), Card("H", "J")]
        expected_discared_opp_crib = [Card("S", "K"), Card("H", "J")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 29: Hand with royal flush-like cards
        hand = Hand()
        hand.cards = [
            Card("H", "10"),
            Card("H", "J"),
            Card("H", "Q"),
            Card("H", "K"),
            Card("D", "A"),
            Card("S", "2"),
        ]
        expected_discard_my_crib = [Card("D", "A"), Card("S", "2")]
        expected_discared_opp_crib = [Card("D", "A"), Card("S", "2")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib

        # Test case 30: Hand with scattered values
        hand = Hand()
        hand.cards = [
            Card("H", "2"),
            Card("S", "5"),
            Card("D", "7"),
            Card("C", "9"),
            Card("H", "J"),
            Card("S", "K"),
        ]
        expected_discard_my_crib = [Card("H", "2"), Card("S", "K")]
        expected_discared_opp_crib = [Card("H", "J"), Card("S", "K")]
        discard_own, score_own = DiscardAnalyzer.evaluate(hand, crib=True)
        discard_opp, score_opp = DiscardAnalyzer.evaluate(hand, crib=False)
        assert discard_own == expected_discard_my_crib
        assert discard_opp == expected_discared_opp_crib
