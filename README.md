# Cribbage AI

A Python implementation of the classic card game Cribbage.

## Overview

This project provides a programmatic implementation of Cribbage, including card management, hand scoring, and game mechanics. It's designed to be modular, extensible, and thoroughly tested.

## Features

- Complete card deck management (shuffling, drawing, etc.)
- Cribbage hand representation and manipulation
- Comprehensive scoring system implementing official Cribbage rules:
  - Fifteen combinations (2 points each)
  - Pairs (2 points per pair)
  - Runs of 3 or more consecutive cards
  - Flushes (4 or 5 points)
  - "One for his nob" (Jack of same suit as starter card)
- Support for standard 2-player Cribbage games

## Installation

### Using Poetry (recommended)

```bash
# Clone the repository
git clone git@github.com:BrandonDedolph/cribbage_ai.git
cd cribbage_ai

# Install dependencies with Poetry
poetry install
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/cribbage.git
cd cribbage

# Install the package
pip install -e .
```

## Usage

```python
from cribbage.cards import Card, Deck
from cribbage.hand import Hand
from cribbage.cribbage import Cribbage

# Initialize a new game
game = Cribbage()

# Create and populate hands
player_hand = Hand()
player_hand.draw(Card("H", "5"))
player_hand.draw(Card("S", "5"))
player_hand.draw(Card("D", "5"))
player_hand.draw(Card("C", "J"))

# Draw a cut card
cut_card = Card("C", "5")

# Score a hand
score = game.score_hand(player_hand, cut_card)
print(f"Hand score: {score}")

# Show the contents of a hand
player_hand.show_hand()
```

## Cribbage Scoring

Cribbage scoring follows standard rules:

| Combination | Points |
|-------------|--------|
| Fifteens (sum of cards = 15) | 2 points each |
| Pairs | 2 points per pair |
| Three of a kind | 6 points (3 pairs) |
| Four of a kind | 12 points (6 pairs) |
| Run of 3 | 3 points |
| Run of 4 | 4 points |
| Run of 5 | 5 points |
| Flush (all cards in hand same suit) | 4 points |
| Flush (all cards in hand + cut card same suit) | 5 points |
| Nobs (Jack of same suit as cut card) | 1 point |

## Development

### Prerequisites

- Python 3.13 or higher
- Poetry (for dependency management)

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest -v tests/cards_test.py
```

### Project Structure

```
cribbage/
├── cribbage/
│   ├── __init__.py
│   ├── cards.py       # Card and Deck classes
│   ├── hand.py        # Hand class for managing cards
│   └── cribbage.py    # Main game logic and scoring
├── tests/
│   ├── cards_test.py  # Tests for Card and Deck classes
│   ├── hand_test.py   # Tests for Hand class
│   └── cribbage_test.py  # Tests for Cribbage class and scoring
├── pyproject.toml     # Poetry configuration
└── setup.py          # Package installation
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
