import GameplayKernal
import random

CONST_RANDOM_MODE = 0
CONST_ROCK_MODE = 1
CONST_PAPER_MODE = 2
CONST_SCISSOR_MODE = 3
CONST_DRAGON_MODE = 4
class AutoPlayer:
    def __init__(self, mode, playerTag):
        self.mode = mode
        self.playerTag = playerTag

    # Get input from this player
    # para1: gameState
    # return: [playertag, decision]
    def GetInput(self, gameState):
        decision = GameplayKernal.CONST_NONE_DECISION
        options = [
            GameplayKernal.CONST_ROCK_DECISION,
            GameplayKernal.CONST_PAPER_DECISION,
            GameplayKernal.CONST_SCISSOR_DECISION,
            GameplayKernal.CONST_DRAGON_DECISION]
        # make dicison depending on mode
        if self.mode == CONST_ROCK_MODE:
            decision = options[0]
        elif self.mode == CONST_PAPER_MODE:
            decision = options[1]
        elif self.mode == CONST_SCISSOR_MODE:
            decision = options[2]
        elif self.mode == CONST_DRAGON_MODE:
            decision = options[3]
        else:
            decision = options[random.randint(0, len(options) - 1)]
        # generate input depending on decision
        return GameplayKernal.UserInput(self.playerTag, decision)