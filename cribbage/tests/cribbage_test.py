import pytest
from cribbage.cards import Card, Deck
from cribbage.hand import Hand
from cribbage.cribbage import Cribbage


@pytest.fixture
def cribbage_game():
    """Fixture that provides a new cribbage game instance."""
    return Cribbage()


@pytest.fixture
def sample_hand():
    """Fixture that provides a hand with specific cards for testing scoring."""
    hand = Hand()
    hand.draw(Card("H", "5"))
    hand.draw(Card("S", "5"))
    hand.draw(Card("D", "5"))
    hand.draw(Card("C", "J"))
    return hand


class TestCribbage:
    def test_init(self, cribbage_game):
        """Test that a new game initializes with correct starting values."""
        assert cribbage_game.player_1_score == 0
        assert cribbage_game.player_2_score == 0
        assert cribbage_game.player_1_hand is None
        assert cribbage_game.player_2_hand is None
        assert isinstance(cribbage_game.deck, Deck)
        assert len(cribbage_game.deck.deck) == 52  # Full deck

    def test_rank_to_value(self, cribbage_game):
        """Test conversion of card ranks to point values."""
        assert cribbage_game._rank_to_value("A") == 1
        assert cribbage_game._rank_to_value("2") == 2
        assert cribbage_game._rank_to_value("10") == 10
        assert cribbage_game._rank_to_value("J") == 10
        assert cribbage_game._rank_to_value("Q") == 10
        assert cribbage_game._rank_to_value("K") == 10

    def test_rank_to_ordered_numerical(self, cribbage_game):
        """Test conversion of card ranks to ordered numerical values."""
        assert cribbage_game._rank_to_ordered_numerical("A") == 1
        assert cribbage_game._rank_to_ordered_numerical("5") == 5
        assert cribbage_game._rank_to_ordered_numerical("10") == 10
        assert cribbage_game._rank_to_ordered_numerical("J") == 11
        assert cribbage_game._rank_to_ordered_numerical("Q") == 12
        assert cribbage_game._rank_to_ordered_numerical("K") == 13

    def test_score_15s(self, cribbage_game):
        """Test scoring for combinations that sum to 15."""
        # Test case: 5+10=15 (one combination of 15)
        cards = [Card("H", "5"), Card("S", "10")]
        assert cribbage_game._score_15s(cards) == 2

        # Test case: 5+5+5=15 (one combination of 15)
        cards = [Card("H", "5"), Card("S", "5"), Card("D", "5")]
        assert cribbage_game._score_15s(cards) == 2

        # Test case: A+4+10=15 and 4+J=15 (two combinations of 15)
        cards = [Card("H", "A"), Card("S", "4"),
                 Card("D", "10"), Card("C", "J")]
        assert cribbage_game._score_15s(cards) == 4

        # Test case: No combinations that sum to 15
        cards = [Card("H", "2"), Card("S", "3"), Card("D", "6")]
        assert cribbage_game._score_15s(cards) == 0

        # Test case: 5+10=15 and 5+J=15 and Q+5=15 (three combinations of 15)
        cards = [Card("H", "5"), Card("S", "10"),
                 Card("D", "J"), Card("C", "Q")]
        assert cribbage_game._score_15s(cards) == 6

    def test_score_pairs(self, cribbage_game):
        """Test scoring for pairs."""
        # Test case: One pair (2 points)
        cards = [Card("H", "5"), Card("S", "5")]
        assert cribbage_game._score_pairs(cards) == 2

        # Test case: Three of a kind (6 points - three pairs)
        cards = [Card("H", "5"), Card("S", "5"), Card("D", "5")]
        assert cribbage_game._score_pairs(cards) == 6

        # Test case: Four of a kind (12 points - six pairs)
        cards = [Card("H", "5"), Card("S", "5"),
                 Card("D", "5"), Card("C", "5")]
        assert cribbage_game._score_pairs(cards) == 12

        # Test case: Two different pairs (4 points)
        cards = [Card("H", "5"), Card("S", "5"),
                 Card("D", "J"), Card("C", "J")]
        assert cribbage_game._score_pairs(cards) == 4

        # Test case: No pairs
        cards = [Card("H", "2"), Card("S", "3"),
                 Card("D", "4"), Card("C", "5")]
        assert cribbage_game._score_pairs(cards) == 0

    def test_score_runs(self, cribbage_game):
        """Test scoring for runs."""
        # Test case: Simple run of 3 (3 points)
        cards = [Card("H", "A"), Card("S", "2"), Card("D", "3")]
        assert cribbage_game._score_runs(cards) == 3

        # Test case: Run of 4 (4 points)
        cards = [Card("H", "2"), Card("S", "3"),
                 Card("D", "4"), Card("C", "5")]
        assert cribbage_game._score_runs(cards) == 4

        # Test case: Run of 3 with a pair (6 points - double run)
        cards = [Card("H", "3"), Card("S", "3"),
                 Card("D", "4"), Card("C", "5")]
        assert cribbage_game._score_runs(cards) == 6

        # Test case: Run of 3 with two pairs (12 points - double double run)
        cards = [
            Card("H", "3"),
            Card("S", "3"),
            Card("D", "4"),
            Card("C", "4"),
            Card("H", "5"),
        ]
        assert cribbage_game._score_runs(cards) == 12

        # Test case: Run of 3 with a triple (9 points - triple run)
        cards = [
            Card("H", "3"),
            Card("S", "3"),
            Card("D", "3"),
            Card("C", "4"),
            Card("H", "5"),
        ]
        assert cribbage_game._score_runs(cards) == 9

        # Test case: Run of 4 with a pair (8 points)
        cards = [
            Card("H", "2"),
            Card("S", "3"),
            Card("D", "4"),
            Card("C", "4"),
            Card("H", "5"),
        ]
        assert cribbage_game._score_runs(cards) == 8

        # Test case: No run
        cards = [Card("H", "A"), Card("S", "3"),
                 Card("D", "5"), Card("C", "7")]
        assert cribbage_game._score_runs(cards) == 0

        # Test case: Run of 5 with specific sequence (5 points)
        cards = [
            Card("H", "5"),
            Card("S", "6"),
            Card("D", "7"),
            Card("C", "8"),
            Card("H", "9"),
        ]
        assert cribbage_game._score_runs(cards) == 5

        # Test case: Run of 5 (5 points)
        cards = [
            Card("H", "2"),
            Card("S", "3"),
            Card("D", "4"),
            Card("C", "5"),
            Card("H", "6"),
        ]
        assert cribbage_game._score_runs(cards) == 5

    def test_score_flush(self, cribbage_game):
        """Test scoring for flushes."""
        # Test case: 4-card flush in hand + matching cut card = 5 points
        hand = Hand()
        hand.draw(Card("H", "2"))
        hand.draw(Card("H", "5"))
        hand.draw(Card("H", "9"))
        hand.draw(Card("H", "K"))
        cut_card = Card("H", "A")
        assert cribbage_game._score_flush(hand, cut_card) == 5

        # Test case: 4-card flush in hand + non-matching cut card = 4 points
        hand = Hand()
        hand.draw(Card("H", "2"))
        hand.draw(Card("H", "5"))
        hand.draw(Card("H", "9"))
        hand.draw(Card("H", "K"))
        cut_card = Card("S", "A")
        assert cribbage_game._score_flush(hand, cut_card) == 4

        # Test case: Less than 4-card flush = 0 points
        hand = Hand()
        hand.draw(Card("H", "2"))
        hand.draw(Card("H", "5"))
        hand.draw(Card("H", "9"))
        hand.draw(Card("S", "K"))
        cut_card = Card("H", "A")
        assert cribbage_game._score_flush(hand, cut_card) == 0

        # Test case: 4-card flush in crib + matching cut card = 5 points
        hand = Hand()
        hand.draw(Card("H", "2"))
        hand.draw(Card("H", "5"))
        hand.draw(Card("H", "9"))
        hand.draw(Card("H", "K"))
        cut_card = Card("H", "A")
        assert cribbage_game._score_flush(hand, cut_card, crib=True) == 5

        # Test case: 4-card flush in crib + non-matching cut card = 0 points (crib specific rule)
        hand = Hand()
        hand.draw(Card("H", "2"))
        hand.draw(Card("H", "5"))
        hand.draw(Card("H", "9"))
        hand.draw(Card("H", "K"))
        cut_card = Card("S", "A")
        assert cribbage_game._score_flush(hand, cut_card, crib=True) == 0

    def test_score_nobs(self, cribbage_game):
        """Test scoring for nobs (jack of same suit as cut card)."""
        # Test case: Hand has jack of same suit as cut card = 1 point
        hand = Hand()
        hand.draw(Card("H", "J"))
        hand.draw(Card("S", "5"))
        hand.draw(Card("D", "9"))
        hand.draw(Card("C", "K"))
        cut_card = Card("H", "A")
        assert cribbage_game._score_nobs(hand, cut_card) == 1

        # Test case: Hand has jack of different suit than cut card = 0 points
        hand = Hand()
        hand.draw(Card("S", "J"))
        hand.draw(Card("S", "5"))
        hand.draw(Card("D", "9"))
        hand.draw(Card("C", "K"))
        cut_card = Card("H", "A")
        assert cribbage_game._score_nobs(hand, cut_card) == 0

        # Test case: Hand has no jack = 0 points
        hand = Hand()
        hand.draw(Card("H", "10"))
        hand.draw(Card("S", "5"))
        hand.draw(Card("D", "9"))
        hand.draw(Card("C", "K"))
        cut_card = Card("H", "A")
        assert cribbage_game._score_nobs(hand, cut_card) == 0

    def test_score_hand_complete(self, cribbage_game):
        """Test complete hand scoring with combinations of scoring elements."""
        # Test case 1: 5♥, 5♠, 5♦, J♣ with cut card 5♣
        # Score should include:
        # - Four of a kind (12 points)
        # - Four combinations of 15 (5+5+5=15 and combinations with J+5+5=15) (8 points minimum)
        # - Run with four 5s (additional points for quadruple run)
        hand = Hand()
        hand.draw(Card("H", "5"))
        hand.draw(Card("S", "5"))
        hand.draw(Card("D", "5"))
        hand.draw(Card("C", "J"))
        cut_card = Card("C", "5")
        # The expected score should be:
        # - 12 points for four of a kind (pairs)
        # - 8+ points for fifteens
        # - Potential additional points based on the implementation of _score_runs with four 5s
        assert cribbage_game.score_hand(hand, cut_card) == 29

        # Test case 2: 5♥, 6♠, 7♦, 8♣ with cut card 9♣
        # Score should include:
        # - Run of 5 (5 points)
        # - No 15s, no pairs, no flush, no nobs
        # - Total: 5 points
        hand = Hand()
        hand.draw(Card("H", "5"))
        hand.draw(Card("S", "6"))
        hand.draw(Card("D", "7"))
        hand.draw(Card("C", "8"))
        cut_card = Card("C", "9")
        assert cribbage_game.score_hand(hand, cut_card) == 9

        # Test case 3: A♥, A♠, 2♦, 2♣ with cut card 3♣
        # Score should include:
        # - Two pairs (4 points)
        # - Run of 3 with a pair of Aces and pair of 2s (12 points - double double run)
        # - No 15s, no flush, no nobs
        # - Total: 16 points
        hand = Hand()
        hand.draw(Card("H", "A"))
        hand.draw(Card("S", "A"))
        hand.draw(Card("D", "2"))
        hand.draw(Card("C", "2"))
        cut_card = Card("C", "3")
        assert cribbage_game.score_hand(hand, cut_card) == 16

        # Test case 4: 5♥, 5♠, 10♦, 10♣ with cut card J♣
        # Score should include:
        # - Two pairs (4 points)
        # - Four combinations of 15 (5+10, 5+10, 5+10, 5+10) (8 points)
        # - Total: 12 points
        hand = Hand()
        hand.draw(Card("H", "5"))
        hand.draw(Card("S", "5"))
        hand.draw(Card("D", "10"))
        hand.draw(Card("C", "10"))
        cut_card = Card("C", "J")

        total_score = cribbage_game.score_hand(hand, cut_card)

        # For clarity, let's calculate each component
        fifteens = cribbage_game._score_15s(hand.cards + [cut_card])
        pairs = cribbage_game._score_pairs(hand.cards + [cut_card])
        runs = cribbage_game._score_runs(hand.cards + [cut_card])
        flush = cribbage_game._score_flush(hand, cut_card)
        nobs = cribbage_game._score_nobs(hand, cut_card)

        expected_total = fifteens + pairs + runs + flush + nobs
        assert total_score == expected_total
        assert total_score == 16  # 4 for pairs + 12 for 15s (6 combinations)

