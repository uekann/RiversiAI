import numpy as np


class board():
    """盤面を保持するクラス"""

    WHITE = 1
    BLACK = 2

    def __init__(self) -> None:
        """コンストラクタ"""
        self.board = np.zeros((8,8),dtype=np.int32)              #盤面の作成
        self.board[[3,4],[3,4]] = board.WHITE     #白い駒の配置
        self.board[[4,3],[3,4]] = board.BLACK     #黒い駒の配置
        self.numbers = {board.WHITE : 2, board.BLACK : 2}  # 駒数の初期化
    
    @classmethod
    def _is_color(cls, color) -> None:
        """渡された値がWHITEかBLACKのいずれかであるかを判定"""

        if not type(color) is int:
            raise TypeError("Color should be int object")
        

        if not (color == board.WHITE or color == board.BLACK):
            raise ValueError(f"{color} is not color. color should be {board.WHITE} or {board.BLACK}")
        
    

    @classmethod
    def _is_place(cls, place) -> None:
        """placeが盤面上の座標であるか判定"""

        if not type(place) is tuple:
            raise TypeError("Place should be tuple object")
        
        if not(len(place) == 2 and type(place[0]) is int and type(place[1]) is int):
            raise ValueError("Place should be a tuple with two int types side by side")
        
        if not(0 <= place[0] <= 7 and 0 <= place[1] <= 7):
            raise IndexError("Place out of range.")
    

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
    

    def put(self, place, color) -> None:
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

        if change_places == []:         # ひっくり返る場所がなければ置けない(例外を出力)
            raise ValueError("You cannot place a piece there.")
        
        for change_place in change_places:
            self.board[change_place] = color  # 色の変更

        self.board[place] = color     # 駒を置く

        self.numbers[color] += 1
        self.numbers[board._turn_color(color)] -= len(change_places)  # 駒数の更新
    
    
    def get_places_to_put(self, color) -> list:
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

        board._is_color(color)

        places_to_put = []
    
        for i in range(8):
            for j in range(8):
                if not self.get_change_plases((i, j), color) == []:
                    places_to_put.append((i, j))
        
        return places_to_put

    def __str__(self) -> str:
        s = ""
        for i in self.board:
            s += " ".join(map(str, i)) + "\n"
        
        s += f"Black | Point:{self.numbers[board.BLACK]}     Place to put:{self.get_places_to_put(board.BLACK)}\n"
        s += f"White | Point:{self.numbers[board.WHITE]}     Place to put:{self.get_places_to_put(board.WHITE)}"

        return s



if __name__ == "__main__":
    bd = board()
    color = board.BLACK
    while True:
        print(bd)
        bd.put(tuple(map(int, input("put:").split())), color)
        color = board._turn_color(color)