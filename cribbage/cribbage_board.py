END_OF_TRACK = 121


class CribbageBoard:
    def __init__(self):
        self.peg_1_location = 0
        self.peg_2_location = 0

    def _reset(self):
        self.peg_1_location = 0
        self.peg_2_location = 0

    def _get_player(player: int):
        return {1: self.peg_1_location, 2: self.peg_2_location}[player]

    def move_peg(player: int, holes: int) -> bool:
        peg_location = self._get_player(player)
        peg_location += holes
        if peg_location >= 121:
            return True
        return False
