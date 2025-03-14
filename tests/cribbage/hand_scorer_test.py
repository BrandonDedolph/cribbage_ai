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
    hand.draw(Card("5", "H"))
    hand.draw(Card("5", "S"))
    hand.draw(Card("5", "D"))
    hand.draw(Card("J", "C"))
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
            cards = [Card("5", "H"), Card("10", "S")]
            assert hand_scorer._score_15s(cards) == 2

            # Single 15 with three cards
            cards = [Card("5", "H"), Card("5", "S"), Card("5", "D")]
            assert hand_scorer._score_15s(cards) == 2

            # Multiple 15s with different combinations
            cards = [Card("A", "H"), Card("4", "S"), Card("10", "D"), Card("J", "C")]
            assert hand_scorer._score_15s(cards) == 4

            # No 15s
            cards = [Card("2", "H"), Card("3", "S"), Card("6", "D")]
            assert hand_scorer._score_15s(cards) == 0

            # Multiple 15s with face cards
            cards = [Card("5", "H"), Card("10", "S"), Card("J", "D"), Card("Q", "C")]
            assert hand_scorer._score_15s(cards) == 6

            # Complex combination of 15s
            cards = [
                Card("5", "H"),
                Card("7", "S"),
                Card("8", "D"),
                Card("J", "C"),
                Card("K", "D"),
            ]
            assert hand_scorer._score_15s(cards) == 6

        def test_score_pairs(self, hand_scorer):
            """Test scoring for pairs."""
            # One pair (2 points)
            cards = [Card("5", "H"), Card("5", "S")]
            assert hand_scorer._score_pairs(cards) == 2

            # Three of a kind (6 points - three pairs)
            cards = [Card("5", "H"), Card("5", "S"), Card("5", "D")]
            assert hand_scorer._score_pairs(cards) == 6

            # Four of a kind (12 points - six pairs)
            cards = [Card("5", "H"), Card("5", "S"), Card("5", "D"), Card("5", "C")]
            assert hand_scorer._score_pairs(cards) == 12

            # Two different pairs (4 points)
            cards = [Card("5", "H"), Card("5", "S"), Card("J", "D"), Card("J", "C")]
            assert hand_scorer._score_pairs(cards) == 4

            # No pairs
            cards = [Card("2", "H"), Card("3", "S"), Card("4", "D"), Card("5", "C")]
            assert hand_scorer._score_pairs(cards) == 0

            # Multiple pairs with face cards
            cards = [Card("Q", "H"), Card("Q", "S"), Card("K", "D"), Card("K", "C")]
            assert hand_scorer._score_pairs(cards) == 4

        def test_score_runs(self, hand_scorer):
            """Test scoring for runs."""
            # Simple run of 3 (3 points)
            cards = [Card("A", "H"), Card("2", "S"), Card("3", "D")]
            assert hand_scorer._score_runs(cards) == 3

            # Run of 4 (4 points)
            cards = [Card("2", "H"), Card("3", "S"), Card("4", "D"), Card("5", "C")]
            assert hand_scorer._score_runs(cards) == 4

            # Run of 3 with a pair (6 points - double run)
            cards = [Card("3", "H"), Card("3", "S"), Card("4", "D"), Card("5", "C")]
            assert hand_scorer._score_runs(cards) == 6

            # Run of 3 with two pairs (12 points - double double run)
            cards = [
                Card("3", "H"),
                Card("3", "S"),
                Card("4", "D"),
                Card("4", "C"),
                Card("5", "H"),
            ]
            assert hand_scorer._score_runs(cards) == 12

            # Run of 3 with a triple (9 points - triple run)
            cards = [
                Card("3", "H"),
                Card("3", "S"),
                Card("3", "D"),
                Card("4", "C"),
                Card("5", "H"),
            ]
            assert hand_scorer._score_runs(cards) == 9

            # Run of 4 with a pair (8 points)
            cards = [
                Card("2", "H"),
                Card("3", "S"),
                Card("4", "D"),
                Card("4", "C"),
                Card("5", "H"),
            ]
            assert hand_scorer._score_runs(cards) == 8

            # No run
            cards = [Card("A", "H"), Card("3", "S"), Card("5", "D"), Card("7", "C")]
            assert hand_scorer._score_runs(cards) == 0

            # Run of 5 (5 points)
            cards = [
                Card("5", "H"),
                Card("6", "S"),
                Card("7", "D"),
                Card("8", "C"),
                Card("9", "H"),
            ]
            assert hand_scorer._score_runs(cards) == 5

            # Another run of 5 (5 points)
            cards = [
                Card("2", "H"),
                Card("3", "S"),
                Card("4", "D"),
                Card("5", "C"),
                Card("6", "H"),
            ]
            assert hand_scorer._score_runs(cards) == 5

            # Non-consecutive cards with face cards (no run)
            cards = [
                Card("10", "H"),
                Card("J", "S"),
                Card("K", "D"),
                Card("A", "C"),
            ]
            assert hand_scorer._score_runs(cards) == 0

            # Run with face cards
            cards = [
                Card("10", "H"),
                Card("J", "S"),
                Card("Q", "D"),
                Card("K", "C"),
            ]
            assert hand_scorer._score_runs(cards) == 4

        def test_score_flush(self, hand_scorer):
            """Test scoring for flushes."""
            # 4-card flush in hand + matching cut card = 5 points
            hand = Hand()
            hand.draw(Card("2", "H"))
            hand.draw(Card("5", "H"))
            hand.draw(Card("9", "H"))
            hand.draw(Card("K", "H"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_flush(hand, cut_card) == 5

            # 4-card flush in hand + non-matching cut card = 4 points
            hand = Hand()
            hand.draw(Card("2", "H"))
            hand.draw(Card("5", "H"))
            hand.draw(Card("9", "H"))
            hand.draw(Card("K", "H"))
            cut_card = Card("A", "S")
            assert hand_scorer._score_flush(hand, cut_card) == 4

            # Less than 4-card flush = 0 points
            hand = Hand()
            hand.draw(Card("2", "H"))
            hand.draw(Card("5", "H"))
            hand.draw(Card("9", "H"))
            hand.draw(Card("K", "S"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_flush(hand, cut_card) == 0

            # 4-card flush in crib + matching cut card = 5 points
            hand = Hand()
            hand.draw(Card("2", "H"))
            hand.draw(Card("5", "H"))
            hand.draw(Card("9", "H"))
            hand.draw(Card("K", "H"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_flush(hand, cut_card, crib=True) == 5

            # 4-card flush in crib + non-matching cut card = 0 points (crib specific rule)
            hand = Hand()
            hand.draw(Card("2", "H"))
            hand.draw(Card("5", "H"))
            hand.draw(Card("9", "H"))
            hand.draw(Card("K", "H"))
            cut_card = Card("A", "S")
            assert hand_scorer._score_flush(hand, cut_card, crib=True) == 0

        def test_score_nobs(self, hand_scorer):
            """Test scoring for nobs (jack of same suit as cut card)."""
            # Hand has jack of same suit as cut card = 1 point
            hand = Hand()
            hand.draw(Card("J", "H"))
            hand.draw(Card("5", "S"))
            hand.draw(Card("9", "D"))
            hand.draw(Card("K", "C"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_nobs(hand, cut_card) == 1

            # Hand has jack of different suit than cut card = 0 points
            hand = Hand()
            hand.draw(Card("J", "S"))
            hand.draw(Card("5", "S"))
            hand.draw(Card("9", "D"))
            hand.draw(Card("K", "C"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_nobs(hand, cut_card) == 0

            # Hand has no jack = 0 points
            hand = Hand()
            hand.draw(Card("10", "H"))
            hand.draw(Card("5", "S"))
            hand.draw(Card("9", "D"))
            hand.draw(Card("K", "C"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_nobs(hand, cut_card) == 0

            # Multiple jacks but none matching cut card suit
            hand = Hand()
            hand.draw(Card("J", "S"))
            hand.draw(Card("J", "D"))
            hand.draw(Card("J", "C"))
            hand.draw(Card("5", "S"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_nobs(hand, cut_card) == 0

            # Multiple jacks including one matching cut card suit
            hand = Hand()
            hand.draw(Card("J", "H"))
            hand.draw(Card("J", "S"))
            hand.draw(Card("9", "D"))
            hand.draw(Card("K", "C"))
            cut_card = Card("A", "H")
            assert hand_scorer._score_nobs(hand, cut_card) == 1

    class TestCompleteHandScoring:
        """Tests for complete hand scoring."""

        def test_score_hand_with_various_combinations(self, hand_scorer):
            """Test complete hand scoring with various combinations of cards."""
            # Test case 1: Four of a kind with a face card
            hand = Hand()
            hand.draw(Card("5", "H"))
            hand.draw(Card("5", "S"))
            hand.draw(Card("5", "D"))
            hand.draw(Card("J", "C"))
            cut_card = Card("5", "C")
            assert hand_scorer.score_hand(hand, cut_card) == 29

            # Test case 2: Run of 5
            hand = Hand()
            hand.draw(Card("5", "H"))
            hand.draw(Card("6", "S"))
            hand.draw(Card("7", "D"))
            hand.draw(Card("8", "C"))
            cut_card = Card("9", "C")
            assert hand_scorer.score_hand(hand, cut_card) == 9

            # Test case 3: Double double run
            hand = Hand()
            hand.draw(Card("A", "H"))
            hand.draw(Card("A", "S"))
            hand.draw(Card("2", "D"))
            hand.draw(Card("2", "C"))
            cut_card = Card("3", "C")
            assert hand_scorer.score_hand(hand, cut_card) == 16

            # Test case 4: Two pairs with several 15s
            hand = Hand()
            hand.draw(Card("5", "H"))
            hand.draw(Card("5", "S"))
            hand.draw(Card("10", "D"))
            hand.draw(Card("10", "C"))
            cut_card = Card("J", "C")
            assert hand_scorer.score_hand(hand, cut_card) == 16

            # Test case 5: Four of a kind with 15s
            hand = Hand()
            hand.draw(Card("K", "H"))
            hand.draw(Card("K", "S"))
            hand.draw(Card("K", "D"))
            hand.draw(Card("K", "C"))
            cut_card = Card("5", "C")
            assert hand_scorer.score_hand(hand, cut_card) == 20

            # Test case 6: Flush with run and nobs
            hand = Hand()
            hand.draw(Card("10", "H"))
            hand.draw(Card("J", "H"))
            hand.draw(Card("Q", "H"))
            hand.draw(Card("K", "H"))
            cut_card = Card("A", "H")
            assert hand_scorer.score_hand(hand, cut_card) == 10

            # Test case 7: Perfect 29-point hand
            hand = Hand()
            hand.draw(Card("5", "H"))
            hand.draw(Card("5", "D"))
            hand.draw(Card("5", "C"))
            hand.draw(Card("J", "S"))
            cut_card = Card("5", "S")
            assert hand_scorer.score_hand(hand, cut_card) == 29

            # Test case 8: Mixed scoring elements
            hand = Hand(
                [
                    Card("5", "H"),
                    Card("6", "S"),
                    Card("J", "D"),
                    Card("4", "S"),
                ]
            )
            cut_card = Card("2", "H")
            assert hand_scorer._score_15s(hand.cards + [cut_card]) == 4
            assert hand_scorer._score_runs(hand.cards + [cut_card]) == 3
            assert hand_scorer.score_hand(hand, cut_card) == 7

        def test_score_hand_detailed_calculation(self, hand_scorer):
            """Test that the sum of individual components equals total score."""
            # Create a hand with multiple scoring elements
            hand = Hand()
            hand.draw(Card("5", "H"))
            hand.draw(Card("5", "S"))
            hand.draw(Card("10", "D"))
            hand.draw(Card("10", "C"))
            cut_card = Card("J", "C")

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
            hand.draw(Card("2", "H"))
            hand.draw(Card("5", "H"))
            hand.draw(Card("9", "H"))
            hand.draw(Card("K", "H"))
            cut_card = Card("A", "S")
            # Note: Possible bug in _score_flush
            assert hand_scorer.score_hand(hand, cut_card, crib=True) == 4

            # 4-card flush in crib + matching cut card = 5 points (plus any other points)
            hand = Hand()
            hand.draw(Card("2", "H"))
            hand.draw(Card("5", "H"))
            hand.draw(Card("9", "H"))
            hand.draw(Card("K", "H"))
            cut_card = Card("A", "H")
            # Should have 5 for flush and 4 for other combinations
            assert hand_scorer.score_hand(hand, cut_card, crib=True) == 9

