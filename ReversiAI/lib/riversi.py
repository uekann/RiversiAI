import numpy as np

class board():
    """盤面を保持するクラス"""

    WHITE = 1
    BLACK = 2

    def __init__(self) -> None:
        self.board = np.zeros((8,8))
        self.board[[4,5],[4,5]] = board.WHITE
        self.board[[5,4],[4,5]] = board.BLACK