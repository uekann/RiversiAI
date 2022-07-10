import random
from abc import ABCMeta, abstractmethod
from .riversi import Board

class Agent(metaclass=ABCMeta):
    """エージェントの基底クラス"""

    def __init__(self, bd=None, color=None) -> None:
        self.board = bd
        self.color = color
    
    def set_board(self, bd):
        if not self.board == None:
            raise Exception("You have alredy set the board")
        
        Board.is_board(bd)
        self.board = bd
    
    def set_color(self, color):
        if not self.color == None:
            raise Exception("You have alredy set the board")
        
        Board.is_color(color)
        self.color = color
    
    @abstractmethod
    def action(self):
        pass


class AgentRandom(Agent):
    """駒を置くことができる座標の一覧から、一様分布に従って行動を選択するAgent"""

    def __init__(self, bd, color) -> None:
        super().__init__(bd, color)
    
    def action(self):
        actions = self.bd.get_places_to_put(self.color)
        self.bd.put(random.randint(0, len(actions)-1))

class HumanPlayer(Agent):
    """人間がプレイするためのクラス"""

    def __init__(self, bd=None, color=None) -> None:
        super().__init__(bd, color)
    
    def action(self):
        
        return