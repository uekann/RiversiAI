from copy import deepcopy
import numpy as np
from functools import lru_cache
from tree import Tree


class Board:

    WHITE = 2
    BLACK = 1
    EMPTY = 0

    def __init__(self, bd : 'Board'=None, bd_array : np.ndarray = None, color_switch : bool = False) -> None:
        """盤面を保持するクラス

        Parameters
        ----------
        bd : Board, optional
            Board型のコピーをする場合コピー元のインスタンスを入れる
            copyやdeepcopyに加え、存在しうる盤面かどうかも判定してくれる。
            デフォルトはNone

        bd_array : np.ndarray, optional
            盤面の配列(ndarray)からBoard型のインスタンスを生成したいときに使う。
            bdがNoneでない場合は無視される。デフォルトはNone

        color_switch : bool, optional
            BlackとWhiteの入れ替えを行うかどうかを表す。
            デフォルトはNone
        """

        if color_switch:   # 色の入れ替え
            self.color1 = Board.WHITE
            self.color2 = Board.BLACK
        else:
            self.color1 = Board.BLACK
            self.color2 = Board.WHITE



        if bd_array is None and bd == None:   # 生成時
            self.board = np.zeros((8,8),dtype=np.int32)              #盤面の作成
            self.board[[3,4],[3,4]] = self.color1     #白い駒の配置
            self.board[[4,3],[3,4]] = self.color2     #黒い駒の配置
            self.numbers = {self.color1 : 2, self.color2 : 2}  # 駒数の初期化

        elif not bd == None:   # Board型のコピーをする時
            Board.is_board(bd)
            self = deepcopy(bd)

        else:   # ndarrayから生成する時
            if type(bd_array) == np.ndarray and \
                bd_array.shape == (8, 8) and \
                bd_array.dtype == np.int32 and \
                ((bd_array==Board.EMPTY) + (bd_array==Board.BLACK) + (bd_array==Board.WHITE)).all():   # ndarrayが盤面として適切か判定

                self.board = deepcopy(bd_array)
                self.numbers = {Board.WHITE : np.sum(bd_array==Board.WHITE), Board.BLACK : np.sum(bd_array==Board.BLACK)} 

            else:
                raise ValueError(f"{bd_array} could not be the board")
        
    
    @classmethod
    def is_color(cls, color : int) -> None:
        """渡された値がWHITEかBLACKのいずれかであるかを判定"""

        if not type(color) is int:
            raise TypeError("Color should be int object")
        

        if not (color == Board.WHITE or color == Board.BLACK):
            raise ValueError(f"{color} is not color. color should be {Board.WHITE} or {Board.BLACK}")
        
    

    @classmethod
    def is_place(cls, place : tuple) -> None:
        """placeが盤面上の座標であるか判定"""

        if not type(place) is tuple:
            raise TypeError("Place should be tuple object")
        
        if not(len(place) == 2 and type(place[0]) is int and type(place[1]) is int):
            raise ValueError("Place should be a tuple with two int types side by side")
        
        if not(0 <= place[0] <= 7 and 0 <= place[1] <= 7):
            raise IndexError("Place out of range.")
    

    @classmethod
    def is_board(cls, bd : 'Board') -> None:
        """bdがboardのインスタンスであるかを判定"""
        if not isinstance(bd, Board):
            raise TypeError(f"{bd} is not instace of board")
        
        if not(type(bd.board) == np.ndarray and \
            bd.board.shape == (8, 8) and \
            bd.board.dtype == np.int32 and \
            ((bd.board==Board.EMPTY) + (bd.board==Board.BLACK) + (bd.board==Board.WHITE)).all()):
            raise ValueError(f"{bd.board} is not match the format of board")

        if not(np.sum(bd.board==Board.BLACK) == bd.numbers[Board.BLACK] and \
            np.sum(bd.board==Board.WHITE) == bd.numbers[Board.WHITE]):
            raise ValueError(f"Number of pieces does not match the board")
    

    @classmethod
    def turn_color(cls, color : int) -> int:
        """渡された色と反対の色を渡す"""
        Board.is_color(color)
        return Board.WHITE if color == Board.BLACK else Board.BLACK
    

    @classmethod
    def get_change_places(cls, bd : 'Board', place : tuple, color : int) -> list:
        """placeに駒を置いたときにひっくり返る駒の座標を取得

        Parameters
        ----------
        bd : Board
            置く対象の盤面
        place : tuple
            駒を置く場所。[0,8)のint二つを要素とする必要がある
        color : int
            置く駒の色。Board.WHITEかBoard.BLACKである必要がある

        Returns
        -------
        list
            ひっくり返る駒のlist。ない場合は[]を返す
        """

        Board.is_board(bd)
        Board.is_color(color)
        Board.is_place(place)

        if bd.board[place] != Board.EMPTY:  # 既に置かれていたら[]を返す
            return []

        change_plases = []    # ひっくり返る座標のリスト

        for direction in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            change_plases_ = []   # directionの方向でひっくり返る駒
            search_place = place
            while True:
                search_place = (search_place[0] + direction[0], search_place[1] + direction[1])  # 探索場所の更新
            
                if not(0 <= search_place[0] <= 7 and 0 <= search_place[1] <= 7) or bd.board[search_place] == Board.EMPTY:  # 行き止まりなら[]を返す
                    change_plases_ = []
                    break

                if bd.board[search_place] == color:     # colorに出逢ったら終了
                    break

                if bd.board[search_place] != color:     # colorの反対の色ならその座標を保存して探索を続ける
                    change_plases_.append(search_place)
            
            change_plases += change_plases_       # 得られた座標をまとめてchange_plasesに保存

        return change_plases


    def put(self, place : tuple, color : int) -> 'Board':
        """selfに駒を置く

        Parameters
        ----------
        place : tuple
            駒を置く場所。[0,8)のint二つを要素とする必要がある
        color : int
            置く駒の色。color1色なら1、color2色なら2を渡す必要がある

        Returns
        -------
        Board
            置いた後の盤面(self)を返す

        """

        if color == 1:   # color1を指定された場合
            color = self.color1
        elif color == 2:   # color2を指定され場合
            color = self.color2
        else:   # どちらでもない場合(例外を出力)
            if not type(color) == int:
                raise TypeError("Color must be int object")
            else:
                raise ValueError("Color must be 1 or 2")
    
        Board.is_place(place)

        change_places = Board.get_change_places(self, place, color)   # ひっくり返る場所のlist

        if change_places == []:         # ひっくり返る場所がなければ置けない(例外を出力)
            raise ValueError("You cannot place a piece there.")
        
        for change_place in change_places:
            self.board[change_place] = color  # 駒をひっくり返す

        self.board[place] = color     # 駒を置く

        self.numbers[color] += 1
        self.numbers[color] += len(change_places)
        self.numbers[Board.turn_color(color)] -= len(change_places)  # 駒数の更新

        return self
    

    @classmethod
    def get_board_after_put(cls, bd : 'Board', place : tuple, color : int) -> 'Board':
        """bdに駒を置く。Board.putのclassmethodでの実装

        Parameters
        ----------
        bd : Board
            置く対象となる盤面
        place : tuple
            駒を置く場所。[0,8)のint二つを要素とする必要がある
        color : int
            置く駒の色。color1色なら1、color2色なら2を渡す必要がある

        Returns
        -------
        Board
            置いた後の盤面を返す

        """

        Board.is_board(bd)
        Board.is_color(color)
        Board.is_place(place)

        bd = deepcopy(bd)
        change_places = Board.get_change_places(bd, place, color)

        if change_places == []:         # ひっくり返る場所がなければ置けない(例外を出力)
            raise ValueError("You cannot place a piece there.")
        
        for change_place in change_places:
            bd.board[change_place] = color  # 色の変更

        bd.board[place] = color     # 駒を置く

        bd.numbers[color] += 1
        bd.numbers[color] += len(change_places)
        bd.numbers[Board.turn_color(color)] -= len(change_places)  # 駒数の更新

        return bd
    

    @classmethod
    def get_places_to_put(cls, bd : 'Board', color : int) -> list:
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
                # (i, j)においたとき一つでもひっくり返るならplaces_to_putに(i, j)を追加

                if not(bd.board[(i, j)] == Board.EMPTY):
                    continue

                for direction in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
                    change_plases = []   # directionの方向でひっくり返る駒
                    search_place = (i, j)
                    while True:
                        search_place = (search_place[0] + direction[0], search_place[1] + direction[1])  # 探索場所の更新
            
                        if not(0 <= search_place[0] <= 7 and 0 <= search_place[1] <= 7) or bd.board[search_place] == Board.EMPTY:  # 行き止まりなら[]を返す
                            change_plases = []
                            break

                        if bd.board[search_place] == color:     # colorに出逢ったら終了
                            break

                        if bd.board[search_place] != color:     # colorの反対の色ならその座標を保存して探索を続ける
                            change_plases.append(search_place)
                    
                    if not(change_plases == []):
                        places_to_put.append((i, j))
                        break
        
        return places_to_put

    
    @classmethod
    def is_end(cls, bd : 'Board', color : int) -> int:
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
            終了時勝った方の色か引き分けならBoard.EMPTYを返す。終了してなければNone
        """

        Board.is_board(bd)
        Board.is_color(color)

        actions = Board.get_places_to_put(bd, color)

        for action in actions:
            bd_new = Board.get_board_after_put(bd,action,color)
            if not Board.get_places_to_put(bd_new, Board.turn_color(color)) == []:
                break
        else:
            if bd.numbers[Board.WHITE] > bd.numbers[Board.BLACK]:
                return Board.WHITE
            elif bd.numbers[Board.BLACK] > bd.numbers[Board.WHITE]:
                return Board.BLACK
            else:
                return Board.EMPTY
        
        return None


    def __str__(self) -> str:
        s = ""
        for i in self.board:
            s += " ".join(map(str, i)) + "\n"

        return s
    
    def __eq__(self, bd : 'Board') -> bool:
        try:
            Board.is_board(bd)
        except:
            return False
        
        return (self.board==bd.board).all()

    
    
class OwnBoard:
    """各Agentが保持する盤面"""

    def __init__(self, bd : 'Board', color : int) -> None:
        """各Agentが保持する盤面(自分視点)

        Parameters
        ----------
        bd : Board
            相手のAgentと共有するBoard。
            参照渡しであるため、これに変更を加えると相手が保持するBoardも変化する
        color : int
            自分の駒の色。Board.BLACKかBoard.WHITEである必要がある
        """
        Board.is_color(color)
        self.color = color

        self.board = Board(bd=bd, color_switch=False if self.color == Board.BLACK else True)   # 色の反転を行うかを指定し初期化。
        self.common_board = bd   # 相手と共有する盤面

        self.end_label = None   # 終了コード。Agentにとって報酬となるように設計
        self.test_mode = False
        self.log_tree = None
    

    @classmethod
    def is_own_board(cls, own_board : 'OwnBoard'):
        if not isinstance(own_board, OwnBoard):
            TypeError(f"{own_board} is not OwnBoard object")
        
        Board.is_board(own_board.common_board)

        if not(own_board.end_label == 0.0 or\
            own_board.end_label == 0.1 or\
            own_board.end_label == 1.0 or\
            own_board.end_label == None):
            raise ValueError("End label must be 0.0 or 0.1 or 1.0 or None")
            
        
    def update_board(self) -> None:
        """
        共有の盤面が変化しているかをチェックし、終了判定を行う。
        変化している場合は自分視点の盤面も更新(初期化)。
        自分のターンにしか呼び出してはならない
        """
        e = Board.is_end(self.common_board, self.color)
        if not e == None:   # 終了している時
            if e == self.color:
                self.end_label = 1.0   # 勝ちなら終了コード1.0
            elif e == Board.turn_color(self.color):
                self.end_label = 0.0   # 負けなら終了コード0.0
            else:
                self.end_label = 0.1   # 引き分けなら終了コード0.1
    

    def start_testmode(self):
        self.test_mode = True
        self.test_board = self._translate_to_own()
        self.last_placed = 2
        self.log_tree = Tree((self.last_placed, self.test_board))
    
    def end_testmode(self):
        self.test_mode = False
        self.log_tree = None
        self.test_board = None

        

    def get_place_to_put(self) -> list:
        """次の駒をどこに置けるかを取得

        Returns
        -------
        list
            駒を置ける場所のlist
        """

        if self.test_mode:
            return Board.get_places_to_put(self.test_board, Board.turn_color(self.last_placed))

        self.update_board()   # 盤面の更新
        return Board.get_places_to_put(self.common_board, self.color) if self.end_label == None else []   # 終了していなければ置ける場所を取得し返す
    

    def put(self, place : tuple) -> None:
        """盤面に次のの駒を置く

        Parameters
        ----------
        place : tuple
            駒を置く場所。[0,8)のint二つを要素とする必要がある

        """

        if self.test_mode:
            try:
                next_board = Board.get_board_after_put(self.test_board, place, Board.turn_color(self.last_placed))
                self.last_placed = Board.turn_color(self.last_placed)
                self.log_tree.add((place, self.last_placed, next_board))
                return True
            except:
                return False
        
        self.update_board()   # 盤面の更新
        if not self.end_label == None:   # 終了していれば駒を置ける場所はない
            raise Exception("You can not put a pices any more")
        self.common_board.put(place, self.color)   # 自分視点でErrorが出なければ共通の盤面に駒を置く
    

    def return_log(self, count : int = 1):
        if not self.test_mode:
            raise(Exception("You have to star test mode with \"OwnBoard.start_testmode\" when you want to use this"))
        
        self.log_tree.back(count)
        _, self.last_placed, self.test_board = self.log_tree.get_attention_data()
    
    def get_child(self):
        if not self.test_mode:
            raise(Exception("You have to star test mode with \"OwnBoard.start_testmode\" when you want to use this"))
        
        return self.log_tree.get_child()
    
    def get_parent(self):
        if not self.test_mode:
            raise(Exception("You have to star test mode with \"OwnBoard.start_testmode\" when you want to use this"))
        
        return self.log_tree.get_parent()
    

    def is_end(self) -> float:
        """終了判定を行い、終了コードを返す

        Returns
        -------
        int
            終了コード。勝利なら1.0、負けなら0.0、引き分けなら0.1、終了していなければNone
        """
        self.update_board()   # 盤面の更新
        return self.end_label   # 盤面の更新によって得られた終了コードを出力
    

    def _translate_to_own(self):
        board_array = self.common_board.board
        board_array = (board_array==self.color)*1 + (board_array==Board.turn_color(self.color))*2 + (board_array==Board.EMPTY)*0
        return Board(bd_array=board_array.astype(np.int32))
    
    

    def __str__(self) -> str:
        self.update_board()   # 駒の更新
        if self.end_label == None:   # 終了していない時
            s = str(self._translate_to_own())
            s += f"place to put : {self.get_place_to_put()}"   # 自身の色と置ける場所も出力
        elif self.end_label == 0.0:   # 敗北時
            s = f"----------------------\n   You lose {self.common_board.numbers[Board.turn_color(self.color)]:02} - {self.common_board.numbers[self.color]:02}   \n----------------------"
        elif self.end_label == 1.0:   # 勝利時
            s = f"---------------------\n   You won {self.common_board.numbers[self.color]:02} - {self.common_board.numbers[Board.turn_color(self.color)]:02}   \n---------------------"
        else:   # 引き分け時
            s = f"----------------------\n   You drew {self.common_board.numbers[Board.turn_color[self.color]]:02} - {self.common_board.numbers[self.color]:02}   \n----------------------"
        return s
    


if __name__ == "__main__":
    bd = Board()
    color = Board.BLACK

    # print(board.get_change_places(bd, (5, 4), 2))
    while True:
        print(bd)
        print(f"Places to put : {Board.get_places_to_put(bd, color)}")
        bd.put(tuple(map(int, input("put:").split())), color)
        color = Board.turn_color(color)
