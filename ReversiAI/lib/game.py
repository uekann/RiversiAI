from .riversi import board

class game():
    """ゲームそのものを管理するクラス"""

    def __init__(self) -> None:
        self.board = board()
    
    