from copy import deepcopy
import numpy as np
from functools import lru_cache


class Board:
    """盤面を保持するクラス"""

    WHITE = 1
    BLACK = 2

    def __init__(self) -> None:
        """コンストラクタ"""
        self.board = np.zeros((8,8),dtype=np.int32)              #盤面の作成
        self.board[[3,4],[3,4]] = Board.WHITE     #白い駒の配置
        self.board[[4,3],[3,4]] = Board.BLACK     #黒い駒の配置
        self.numbers = {Board.WHITE : 2, Board.BLACK : 2}  # 駒数の初期化
    
    @classmethod
    def is_color(cls, color) -> None:
        """渡された値がWHITEかBLACKのいずれかであるかを判定"""

        if not type(color) is int:
            raise TypeError("Color should be int object")
        

        if not (color == Board.WHITE or color == Board.BLACK):
            raise ValueError(f"{color} is not color. color should be {Board.WHITE} or {Board.BLACK}")
        
    

    @classmethod
    def is_place(cls, place) -> None:
        """placeが盤面上の座標であるか判定"""

        if not type(place) is tuple:
            raise TypeError("Place should be tuple object")
        
        if not(len(place) == 2 and type(place[0]) is int and type(place[1]) is int):
            raise ValueError("Place should be a tuple with two int types side by side")
        
        if not(0 <= place[0] <= 7 and 0 <= place[1] <= 7):
            raise IndexError("Place out of range.")
    
    @classmethod
    def is_board(cls, bd) -> None:
        """bdがboardのインスタンスであるかを判定"""
        if not isinstance(bd, Board):
            raise TypeError(f"{bd} is not instace of board")
        
        if not(np.sum(bd.board==Board.BLACK) == bd.numbers[Board.BLACK] and \
            np.sum(bd.board==Board.WHITE) == bd.numbers[Board.WHITE]):
            raise ValueError(f"Number of pieces does not match the board")
    

    @classmethod
    def turn_color(cls, color) -> int:
        """渡された色と反対の色を渡す"""
        return Board.WHITE if color == Board.BLACK else Board.BLACK
    
    
    @lru_cache()
    def get_change_places_for_self(self, place, color) -> list:
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

        Board.is_color(color)
        Board.is_place(place)

        if self.board[place] != 0:  # 既に置かれていたら[]を返す
            return []

        change_plases = []    # ひっくり返る座標のリスト

        for direction in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            change_plases_ = []   # directionの方向でひっくり返る駒
            search_place = place
            while True:
                search_place = (search_place[0] + direction[0], search_place[1] + direction[1])  # 探索場所の更新
            
                if not(0 <= search_place[0] <= 7 and 0 <= search_place[1] <= 7) or self.board[search_place] == 0:  # 行き止まりなら[]を返す
                    change_plases_ = []
                    break

                if self.board[search_place] == color:     # colorに出逢ったら終了
                    break

                if self.board[search_place] != color:     # colorの反対の色ならその座標を保存して探索を続ける
                    change_plases_.append(search_place)
            
            change_plases += change_plases_       # 得られた座標をまとめてchange_plasesに保存

        return change_plases
    

    @classmethod
    @lru_cache
    def get_change_places_for_input(cls, bd, place, color) -> list:
        """get_chage_places_for_selfのclassmethodでの実装"""

        Board.is_board(bd)
        Board.is_color(color)
        Board.is_place(place)

        if bd.board[place] != 0:  # 既に置かれていたら[]を返す
            return []

        change_plases = []    # ひっくり返る座標のリスト

        for direction in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            change_plases_ = []   # directionの方向でひっくり返る駒
            search_place = place
            while True:
                search_place = (search_place[0] + direction[0], search_place[1] + direction[1])  # 探索場所の更新
            
                if not(0 <= search_place[0] <= 7 and 0 <= search_place[1] <= 7) or bd.board[search_place] == 0:  # 行き止まりなら[]を返す
                    change_plases_ = []
                    break

                if bd.board[search_place] == color:     # colorに出逢ったら終了
                    break

                if bd.board[search_place] != color:     # colorの反対の色ならその座標を保存して探索を続ける
                    change_plases_.append(search_place)
            
            change_plases += change_plases_       # 得られた座標をまとめてchange_plasesに保存

        return change_plases


    def put_for_self(self, place, color) -> None:
        """コマを置く

        Parameters
        ----------
        place : tuple
            置く座標
        color : int
            置く色

        """

        Board.is_color(color)
        Board.is_place(place)

        change_places = self.get_change_places_for_self(place, color)

        if change_places == []:         # ひっくり返る場所がなければ置けない(例外を出力)
            raise ValueError("You cannot place a piece there.")
        
        for change_place in change_places:
            self.board[change_place] = color  # 色の変更

        self.board[place] = color     # 駒を置く

        self.numbers[color] += 1
        self.numbers[Board.turn_color(color)] -= len(change_places)  # 駒数の更新


    @classmethod
    def put_for_input(cls, bd, place, color) -> 'Board':
        """コマを置く

        Parameters
        ----------
        bd : board
            置く場所
        place : tuple
            置く座標
        color : int
            置く色

        Returns
        -------
        board
            おいた後の盤面
        """

        Board.is_board(bd)
        Board.is_color(color)
        Board.is_place(place)

        bd = deepcopy(bd)
        change_places = bd.get_change_places_for_self(place, color)

        if change_places == []:         # ひっくり返る場所がなければ置けない(例外を出力)
            raise ValueError("You cannot place a piece there.")
        
        for change_place in change_places:
            bd.board[change_place] = color  # 色の変更

        bd.board[place] = color     # 駒を置く

        bd.numbers[color] += 1
        bd.numbers[Board.turn_color(color)] -= len(change_places)  # 駒数の更新

        return bd
    
    
    def get_places_to_put_for_self(self, color) -> list:
        """置ける場所の取得

        Parameters
        ----------
        color : int
            置く色

        Returns
        -------
        list
            おける場所のリスト
        """

        Board.is_color(color)

        places_to_put = []
    
        for i in range(8):
            for j in range(8):
                if not self.get_change_places_for_self((i, j), color) == []:
                    places_to_put.append((i, j))
        
        return places_to_put
    

    @classmethod
    def get_places_to_put_for_input(cls, bd, color) -> list:
        """置ける場所の取得

        Parameters
        ----------
        bd : board
            置く盤面
        color : int
            置く色

        Returns
        -------
        list
            おける場所のリスト
        """

        Board.is_board(bd)
        Board.is_color(color)

        places_to_put = []
    
        for i in range(8):
            for j in range(8):
                if not bd.get_change_places_for_self((i, j), color) == []:
                    places_to_put.append((i, j))
        
        return places_to_put


    def is_end_for_self(self, color) -> int:
        """ゲームが終了したかの判定

        Parameters
        ----------
        color : int
            次に置く色

        Returns
        -------
        int
            終了時勝った方の色か引き分けなら0を返す。終了してなければNone
        """

        Board.is_color(color)

        actions = self.get_places_to_put_for_self(color)

        for action in actions:
            bd_new = Board.put(self,color)
            if not Board.get_places_to_put_for_self(bd_new, Board.turn_color(color)) == []:
                break
        else:
            if self.numbers[Board.WHITE] > self.numbers[Board.BLACK]:
                return Board.WHITE
            elif self.numbers[Board.BLACK] > self.numbers[Board.WHITE]:
                return Board.BLACK
            else:
                return 0
        
        return None

    
    @classmethod
    def is_end_for_input(cls, bd, color) -> int:
        """ゲームが終了したかの判定

        Parameters
        ----------
        bd : board
            終了判定を行う盤面
        color : int
            次に置く色

        Returns
        -------
        int
            終了時勝った方の色か引き分けなら0を返す。終了してなければNone
        """

        Board.is_board(bd)
        Board.is_color(color)

        actions = bd.get_places_to_put_for_self(color)

        for action in actions:
            bd_new = Board.put(bd,color)
            if not Board.get_places_to_put_for_self(bd_new, Board.turn_color(color)) == []:
                break
        else:
            if bd.numbers[Board.WHITE] > bd.numbers[Board.BLACK]:
                return Board.WHITE
            elif bd.numbers[Board.BLACK] > bd.numbers[Board.WHITE]:
                return Board.BLACK
            else:
                return 0
        
        return None


    def __str__(self) -> str:
        s = ""
        for i in self.board:
            s += " ".join(map(str, i)) + "\n"
        
        s += f"Black | Point:{self.numbers[Board.BLACK]}     Place to put:{self.get_places_to_put_for_self(Board.BLACK)}\n"
        s += f"White | Point:{self.numbers[Board.WHITE]}     Place to put:{self.get_places_to_put_for_self(Board.WHITE)}"

        return s
    




if __name__ == "__main__":
    bd = Board()
    color = Board.BLACK

    # print(board.get_change_places(bd, (5, 4), 2))
    while True:
        print(bd)
        bd.put_for_self(tuple(map(int, input("put:").split())), color)
        color = Board.turn_color(color)