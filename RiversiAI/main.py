from lib import Game
from lib import Board
from lib import CUIPlayer, AgentRandom

if __name__ == "__main__":
    game = Game(Board(), CUIPlayer(), AgentRandom())
    game.play()