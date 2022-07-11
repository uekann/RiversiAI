from ReversiAI.lib.riversi import Board
from lib import game, riversi, agent

if __name__ == "__main__":
    board = riversi.Board()
    player = agent.HumanPlayer(riversi.OwnBoard(board, Board.BLACK))
    cpu = agent.AgentRandom(riversi.OwnBoard(board, Board.WHITE))
    
    game.play(board, player, cpu)