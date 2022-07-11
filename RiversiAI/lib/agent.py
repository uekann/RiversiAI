from copy import deepcopy
import random
from abc import ABCMeta, abstractmethod
from .riversi import Board, OwnBoard

class Agent(metaclass=ABCMeta):
    """エージェントの基底クラス"""

    def __init__(self, own_board : 'OwnBoard' = None) -> None:
        """全Agentの抽象基底クラス。このクラスを継承したクラスは関数"action"を定義する必要がある

        Parameters
        ----------
        own_board : OwnBoard, optional
            自分視点の盤面。デフォルトはNone
        """
        self.own_board = own_board
    
    def set_board(self, own_board):
        if not self.own_board == None:
            Exception("You alredy have your own board")
        
        OwnBoard.is_own_board(own_board)
        self.own_board = own_board
        
    def change_own_board(self, own_board):
        OwnBoard.is_own_board(own_board)
        self.own_board = own_board
    
    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def result(self):
        pass


class AgentRandom(Agent):
    """駒を置くことができる座標の一覧から、一様分布に従って行動を選択するAgent"""

    def __init__(self, own_board : 'OwnBoard' = None) -> None:
        super(AgentRandom, self).__init__(own_board)
    
    def action(self):
        actions = self.own_board.get_place_to_put()
        if actions == []:
            return

        self.own_board.put(actions[random.randint(0, len(actions)-1)])
    
    def result(self):
        pass


class HumanPlayer(Agent):
    """人間がプレイするためのクラス"""

    def __init__(self, own_board : 'OwnBoard' = None) -> None:
        super(HumanPlayer, self).__init__(own_board)
    
    def action(self):
        print(self.own_board)
        if not self.own_board.is_end():
            self.own_board.put(tuple(map(int, input("put : ").split())))
    
    def result(self):
        print(self.own_board)