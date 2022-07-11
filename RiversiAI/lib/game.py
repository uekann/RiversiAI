from riversi import Board, OwnBoard
from agent import Agent, AgentRandom


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
            self.agent1.set_own_board(OwnBoard(self.board, 1))

        if (not self.agent2 == None) and self.agent2.own_board == None:
            self.agent2.set_own_board(OwnBoard(self.board, 2))
    
    def set_agent1(self, ag1 : 'Agent'):
        if not isinstance(ag1, Agent):
            raise TypeError("The argment \"ag1\" must be instance of \"Agnet\"")
        self.agent1 = ag1

        if (not self.board == None) and self.agent1.own_board == None:
            self.agent1.set_own_board(OwnBoard(self.board, 1))
    
    def set_agent2(self, ag2 : 'Agent'):
        self.agent2 = ag2
        if not isinstance(ag2, Agent):
            raise TypeError("The argment \"ag1\" must be instance of \"Agnet\"")

        if (not self.board == None) and self.agent2.own_board == None:
            self.agent2.set_own_board(OwnBoard(self.board, 2))
    
    def set_agents(self, ag1 : 'Agent', ag2 : 'Agent'):
        self.set_agent1(ag1)
        self.set_agent2(ag2)
    

    def new_game(self):
        self.board = Board()
        self.agent1, self.agent2 = self.agent2, self.agent1
        self.agent1.change_board(self.board, 1)
        self.agent2.change_board(self.board, 2)


    
    def play(self):
        while True:
            while Board.is_end(self.board, 1) == None:
                self.agent1.action()
                self.agent2.action()
            
            self.agent1.result()
            self.agent2.result()

            if not(self.agent1.next_game or self.agent2.next_game):
                break

            self.new_game()

class GameGUI:
    def __init__(self) -> None:
        self.board = Board()
        self.opponent = AgentRandom(OwnBoard(self.board, 2))
        self.last_placed = 2
    
    def update(self):
        if self.last_placed == 1:
            self.opponent.action()
            self.last_placed = 2
        
        return Board.is_end(self.board, Board.turn_color(self.last_placed))
    
    def put(self, x, y):
        if not self.update():
            self.last_placed = 1
            try:
                self.board.put((x, y), 1)
            except:
                if not Board.get_places_to_put(self.board, 1) == []:
                    self.last_placed = 2
            # print(self.board)