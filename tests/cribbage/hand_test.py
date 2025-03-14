import pytest
import io
from cribbage.cards import Card
from cribbage.hand import Hand


@pytest.fixture
def empty_hand():
    """Fixture that provides an empty hand for tests."""
    return Hand()


@pytest.fixture
def hand_with_cards():
    """Fixture that provides a hand with two cards."""
    hand = Hand()
    hand.draw(Card("K", "H"))
    hand.draw(Card("5", "S"))
    return hand


def test_init(empty_hand):
    """Test that a new hand initializes with an empty cards list."""
    assert len(empty_hand.cards) == 0
    assert empty_hand.cards == []


def test_draw(empty_hand):
    """Test that drawing a card adds it to the hand."""
    card = Card("K", "H")
    empty_hand.draw(card)
    assert len(empty_hand.cards) == 1
    assert empty_hand.cards[0] == card

    # Draw another card
    card2 = Card("5", "S")
    empty_hand.draw(card2)
    assert len(empty_hand.cards) == 2
    assert empty_hand.cards[1] == card2


def test_play(hand_with_cards):
    """Test that playing a card removes and returns it from hand."""
    # Get references to the cards
    card1 = hand_with_cards.cards[0]
    card2 = hand_with_cards.cards[1]

    # Play a card and check it's returned
    played_card = hand_with_cards.play(0)
    assert played_card == card1

    # Check that the card is removed from hand
    assert len(hand_with_cards.cards) == 1
    assert hand_with_cards.cards[0] == card2

    # Play the second card
    played_card = hand_with_cards.play(0)
    assert played_card == card2
    assert len(hand_with_cards.cards) == 0


def test_play_invalid_index(empty_hand):
    """Test that playing a card with invalid index raises an error."""
    card = Card("10", "S")
    empty_hand.draw(card)

    # Try to play with an invalid index
    with pytest.raises(IndexError):
        empty_hand.play(1)  # Only index 0 is valid

    with pytest.raises(IndexError):
        empty_hand.play(-2)  # Negative index out of range


def test_show_hand(hand_with_cards, monkeypatch, capsys):
    """Test that show_hand prints the correct representation of cards."""
    # Call show_hand and capture the output
    hand_with_cards.show_hand()
    captured = capsys.readouterr()
    expected_output = "0:KH\n1:5S\n"
    assert captured.out == expected_output

    # Test with empty hand
    empty_hand = Hand()  # Reset to empty hand
    empty_hand.show_hand()
    captured = capsys.readouterr()
    assert captured.out == ""  # No output for empty hand

