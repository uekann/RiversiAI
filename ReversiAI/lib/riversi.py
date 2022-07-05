import numpy as np


class board():
    """盤面を保持するクラス"""

    WHITE = 1
    BLACK = 2

    def __init__(self) -> None:
        """コンストラクタ"""
        self.board = np.zeros((8,8))              #盤面の作成
        self.board[[3,4],[3,4]] = board.WHITE     #白い駒の配置
        self.board[[4,3],[3,4]] = board.BLACK     #黒い駒の配置
        self.number_W = 2                         #白い駒の数
        self.number_B = 2                         #黒い駒の数

        return None
    

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
    

    @classmethod
    def _turn_color(cls, color) -> int:
        """渡された色と反対の色を渡す"""
        return board.WHITE if color == board.BLACK else board.BLACK
    


    def get_change_plases(self, place, color) -> list:
        """placeにコマを置いたときひっくり返る座標のlistを返す

        Parameters
        ----------
        place : tuple
            駒を置きたい場所
        color : int
            置きたい駒の色(board.WHITE or board.BLACK)

        Returns
        -------
        list
            ひっくり返る座標のlist
        """

        board._is_color(color)
        board._is_place(place)

        if self.board[place] != 0:
            return []

        change_plases = []
        for direction in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            change_plases_ = []
            search_place = place
            while True:
                search_place = (search_place[0] + direction[0], search_place[1] + direction[1])
            
                if not(0 <= search_place[0] <= 7 and 0 <= search_place[1] <= 7) or self.board[search_place] == 0:
                    change_plases_ = []
                    break

                if self.board[search_place] == color:
                    break

                if self.board[search_place] != color:
                    change_plases_.append(search_place)
            
            change_plases += change_plases_


        return change_plases
    
    def put(self, place, color) -> bool:
        """コマを置く

        Parameters
        ----------
        place : tuple_
            置く座標
        color : int
            置く色

        Returns
        -------
        bool
            実行結果
        """

        board._is_color(color)
        board._is_place(place)

        change_places = self.get_change_plases(place, color)

        if change_places == []:
            raise ValueError("You cannot place a piece there.")
            return False
        
        for change_place in change_places:
            self.board[change_place] = color
            
        self.board[place] = color
        return True

if __name__ == "__main__":
    bd = board()
    color = board.WHITE

    while True:
        print(bd.board)
        point = tuple(map(int, input().split()))
        bd.put(point,color)
        color = board._turn_color(color)