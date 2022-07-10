from .riversi import Board
from .agent import Agent


def play(bd, ag1, ag2):
    if not (isinstance(bd, Board) and isinstance(ag1, Agent) and isinstance(ag2, Agent)):
        raise TypeError("Function \"play\" need 1 Board object and 2 Agent object")
    
    ag1.board = bd
    ag2.board = bd

    ag1.color = Board.WHITE
    ag2.color = Board.WHITE