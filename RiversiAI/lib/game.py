from .riversi import Board, OwnBoard
from .agent import Agent


class Game:
    def __init__(self, bd : 'Board' = None, ag1 : 'Agent' = None, ag2 : 'Agent' = None) -> None:
        self.board = None
        self.agent1 = None
        self.agent2 = None

        if not bd == None:
            self.set_board(bd)
        
        if not ag1 == None:
            self.set_agent1(ag1)
        
        if not ag2 == None:
            self.set_agent2(ag2)
    
    def set_board(self, bd : 'Board'):
        Board.is_board(bd)
        self.board = bd

        if (not self.agent1 == None) and self.agent1.own_board == None:
            self.agent1.set_board(OwnBoard(self.board, 1))

        if (not self.agent2 == None) and self.agent2.own_board == None:
            self.agent2.set_board(OwnBoard(self.board, 2))
    
    def set_agent1(self, ag1 : 'Agent'):
        if not isinstance(ag1, Agent):
            raise TypeError("The argment \"ag1\" must be instance of \"Agnet\"")
        self.agent1 = ag1

        if (not self.board == None) and self.agent1.own_board == None:
            self.agent1.set_board(OwnBoard(self.board, 1))
    
    def set_agent2(self, ag2 : 'Agent'):
        self.agent2 = ag2
        if not isinstance(ag2, Agent):
            raise TypeError("The argment \"ag1\" must be instance of \"Agnet\"")

        if (not self.board == None) and self.agent2.own_board == None:
            self.agent2.set_board(OwnBoard(self.board, 2))
    
    def set_agents(self, ag1 : 'Agent', ag2 : 'Agent'):
        self.set_agent1(ag1)
        self.set_agent2(ag2)
    
    def play(self):
        while Board.is_end(self.board, 1) == None:
            self.agent1.action()
            self.agent2.action()
        self.agent1.result()
        self.agent2.result()