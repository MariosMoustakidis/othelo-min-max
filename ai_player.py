import math

class AIPlayer:
    def __init__(self, depth=3):
        self.depth = depth

    def get_move(self, game):
        _, move = game.minimax(self.depth, True, -math.inf, math.inf)
        return move
