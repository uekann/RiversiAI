import sys
import numpy as np


class board():
    """盤面を保持するクラス"""

    WHITE = 1
    BLACK = 2

    def __init__(self) -> None:
        """コンストラクタ"""
        self.board = np.zeros((8,8))              #盤面の作成
        self.board[[4,5],[4,5]] = board.WHITE     #白い駒の配置
        self.board[[5,4],[4,5]] = board.BLACK     #黒い駒の配置
        self.number_W = 2                         #白い駒の数
        self.number_B = 2                         #黒い駒の数
    
    @classmethod
    def _is_color(cls, color) -> bool:
        """渡された値がWHITEかBLACKのいずれかであるかを判定"""

        if not type(color) is int:
            raise TypeError("Color should be int object")
        

        if not (color == board.WHITE or color == board.BLACK):
            raise ValueError(f"{color} is not color. color should be {board.WHITE} or {board.BLACK}")
        

        return True
    
    @classmethod
    def _is_place(cls, place) -> bool:
        """placeが盤面上の座標であるか判定"""

        if not type(place) is tuple:
            raise TypeError("Place should be tuple object")
        
        if not(len(place) == 2 and type(place[0]) is int and type(place[1]) is int):
            raise ValueError("Place should be a tuple with two int types side by side")
        
        if not(0 <= place[0] <= 7 and 0 <= place[1] <= 7):
            raise IndexError("Place out of range.")
        
        return True


    def can_put(self, place, color) -> bool:
        """駒を置けるかを判定

        Parameters
        ----------
        place : tuple
            駒を置きたい場所
        color : int
            置きたい駒の色(board.WHITE or board.BLACK)

        Returns
        -------
        bool
            設置可能かどうか
        """

        board._is_color(color)
        board._is_place(place)
        return True