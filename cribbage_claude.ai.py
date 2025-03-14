import random
from collections import Counter
from itertools import combinations
import os
import time
import sys

try:
    from colorama import Fore, Back, Style, init
except ImportError:
    print("Colorama not found. Installing...")
    try:
        import pip

        pip.main(["install", "colorama"])
        from colorama import Fore, Back, Style, init
    except:
        # Fallback if colorama can't be installed
        class DummyColor:
            def __getattr__(self, name):
                return ""

        Fore = Back = Style = DummyColor()

        def init(autoreset=True):
            pass


# Initialize colorama
init(autoreset=True)


class Card:
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS = ["♥", "♦", "♣", "♠"]
    SUIT_COLORS = {"♥": Fore.RED, "♦": Fore.RED, "♣": Fore.WHITE, "♠": Fore.WHITE}
    SUIT_NAMES = {"♥": "Hearts", "♦": "Diamonds", "♣": "Clubs", "♠": "Spades"}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        if self.rank == "A":
            return 1
        elif self.rank in ["J", "Q", "K"]:
            return 10
        else:
            return int(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def colored_str(self):
        return f"{self.rank}{self.SUIT_COLORS[self.suit]}{self.suit}{Style.RESET_ALL}"

    def display_name(self):
        return f"{self.rank} of {self.SUIT_NAMES[self.suit]}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))


class CardDisplay:
    @staticmethod
    def card_to_lines(card):
        """Convert a card to a list of strings representing card lines"""
        rank = card.rank if len(card.rank) < 3 else card.rank[0]
        color = Card.SUIT_COLORS[card.suit]
        colored_suit = f"{color}{card.suit}{Style.RESET_ALL}"
        lines = []
        lines.append(f"┌───────┐")
        lines.append(f"│{rank:<2}     │")
        lines.append(f"│       │")
        lines.append(f"│   {colored_suit}   │")
        lines.append(f"│       │")
        lines.append(f"│     {rank:>2}│")
        lines.append(f"└───────┘")
        return lines

    @staticmethod
    def display_cards(cards, indices=True):
        """Display cards side by side with optional indices"""
        if not cards:
            return

        card_lines = [CardDisplay.card_to_lines(card) for card in cards]

        # Add indices if requested
        if indices:
            idx_lines = []
            for i in range(len(cards)):
                idx_str = f"  [{i}]   "
                idx_lines.append(idx_str)

            # Print indices
            print("".join(idx_lines))

        # Print cards
        for i in range(7):  # 7 lines per card
            print("".join(card_lines[j][i] for j in range(len(cards))))


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left in the deck")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards


class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.hand = []
        self.is_ai = is_ai
        self.score = 0
        self.play_cards = []
        self.avatar = (
            self._generate_avatar() if not is_ai else self._generate_ai_avatar()
        )

    def _generate_avatar(self):
        """Generate a random ASCII avatar for the player"""
        avatars = [
            f"{Fore.GREEN}(ᵔᴥᵔ){Style.RESET_ALL}",
            f"{Fore.BLUE}(◕‿◕){Style.RESET_ALL}",
            f"{Fore.YELLOW}(•◡•){Style.RESET_ALL}",
            f"{Fore.MAGENTA}(◠‿◠){Style.RESET_ALL}",
            f"{Fore.CYAN}(｡◕‿◕｡){Style.RESET_ALL}",
        ]
        return random.choice(avatars)

    def _generate_ai_avatar(self):
        """Generate an AI-specific avatar"""
        ai_avatars = [
            f"{Fore.RED}[◉_◉]{Style.RESET_ALL}",
            f"{Fore.RED}[⚙_⚙]{Style.RESET_ALL}",
            f"{Fore.RED}[҉_҉]{Style.RESET_ALL}",
        ]
        return random.choice(ai_avatars)

    def add_cards(self, cards):
        self.hand.extend(cards)

    def discard_to_crib(self, card_indices):
        if len(card_indices) > len(self.hand):
            raise ValueError("Cannot discard more cards than in hand")

        # Sort indices in descending order to avoid index shifting
        card_indices = sorted(card_indices, reverse=True)
        discarded = []

        for idx in card_indices:
            if idx < 0 or idx >= len(self.hand):
                raise ValueError(f"Invalid card index: {idx}")
            discarded.append(self.hand.pop(idx))

        return discarded

    def reset_play_cards(self):
        self.play_cards = self.hand.copy()


class CribbageBoard:
    def __init__(self, player1, player2, target_score=121):
        self.players = [player1, player2]
        self.target_score = target_score
        self.board_length = 60  # Visual length of the board

    def display(self):
        """Display the cribbage board with current scores"""
        scale_factor = self.board_length / self.target_score

        # Convert scores to board positions
        positions = [
            min(int(player.score * scale_factor), self.board_length)
            for player in self.players
        ]

        print(f"\n{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}CRIBBAGE BOARD{Style.RESET_ALL}")

        # Player 1 track
        p1_track = ["_"] * self.board_length
        if positions[0] > 0:
            p1_track[positions[0] - 1] = f"{Fore.GREEN}⬤{Style.RESET_ALL}"
        p1_display = "".join(p1_track)
        print(f"{self.players[0].avatar} {Fore.GREEN}{self.players[0].name}{
              Style.RESET_ALL} [{self.players[0].score}]")
        print(f"[S]{''.join(p1_track)}[E]")

        # Player 2 track
        p2_track = ["_"] * self.board_length
        if positions[1] > 0:
            p2_track[positions[1] - 1] = f"{Fore.RED}⬤{Style.RESET_ALL}"
        p2_display = "".join(p2_track)
        print(f"{self.players[1].avatar} {Fore.RED}{self.players[1].name}{
              Style.RESET_ALL} [{self.players[1].score}]")
        print(f"[S]{''.join(p2_track)}[E]")

        print(f"{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}\n")


class CribbageGame:
    def __init__(
        self,
        player1_name="Player 1",
        player2_name="Player 2",
        target_score=121,
        player2_is_ai=True,
    ):
        self.players = [Player(player1_name), Player(player2_name, is_ai=player2_is_ai)]
        self.target_score = target_score
        self.board = CribbageBoard(self.players[0], self.players[1], target_score)
        self.deck = None
        self.starter_card = None
        self.crib = []
        self.dealer_idx = None
        self.current_player_idx = None
        self.play_pile = []
        self.play_count = 0
        self.game_over = False
        self.winner = None
        self.round_number = 1

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def slow_print(self, text, delay=0.03):
        """Print text with a typing effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def print_logo(self):
        """Display the game logo"""
        logo = f"""
{Fore.YELLOW}  _____       _ _     _
{Fore.YELLOW} / ____|     (_) |   | |
{Fore.YELLOW}| |     _ __  _| |__ | |__   __ _  __ _  ___
{Fore.YELLOW}| |    | '_ \\| | '_ \\| '_ \\ / _` |/ _` |/ _ \\
{Fore.YELLOW}| |____| |_) | | |_) | |_) | (_| | (_| |  __/
{Fore.YELLOW} \\_____| .__/|_|_.__/|_.__/ \\__,_|\\__, |\\___|
{Fore.YELLOW}       | |                         __/ |
{Fore.YELLOW}       |_|                        |___/
{Style.RESET_ALL}"""
        print(logo)

    def display_announcement(self, text):
        """Display a highlighted announcement"""
        width = 60
        padding = (width - len(text)) // 2
        print(f"\n{Fore.BLACK}{Back.YELLOW}{' ' * width}{Style.RESET_ALL}")
        print(f"{Fore.BLACK}{Back.YELLOW}{' ' * padding}{text}{' ' *
              (width - len(text) - padding)}{Style.RESET_ALL}")
        print(f"{Fore.BLACK}{Back.YELLOW}{' ' * width}{Style.RESET_ALL}\n")
        time.sleep(1)

    def start_game(self):
        """Initialize the game by determining the dealer."""
        self.clear_screen()
        self.print_logo()
        self.slow_print(f"{Fore.CYAN}Welcome to the game of Cribbage!{
                        Style.RESET_ALL}")
        self.slow_print(f"First to {self.target_score} points wins.")
        time.sleep(1)

        self.deck = Deck()
        # Players cut for deal - low card deals
        self.display_announcement("CUTTING FOR DEAL")
        cuts = [self.deck.deal(1)[0] for _ in range(2)]

        print(f"{self.players[0].avatar} {Fore.GREEN}{self.players[0].name}{
              Style.RESET_ALL} cuts: {cuts[0].colored_str()}")
        time.sleep(0.5)
        print(f"{self.players[1].avatar} {Fore.RED}{self.players[1].name}{
              Style.RESET_ALL} cuts: {cuts[1].colored_str()}")
        time.sleep(0.5)

        # In case of tie, re-cut
        while cuts[0].get_value() == cuts[1].get_value():
            self.slow_print(f"{Fore.YELLOW}Tie! Cutting again...{
                            Style.RESET_ALL}")
            time.sleep(0.5)
            self.deck = Deck()
            cuts = [self.deck.deal(1)[0] for _ in range(2)]
            print(f"{self.players[0].avatar} {Fore.GREEN}{self.players[0].name}{
                  Style.RESET_ALL} cuts: {cuts[0].colored_str()}")
            time.sleep(0.5)
            print(f"{self.players[1].avatar} {Fore.RED}{self.players[1].name}{
                  Style.RESET_ALL} cuts: {cuts[1].colored_str()}")
            time.sleep(0.5)

        # Lower card deals first
        self.dealer_idx = 0 if cuts[0].get_value() < cuts[1].get_value() else 1
        dealer = self.players[self.dealer_idx]
        self.slow_print(f"\n{dealer.avatar} {Fore.CYAN}{dealer.name}{
                        Style.RESET_ALL} will deal first")
        time.sleep(1)

        input(f"\n{Fore.YELLOW}Press Enter to begin the game...{
              Style.RESET_ALL}")

        # Start the first round
        self.play_round()

    def play_round(self):
        """Play a full round of cribbage."""
        if self.game_over:
            return

        self.clear_screen()
        self.board.display()

        dealer = self.players[self.dealer_idx]
        self.display_announcement(f"ROUND {self.round_number}: {dealer.name} DEALS")

        # Reset variables for new round
        self.deck = Deck()
        self.crib = []
        self.play_pile = []
        self.play_count = 0

        # Deal 6 cards to each player with animation
        self.slow_print(f"{Fore.CYAN}Dealing cards...{Style.RESET_ALL}")
        time.sleep(0.5)

        for player in self.players:
            player.hand = []
            player.add_cards(self.deck.deal(6))
            if not player.is_ai:
                self._display_hand(player)

        # Both players discard 2 cards to the crib
        self._discard_phase()
        if self.game_over:
            return

        # Cut for starter card with animation
        self.display_announcement("CUTTING FOR STARTER CARD")
        time.sleep(0.5)

        self.starter_card = self.deck.deal(1)[0]
        print(f"The starter card is:")
        time.sleep(0.5)
        CardDisplay.display_cards([self.starter_card], indices=False)

        # Check for his heels (nibs) - Jack as starter gives dealer 2 points
        if self.starter_card.rank == "J":
            self.display_announcement(f"HIS HEELS! {dealer.name} gets 2 points")
            self._add_score(self.dealer_idx, 2, "His Heels")
            if self.game_over:
                return

        input(f"\n{Fore.YELLOW}Press Enter to continue to 'The Play'...{
              Style.RESET_ALL}")

        # The play
        self._play_phase()
        if self.game_over:
            return

        input(f"\n{Fore.YELLOW}Press Enter to continue to 'The Show'...{
              Style.RESET_ALL}")

        # The show (counting)
        self._show_phase()
        if self.game_over:
            return

        # Switch dealer for next round
        self.dealer_idx = 1 - self.dealer_idx
        self.round_number += 1

        input(f"\n{Fore.YELLOW}Press Enter to begin the next round...{
              Style.RESET_ALL}")

        # Play another round
        self.play_round()

    def _display_hand(self, player):
        """Display a player's hand with graphical cards"""
        print(f"\n{player.avatar} {Fore.CYAN}{
              player.name}'s hand:{Style.RESET_ALL}")
        CardDisplay.display_cards(player.hand)

    def _discard_phase(self):
        """Both players discard 2 cards to the crib."""
        self.display_announcement("DISCARD PHASE")

        for i, player in enumerate(self.players):
            dealer_status = " (Dealer)" if i == self.dealer_idx else ""
            print(f"\n{player.avatar} {Fore.CYAN}{player.name}{
                  dealer_status}'s turn to discard{Style.RESET_ALL}")

            if player.is_ai:
                # AI discard with animation
                print(f"{player.avatar} {player.name} is thinking...")
                time.sleep(1.5)

                # Simple AI strategy: discard cards that contribute least to hand
                discard_indices = self._ai_select_discards(player.hand)
                discards = player.discard_to_crib(discard_indices)

                print(f"{player.avatar} {player.name} discards {
                      len(discards)} cards to the crib")
                time.sleep(0.5)
            else:
                # Human player selects cards to discard
                valid_selection = False
                while not valid_selection:
                    print(f"\n{player.avatar} {Fore.GREEN}{player.name}{
                          Style.RESET_ALL}, select 2 cards to discard to the crib:")
                    self._display_hand(player)

                    try:
                        discard_input = input(
                            f"{Fore.YELLOW}Enter two indices separated by space (e.g., '0 3'): {
                                Style.RESET_ALL}"
                        )
                        discard_indices = [int(x) for x in discard_input.split()]

                        if len(discard_indices) != 2:
                            print(f"{Fore.RED}You must discard exactly 2 cards.{
                                  Style.RESET_ALL}")
                            continue

                        discards = player.discard_to_crib(discard_indices)
                        valid_selection = True

                        print(f"\n{player.avatar} You discarded:")
                        CardDisplay.display_cards(discards, indices=False)
                        time.sleep(0.5)

                    except (ValueError, IndexError) as e:
                        print(f"{Fore.RED}Invalid selection: {
                              e}{Style.RESET_ALL}")

            self.crib.extend(discards)

        crib_owner = self.players[self.dealer_idx]
        print(f"\n{Fore.MAGENTA}Crib now has {len(self.crib)
                                              } cards (belongs to {crib_owner.name}){Style.RESET_ALL}")
        time.sleep(0.5)

    def _play_phase(self):
        """The play phase of cribbage."""
        self.clear_screen()
        self.board.display()
        self.display_announcement("THE PLAY")

        # Non-dealer leads first
        self.current_player_idx = 1 - self.dealer_idx

        # Players prepare their play cards
        for player in self.players:
            player.reset_play_cards()

        self.play_pile = []
        self.play_count = 0
        go_count = 0

        # Show starter card
        print(f"{Fore.CYAN}Starter card:{Style.RESET_ALL}")
        CardDisplay.display_cards([self.starter_card], indices=False)

        # Show human player's hand if applicable
        for player in self.players:
            if not player.is_ai:
                self._display_hand(player)

        while any(len(player.play_cards) > 0 for player in self.players):
            current_player = self.players[self.current_player_idx]

            # Display current play state
            print(f"\n{Fore.YELLOW}Current count: {
                  self.play_count}{Style.RESET_ALL}")
            if self.play_pile:
                print(f"{Fore.CYAN}Cards in play:{Style.RESET_ALL}")
                CardDisplay.display_cards(
                    self.play_pile[-min(4, len(self.play_pile)) :], indices=False
                )

            print(f"\n{current_player.avatar} {Fore.CYAN}{
                  current_player.name}'s turn{Style.RESET_ALL}")

            if len(current_player.play_cards) == 0:
                print(f"{current_player.avatar} {current_player.name} says '{
                      Fore.YELLOW}GO{Style.RESET_ALL}'")
                go_count += 1
                time.sleep(0.7)

                # If both players say GO, reset count
                if go_count == 2:
                    self.display_announcement("COUNT RESET TO 0")
                    self.play_count = 0
                    self.play_pile = []
                    go_count = 0

                    # Last player to play gets 1 point for Go
                    last_player_idx = 1 - self.current_player_idx
                    last_player = self.players[last_player_idx]
                    print(f"{last_player.avatar} {Fore.GREEN}{
                          last_player.name} gets 1 point for last card{Style.RESET_ALL}")
                    self._add_score(last_player_idx, 1, "Last Card")
                    if self.game_over:
                        return

                # Move to next player
                self.current_player_idx = 1 - self.current_player_idx
                continue

            # Reset GO count since current player can play
            go_count = 0

            # Get playable cards (those that won't exceed 31)
            playable_cards = [
                card
                for card in current_player.play_cards
                if self.play_count + card.get_value() <= 31
            ]

            if not playable_cards:
                print(f"{current_player.avatar} {current_player.name} says '{
                      Fore.YELLOW}GO{Style.RESET_ALL}'")
                go_count += 1
                time.sleep(0.7)

                # Move to next player
                self.current_player_idx = 1 - self.current_player_idx
                continue

            # Play a card
            if current_player.is_ai:
                # AI selects card with animation
                print(f"{current_player.avatar} {
                      current_player.name} is thinking...")
                time.sleep(0.8)

                # Simple AI strategy with a bit of randomness
                if random.random() < 0.8:  # 80% of the time use strategy
                    played_card = self._ai_select_play_card(
                        current_player.play_cards, playable_cards
                    )
                else:  # 20% random play for unpredictability
                    played_card = random.choice(playable_cards)

                played_index = current_player.play_cards.index(played_card)
                current_player.play_cards.pop(played_index)
            else:
                # Human selects card to play
                valid_selection = False
                while not valid_selection:
                    print(f"\n{current_player.avatar} {Fore.GREEN}Your turn{
                          Style.RESET_ALL} (count: {self.play_count})")
                    print(f"Your playable cards:")

                    # Only show playable cards
                    playable_indices = []
                    for idx, card in enumerate(current_player.play_cards):
                        if card in playable_cards:
                            playable_indices.append(idx)

                    # Display only playable cards
                    playable_display = [
                        current_player.play_cards[i] for i in playable_indices
                    ]
                    CardDisplay.display_cards(playable_display, indices=True)

                    # Match displayed indices to actual indices
                    index_map = {
                        display_idx: actual_idx
                        for display_idx, actual_idx in enumerate(playable_indices)
                    }

                    try:
                        play_input = input(f"{Fore.YELLOW}Enter index of card to play: {
                                           Style.RESET_ALL}")
                        display_idx = int(play_input)

                        if display_idx < 0 or display_idx >= len(playable_indices):
                            print(f"{Fore.RED}Invalid index.{Style.RESET_ALL}")
                            continue

                        # Map displayed index to actual index
                        played_index = index_map[display_idx]
                        played_card = current_player.play_cards[played_index]

                        # Remove the played card from play_cards
                        current_player.play_cards.pop(played_index)
                        valid_selection = True

                    except ValueError:
                        print(f"{Fore.RED}Please enter a valid number.{
                              Style.RESET_ALL}")

            # Add card to play pile and update count
            self.play_pile.append(played_card)
            self.play_count += played_card.get_value()

            print(f"\n{current_player.avatar} {
                  current_player.name} plays {played_card.colored_str()}")
            print(f"{Fore.YELLOW}Count: {self.play_count}{Style.RESET_ALL}")
            time.sleep(0.5)

            # Check for scoring in play
            points_earned = self._check_play_scoring()
            if points_earned > 0:
                self._add_score(self.current_player_idx, points_earned, "Play")
                if self.game_over:
                    return

            # If count reaches 31, reset count
            if self.play_count == 31:
                self.display_announcement(
                    f"{current_player.name} MAKES 31 FOR 2 POINTS"
                )
                self._add_score(self.current_player_idx, 2, "Thirty-One")
                if self.game_over:
                    return

                self.play_pile = []
                self.play_count = 0
                go_count = 0
                time.sleep(0.5)

            # Move to next player
            self.current_player_idx = 1 - self.current_player_idx

        # Last card point
        if self.play_count > 0 and self.play_count < 31:
            last_player_idx = 1 - self.current_player_idx
            last_player = self.players[last_player_idx]
            self.display_announcement(f"{last_player.name} GETS 1 POINT FOR LAST CARD")
            self._add_score(last_player_idx, 1, "Last Card")
            if self.game_over:
                return

    def _ai_select_play_card(self, available_cards, playable_cards):
        """AI strategy for selecting which card to play"""
        # First, try to make 15 or 31
        for card in playable_cards:
            if self.play_count + card.get_value() == 15:
                return card
            if self.play_count + card.get_value() == 31:
                return card

        # Look for pairs
        if self.play_pile:
            last_played = self.play_pile[-1]
            for card in playable_cards:
                if card.rank == last_played.rank:
                    return card

        # Look for runs
        if len(self.play_pile) >= 2:
            # Simple check for potential run continuation
            rank_values = {
                "A": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
                "J": 11,
                "Q": 12,
                "K": 13,
            }

            recent_ranks = [rank_values[card.rank] for card in self.play_pile[-2:]]
            sorted_recent = sorted(recent_ranks)

            # If the last two cards are sequential
            if sorted_recent[1] == sorted_recent[0] + 1:
                # Look for continuation
                for card in playable_cards:
                    card_value = rank_values[card.rank]
                    if (
                        card_value == sorted_recent[1] + 1
                        or card_value == sorted_recent[0] - 1
                    ):
                        return card

        # Default: play lowest value card
        return min(playable_cards, key=lambda card: card.get_value())

    def _check_play_scoring(self):
        """Check for scoring combinations during play."""
        if not self.play_pile:
            return 0

        current_player = self.players[self.current_player_idx]
        total_points = 0

        # Check for 15
        if self.play_count == 15:
            print(f"{Fore.GREEN}{current_player.name} makes 15 for 2 points{
                  Style.RESET_ALL}")
            total_points += 2
            time.sleep(0.5)

        # Check for pairs, three of a kind, four of a kind
        if len(self.play_pile) >= 2:
            # Check last cards for same rank
            matching_cards = 1
            last_rank = self.play_pile[-1].rank

            for i in range(2, min(5, len(self.play_pile) + 1)):
                if self.play_pile[-i].rank == last_rank:
                    matching_cards += 1
                else:
                    break

            if matching_cards == 2:
                print(f"{Fore.GREEN}{current_player.name} makes a pair for 2 points{
                      Style.RESET_ALL}")
                total_points += 2
            elif matching_cards == 3:
                print(f"{Fore.GREEN}{current_player.name} makes three of a kind for 6 points{
                      Style.RESET_ALL}")
                total_points += 6
            elif matching_cards == 4:
                print(f"{Fore.GREEN}{current_player.name} makes four of a kind for 12 points{
                      Style.RESET_ALL}")
                total_points += 12

            if matching_cards > 1:
                time.sleep(0.5)

        # Check for runs (sequences of 3 or more)
        if len(self.play_pile) >= 3:
            for run_length in range(min(7, len(self.play_pile)), 2, -1):
                # Get the last run_length cards
                run_check = self.play_pile[-run_length:]

                # Convert ranks to numerical values for checking runs
                rank_values = {
                    "A": 1,
                    "2": 2,
                    "3": 3,
                    "4": 4,
                    "5": 5,
                    "6": 6,
                    "7": 7,
                    "8": 8,
                    "9": 9,
                    "10": 10,
                    "J": 11,
                    "Q": 12,
                    "K": 13,
                }

                # Get numerical values of all cards
                num_values = [rank_values[card.rank] for card in run_check]

                # Check if sorted values form consecutive sequence
                sorted_values = sorted(num_values)
                is_run = True
                for i in range(1, len(sorted_values)):
                    if sorted_values[i] != sorted_values[i - 1] + 1:
                        is_run = False
                        break

                if is_run:
                    points = run_length
                    print(f"{Fore.GREEN}{current_player.name} makes a run of {
                          run_length} for {points} points{Style.RESET_ALL}")
                    total_points += points
                    time.sleep(0.5)
                    break  # Only count the longest run

        return total_points

    def _ai_select_discards(self, hand):
        """AI strategy for selecting which cards to discard to the crib."""
        # Calculate potential value of each card in the hand
        card_values = {}
        for i, card in enumerate(hand):
            # Create test hand without this card
            test_hand = hand.copy()
            test_hand.pop(i)

            # For each possible second discard
            remaining_indices = [j for j in range(len(hand)) if j != i]
            total_value = 0

            for j in remaining_indices:
                test_hand2 = test_hand.copy()
                test_hand2.pop(remaining_indices.index(j))
                # Score the remaining 4 cards
                hand_value = self._calculate_hand_value(test_hand2, None)
                total_value += hand_value

            # Average value when this card is discarded
            card_values[i] = total_value / len(remaining_indices)

        # Find the two cards that leave the highest valued hand
        sorted_indices = sorted(
            card_values.keys(), key=lambda idx: card_values[idx], reverse=True
        )
        return sorted_indices[:2]

    def _show_phase(self):
        """The show (counting) phase of cribbage."""
        self.clear_screen()
        self.board.display()
        self.display_announcement("THE SHOW")

        # Non-dealer scores first, then dealer, then crib
        scoring_player_idx = 1 - self.dealer_idx

        # Display starter card
        print(f"{Fore.CYAN}Starter card:{Style.RESET_ALL}")
        CardDisplay.display_cards([self.starter_card], indices=False)
        time.sleep(0.5)

        # Score each player's hand
        for i in range(2):
            player = self.players[scoring_player_idx]
            dealer_status = " (Dealer)" if scoring_player_idx == self.dealer_idx else ""

            print(f"\n{player.avatar} {Fore.CYAN}{player.name}{
                  dealer_status}'s hand:{Style.RESET_ALL}")
            CardDisplay.display_cards(player.hand, indices=False)
            time.sleep(0.5)

            # Calculate and show score
            points = self._calculate_hand_value(player.hand, self.starter_card)
            scoring_details = self._get_hand_scoring_details(
                player.hand, self.starter_card
            )

            # Display scoring details
            for category, value in scoring_details.items():
                if value > 0:
                    print(
                        f"{Fore.GREEN}+ {value} points for {category}{Style.RESET_ALL}"
                    )
                    time.sleep(0.3)

            print(f"{Fore.YELLOW}{player.name} scores {
                  points} points{Style.RESET_ALL}")
            self._add_score(scoring_player_idx, points, "Hand")
            if self.game_over:
                return

            # Switch to other player
            scoring_player_idx = 1 - scoring_player_idx
            time.sleep(0.5)

        # Score the crib (dealer's crib)
        dealer = self.players[self.dealer_idx]
        print(f"\n{Fore.MAGENTA}{dealer.name}'s crib:{Style.RESET_ALL}")
        CardDisplay.display_cards(self.crib, indices=False)
        time.sleep(0.5)

        crib_points = self._calculate_hand_value(
            self.crib, self.starter_card, is_crib=True
        )
        scoring_details = self._get_hand_scoring_details(
            self.crib, self.starter_card, is_crib=True
        )

        # Display crib scoring details
        for category, value in scoring_details.items():
            if value > 0:
                print(f"{Fore.GREEN}+ {value} points for {category}{Style.RESET_ALL}")
                time.sleep(0.3)

        print(f"{Fore.YELLOW}{dealer.name} scores {
              crib_points} points from the crib{Style.RESET_ALL}")
        self._add_score(self.dealer_idx, crib_points, "Crib")
        if self.game_over:
            return

    def _calculate_hand_value(self, cards, starter, is_crib=False):
        """Calculate the value of a hand or crib."""
        if not cards:
            return 0

        all_cards = cards.copy()
        if starter:
            all_cards.append(starter)

        score = 0

        # Fifteens: any combination of cards totaling 15 = 2 points
        score += self._count_fifteens(all_cards)

        # Pairs: 2 points per pair
        score += self._count_pairs(all_cards)

        # Runs: 1 point per card in run
        score += self._count_runs(all_cards)

        # Flushes:
        # - Hand: 4 points if all 4 hand cards match suit, 5 if starter matches too
        # - Crib: 5 points but only if all 5 cards (including starter) match suit
        score += self._count_flush(cards, starter, is_crib)

        # His Nobs: Jack of same suit as starter = 1 point
        if starter:
            score += self._count_nobs(cards, starter)

        return score

    def _count_fifteens(self, cards):
        """Count combinations adding to 15."""
        total_points = 0
        values = [min(10, card.get_value()) for card in cards]

        # Check all combinations of cards for fifteens
        for r in range(2, len(cards) + 1):
            for combo in combinations(values, r):
                if sum(combo) == 15:
                    total_points += 2

        return total_points

    def _count_pairs(self, cards):
        """Count pairs in the hand."""
        pairs = 0
        # Group cards by rank
        rank_groups = Counter([card.rank for card in cards])

        # For each rank, calculate pairs
        for rank, count in rank_groups.items():
            if count >= 2:
                # Formula: n(n-1)/2 gives number of pairs
                pairs += (count * (count - 1)) // 2

        return pairs * 2  # 2 points per pair

    def _count_runs(self, cards):
        """Count runs (sequences) in the hand."""
        if not cards:
            return 0

        # Convert ranks to numerical values
        rank_values = {
            "A": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
        }

        # Count occurrences of each rank
        rank_counts = Counter([card.rank for card in cards])
        unique_ranks = sorted([rank_values[rank] for rank in rank_counts.keys()])

        # Find the longest run
        longest_run = 0
        current_run = 1

        for i in range(1, len(unique_ranks)):
            if unique_ranks[i] == unique_ranks[i - 1] + 1:
                current_run += 1
            else:
                longest_run = max(longest_run, current_run)
                current_run = 1

        longest_run = max(longest_run, current_run)

        # Only count if run length is at least 3
        if longest_run < 3:
            return 0

        # Calculate points: run length × number of combinations
        total_points = longest_run

        # Multiply by combinations if there are duplicate ranks in the run
        in_run_ranks = unique_ranks[:longest_run]
        combinations = 1
        for rank_val in in_run_ranks:
            rank = next(key for key, val in rank_values.items() if val == rank_val)
            if rank_counts[rank] > 1:
                combinations *= rank_counts[rank]

        return total_points * combinations

    def _count_flush(self, cards, starter, is_crib=False):
        """Count flush points."""
        if not cards:
            return 0

        # Check if all hand cards are the same suit
        suits = [card.suit for card in cards]
        if len(set(suits)) == 1:
            if starter and starter.suit == suits[0]:
                # All 5 cards same suit = 5 points
                return 5
            elif not is_crib:
                # In hand (not crib), 4 same suit = 4 points
                return 4

        return 0

    def _count_nobs(self, cards, starter):
        """Count 'His Nobs' - Jack of the same suit as starter card."""
        starter_suit = starter.suit
        for card in cards:
            if card.rank == "J" and card.suit == starter_suit:
                return 1
        return 0

    def _get_hand_scoring_details(self, cards, starter, is_crib=False):
        """Get detailed breakdown of scoring for a hand."""
        if not cards:
            return {}

        all_cards = cards.copy()
        if starter:
            all_cards.append(starter)

        details = {"Fifteens": 0, "Pairs": 0, "Runs": 0, "Flush": 0, "His Nobs": 0}

        # Fifteens
        details["Fifteens"] = self._count_fifteens(all_cards)

        # Pairs
        details["Pairs"] = self._count_pairs(all_cards)

        # Runs
        details["Runs"] = self._count_runs(all_cards)

        # Flushes
        details["Flush"] = self._count_flush(cards, starter, is_crib)

        # His Nobs
        if starter:
            details["His Nobs"] = self._count_nobs(cards, starter)

        return details

    def _add_score(self, player_idx, points, score_type):
        """Add points to a player's score and check for game end."""
        player = self.players[player_idx]
        player.score += points

        # Update board display to show new score
        self.clear_screen()
        self.board.display()

        # Announce scoring
        self.slow_print(f"{Fore.GREEN}{player.name} scores {
                        points} points from {score_type}{Style.RESET_ALL}")
        time.sleep(0.5)

        # Check for game over
        if player.score >= self.target_score:
            self.game_over = True
            self.winner = player
            self.display_announcement(f"GAME OVER! {player.name} WINS!")
            print(f"\n{Fore.GREEN}Final Score:{Style.RESET_ALL}")
            print(f"{self.players[0].avatar} {Fore.CYAN}{self.players[0].name}: {
                  self.players[0].score}{Style.RESET_ALL}")
            print(f"{self.players[1].avatar} {Fore.CYAN}{self.players[1].name}: {
                  self.players[1].score}{Style.RESET_ALL}")

            return True

        return False


def main():
    """Main function to start the game."""
    # Get player name
    print(f"{Fore.CYAN}Welcome to Cribbage!{Style.RESET_ALL}")
    player_name = input(f"{Fore.YELLOW}Enter your name: {Style.RESET_ALL}")
    if not player_name.strip():
        player_name = "Player 1"

    # Ask if player wants to play against AI
    ai_opponent = (
        input(f"{Fore.YELLOW}Play against AI? (y/n): {Style.RESET_ALL}")
        .lower()
        .startswith("y")
    )

    if ai_opponent:
        opponent_name = "Computer"
    else:
        opponent_name = input(f"{Fore.YELLOW}Enter opponent's name: {Style.RESET_ALL}")
        if not opponent_name.strip():
            opponent_name = "Player 2"

    # Ask for target score
    try:
        target_input = input(
            f"{Fore.YELLOW}Target score (61 or 121) [default: 121]: {
                Style.RESET_ALL}"
        )
        target_score = int(target_input) if target_input.strip() else 121
        if target_score not in [61, 121]:
            print(f"{Fore.RED}Invalid target score. Using 121.{Style.RESET_ALL}")
            target_score = 121
    except ValueError:
        print(f"{Fore.RED}Invalid input. Using default target score of 121.{
              Style.RESET_ALL}")
        target_score = 121

    # Create and start the game
    game = CribbageGame(
        player1_name=player_name,
        player2_name=opponent_name,
        target_score=target_score,
        player2_is_ai=ai_opponent,
    )
    game.start_game()


if __name__ == "__main__":
    main()
