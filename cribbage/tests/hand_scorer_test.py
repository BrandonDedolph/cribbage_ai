import pytest
from cribbage.cards import Card, Deck
from cribbage.hand import Hand
from cribbage.hand_scorer import HandScorer


@pytest.fixture
def hand_scorer():
    """Fixture that provides a new HandScorer instance."""
    return HandScorer()


@pytest.fixture
def sample_hand():
    """Fixture that provides a hand with specific cards for testing scoring."""
    hand = Hand()
    hand.draw(Card("H", "5"))
    hand.draw(Card("S", "5"))
    hand.draw(Card("D", "5"))
    hand.draw(Card("C", "J"))
    return hand


class TestHandScorer:
    """Test suite for the HandScorer class."""

    class TestHelperMethods:
        """Tests for utility/helper methods in HandScorer."""

        def test_rank_to_value(self, hand_scorer):
            """Test conversion of card ranks to point values."""
            # Test numeric values
            assert hand_scorer._rank_to_value("A") == 1
            assert hand_scorer._rank_to_value("2") == 2
            assert hand_scorer._rank_to_value("9") == 9
            assert hand_scorer._rank_to_value("10") == 10

            # Test face cards
            assert hand_scorer._rank_to_value("J") == 10
            assert hand_scorer._rank_to_value("Q") == 10
            assert hand_scorer._rank_to_value("K") == 10

        def test_rank_to_ordered_numerical(self, hand_scorer):
            """Test conversion of card ranks to ordered numerical values."""
            # Test numeric values
            assert hand_scorer._rank_to_ordered_numerical("A") == 1
            assert hand_scorer._rank_to_ordered_numerical("5") == 5
            assert hand_scorer._rank_to_ordered_numerical("10") == 10

            # Test face cards
            assert hand_scorer._rank_to_ordered_numerical("J") == 11
            assert hand_scorer._rank_to_ordered_numerical("Q") == 12
            assert hand_scorer._rank_to_ordered_numerical("K") == 13

    class TestScoringComponents:
        """Tests for individual scoring component methods."""

        def test_score_15s(self, hand_scorer):
            """Test scoring for combinations that sum to 15."""
            # Single 15 with two cards
            cards = [Card("H", "5"), Card("S", "10")]
            assert hand_scorer._score_15s(cards) == 2

            # Single 15 with three cards
            cards = [Card("H", "5"), Card("S", "5"), Card("D", "5")]
            assert hand_scorer._score_15s(cards) == 2

            # Multiple 15s with different combinations
            cards = [Card("H", "A"), Card("S", "4"), Card("D", "10"), Card("C", "J")]
            assert hand_scorer._score_15s(cards) == 4

            # No 15s
            cards = [Card("H", "2"), Card("S", "3"), Card("D", "6")]
            assert hand_scorer._score_15s(cards) == 0

            # Multiple 15s with face cards
            cards = [Card("H", "5"), Card("S", "10"), Card("D", "J"), Card("C", "Q")]
            assert hand_scorer._score_15s(cards) == 6

            # Complex combination of 15s
            cards = [
                Card("H", "5"),
                Card("S", "7"),
                Card("D", "8"),
                Card("C", "J"),
                Card("D", "K"),
            ]
            assert hand_scorer._score_15s(cards) == 6

        def test_score_pairs(self, hand_scorer):
            """Test scoring for pairs."""
            # One pair (2 points)
            cards = [Card("H", "5"), Card("S", "5")]
            assert hand_scorer._score_pairs(cards) == 2

            # Three of a kind (6 points - three pairs)
            cards = [Card("H", "5"), Card("S", "5"), Card("D", "5")]
            assert hand_scorer._score_pairs(cards) == 6

            # Four of a kind (12 points - six pairs)
            cards = [Card("H", "5"), Card("S", "5"), Card("D", "5"), Card("C", "5")]
            assert hand_scorer._score_pairs(cards) == 12

            # Two different pairs (4 points)
            cards = [Card("H", "5"), Card("S", "5"), Card("D", "J"), Card("C", "J")]
            assert hand_scorer._score_pairs(cards) == 4

            # No pairs
            cards = [Card("H", "2"), Card("S", "3"), Card("D", "4"), Card("C", "5")]
            assert hand_scorer._score_pairs(cards) == 0

            # Multiple pairs with face cards
            cards = [Card("H", "Q"), Card("S", "Q"), Card("D", "K"), Card("C", "K")]
            assert hand_scorer._score_pairs(cards) == 4

        def test_score_runs(self, hand_scorer):
            """Test scoring for runs."""
            # Simple run of 3 (3 points)
            cards = [Card("H", "A"), Card("S", "2"), Card("D", "3")]
            assert hand_scorer._score_runs(cards) == 3

            # Run of 4 (4 points)
            cards = [Card("H", "2"), Card("S", "3"), Card("D", "4"), Card("C", "5")]
            assert hand_scorer._score_runs(cards) == 4

            # Run of 3 with a pair (6 points - double run)
            cards = [Card("H", "3"), Card("S", "3"), Card("D", "4"), Card("C", "5")]
            assert hand_scorer._score_runs(cards) == 6

            # Run of 3 with two pairs (12 points - double double run)
            cards = [
                Card("H", "3"),
                Card("S", "3"),
                Card("D", "4"),
                Card("C", "4"),
                Card("H", "5"),
            ]
            assert hand_scorer._score_runs(cards) == 12

            # Run of 3 with a triple (9 points - triple run)
            cards = [
                Card("H", "3"),
                Card("S", "3"),
                Card("D", "3"),
                Card("C", "4"),
                Card("H", "5"),
            ]
            assert hand_scorer._score_runs(cards) == 9

            # Run of 4 with a pair (8 points)
            cards = [
                Card("H", "2"),
                Card("S", "3"),
                Card("D", "4"),
                Card("C", "4"),
                Card("H", "5"),
            ]
            assert hand_scorer._score_runs(cards) == 8

            # No run
            cards = [Card("H", "A"), Card("S", "3"), Card("D", "5"), Card("C", "7")]
            assert hand_scorer._score_runs(cards) == 0

            # Run of 5 (5 points)
            cards = [
                Card("H", "5"),
                Card("S", "6"),
                Card("D", "7"),
                Card("C", "8"),
                Card("H", "9"),
            ]
            assert hand_scorer._score_runs(cards) == 5

            # Another run of 5 (5 points)
            cards = [
                Card("H", "2"),
                Card("S", "3"),
                Card("D", "4"),
                Card("C", "5"),
                Card("H", "6"),
            ]
            assert hand_scorer._score_runs(cards) == 5

            # Non-consecutive cards with face cards (no run)
            cards = [
                Card("H", "10"),
                Card("S", "J"),
                Card("D", "K"),
                Card("C", "A"),
            ]
            assert hand_scorer._score_runs(cards) == 0

            # Run with face cards
            cards = [
                Card("H", "10"),
                Card("S", "J"),
                Card("D", "Q"),
                Card("C", "K"),
            ]
            assert hand_scorer._score_runs(cards) == 4

        def test_score_flush(self, hand_scorer):
            """Test scoring for flushes."""
            # 4-card flush in hand + matching cut card = 5 points
            hand = Hand()
            hand.draw(Card("H", "2"))
            hand.draw(Card("H", "5"))
            hand.draw(Card("H", "9"))
            hand.draw(Card("H", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_flush(hand, cut_card) == 5

            # 4-card flush in hand + non-matching cut card = 4 points
            hand = Hand()
            hand.draw(Card("H", "2"))
            hand.draw(Card("H", "5"))
            hand.draw(Card("H", "9"))
            hand.draw(Card("H", "K"))
            cut_card = Card("S", "A")
            assert hand_scorer._score_flush(hand, cut_card) == 4

            # Less than 4-card flush = 0 points
            hand = Hand()
            hand.draw(Card("H", "2"))
            hand.draw(Card("H", "5"))
            hand.draw(Card("H", "9"))
            hand.draw(Card("S", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_flush(hand, cut_card) == 0

            # 4-card flush in crib + matching cut card = 5 points
            hand = Hand()
            hand.draw(Card("H", "2"))
            hand.draw(Card("H", "5"))
            hand.draw(Card("H", "9"))
            hand.draw(Card("H", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_flush(hand, cut_card, crib=True) == 5

            # 4-card flush in crib + non-matching cut card = 0 points (crib specific rule)
            hand = Hand()
            hand.draw(Card("H", "2"))
            hand.draw(Card("H", "5"))
            hand.draw(Card("H", "9"))
            hand.draw(Card("H", "K"))
            cut_card = Card("S", "A")
            assert hand_scorer._score_flush(hand, cut_card, crib=True) == 0

        def test_score_nobs(self, hand_scorer):
            """Test scoring for nobs (jack of same suit as cut card)."""
            # Hand has jack of same suit as cut card = 1 point
            hand = Hand()
            hand.draw(Card("H", "J"))
            hand.draw(Card("S", "5"))
            hand.draw(Card("D", "9"))
            hand.draw(Card("C", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_nobs(hand, cut_card) == 1

            # Hand has jack of different suit than cut card = 0 points
            hand = Hand()
            hand.draw(Card("S", "J"))
            hand.draw(Card("S", "5"))
            hand.draw(Card("D", "9"))
            hand.draw(Card("C", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_nobs(hand, cut_card) == 0

            # Hand has no jack = 0 points
            hand = Hand()
            hand.draw(Card("H", "10"))
            hand.draw(Card("S", "5"))
            hand.draw(Card("D", "9"))
            hand.draw(Card("C", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_nobs(hand, cut_card) == 0

            # Multiple jacks but none matching cut card suit
            hand = Hand()
            hand.draw(Card("S", "J"))
            hand.draw(Card("D", "J"))
            hand.draw(Card("C", "J"))
            hand.draw(Card("S", "5"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_nobs(hand, cut_card) == 0

            # Multiple jacks including one matching cut card suit
            hand = Hand()
            hand.draw(Card("H", "J"))
            hand.draw(Card("S", "J"))
            hand.draw(Card("D", "9"))
            hand.draw(Card("C", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer._score_nobs(hand, cut_card) == 1

    class TestCompleteHandScoring:
        """Tests for complete hand scoring."""

        def test_score_hand_with_various_combinations(self, hand_scorer):
            """Test complete hand scoring with various combinations of cards."""
            # Test case 1: Four of a kind with a face card
            hand = Hand()
            hand.draw(Card("H", "5"))
            hand.draw(Card("S", "5"))
            hand.draw(Card("D", "5"))
            hand.draw(Card("C", "J"))
            cut_card = Card("C", "5")
            assert hand_scorer.score_hand(hand, cut_card) == 29

            # Test case 2: Run of 5
            hand = Hand()
            hand.draw(Card("H", "5"))
            hand.draw(Card("S", "6"))
            hand.draw(Card("D", "7"))
            hand.draw(Card("C", "8"))
            cut_card = Card("C", "9")
            assert hand_scorer.score_hand(hand, cut_card) == 9

            # Test case 3: Double double run
            hand = Hand()
            hand.draw(Card("H", "A"))
            hand.draw(Card("S", "A"))
            hand.draw(Card("D", "2"))
            hand.draw(Card("C", "2"))
            cut_card = Card("C", "3")
            assert hand_scorer.score_hand(hand, cut_card) == 16

            # Test case 4: Two pairs with several 15s
            hand = Hand()
            hand.draw(Card("H", "5"))
            hand.draw(Card("S", "5"))
            hand.draw(Card("D", "10"))
            hand.draw(Card("C", "10"))
            cut_card = Card("C", "J")
            assert hand_scorer.score_hand(hand, cut_card) == 16

            # Test case 5: Four of a kind with 15s
            hand = Hand()
            hand.draw(Card("H", "K"))
            hand.draw(Card("S", "K"))
            hand.draw(Card("D", "K"))
            hand.draw(Card("C", "K"))
            cut_card = Card("C", "5")
            assert hand_scorer.score_hand(hand, cut_card) == 20

            # Test case 6: Flush with run and nobs
            hand = Hand()
            hand.draw(Card("H", "10"))
            hand.draw(Card("H", "J"))
            hand.draw(Card("H", "Q"))
            hand.draw(Card("H", "K"))
            cut_card = Card("H", "A")
            assert hand_scorer.score_hand(hand, cut_card) == 10

            # Test case 7: Perfect 29-point hand
            hand = Hand()
            hand.draw(Card("H", "5"))
            hand.draw(Card("D", "5"))
            hand.draw(Card("C", "5"))
            hand.draw(Card("S", "J"))
            cut_card = Card("S", "5")
            assert hand_scorer.score_hand(hand, cut_card) == 29

            # Test case 8: Mixed scoring elements
            hand = Hand(
                [
                    Card("H", "5"),
                    Card("S", "6"),
                    Card("D", "J"),
                    Card("S", "4"),
                ]
            )
            cut_card = Card("H", "2")
            assert hand_scorer._score_15s(hand.cards + [cut_card]) == 4
            assert hand_scorer._score_runs(hand.cards + [cut_card]) == 3
            assert hand_scorer.score_hand(hand, cut_card) == 7

        def test_score_hand_detailed_calculation(self, hand_scorer):
            """Test that the sum of individual components equals total score."""
            # Create a hand with multiple scoring elements
            hand = Hand()
            hand.draw(Card("H", "5"))
            hand.draw(Card("S", "5"))
            hand.draw(Card("D", "10"))
            hand.draw(Card("C", "10"))
            cut_card = Card("C", "J")

            # Get total score
            total_score = hand_scorer.score_hand(hand, cut_card)

            # Calculate each component
            fifteens = hand_scorer._score_15s(hand.cards + [cut_card])
            pairs = hand_scorer._score_pairs(hand.cards + [cut_card])
            runs = hand_scorer._score_runs(hand.cards + [cut_card])
            flush = hand_scorer._score_flush(hand, cut_card)
            nobs = hand_scorer._score_nobs(hand, cut_card)

            # Verify components add up to total
            expected_total = fifteens + pairs + runs + flush + nobs
            assert total_score == expected_total
            assert total_score == 16  # 4 for pairs + 12 for 15s

        def test_score_hand_crib(self, hand_scorer):
            """Test hand scoring with crib-specific rules."""
            # 4-card flush in crib + non-matching cut card = 0 points
            hand = Hand()
            hand.draw(Card("H", "2"))
            hand.draw(Card("H", "5"))
            hand.draw(Card("H", "9"))
            hand.draw(Card("H", "K"))
            cut_card = Card("S", "A")
            # Note: Possible bug in _score_flush
            assert hand_scorer.score_hand(hand, cut_card, crib=True) == 4

            # 4-card flush in crib + matching cut card = 5 points (plus any other points)
            hand = Hand()
            hand.draw(Card("H", "2"))
            hand.draw(Card("H", "5"))
            hand.draw(Card("H", "9"))
            hand.draw(Card("H", "K"))
            cut_card = Card("H", "A")
            # Should have 5 for flush and 4 for other combinations
            assert hand_scorer.score_hand(hand, cut_card, crib=True) == 9
