# rock/paper/scissor
CONST_NONE_DECISION = "none"
CONST_ROCK_DECISION = "rock"
CONST_PAPER_DECISION = "paper"
CONST_SCISSOR_DECISION= "scissor"
CONST_DRAGON_DECISION = "dragon"
# player
CONST_PLAYER1 = 1
CONST_PLATER2 = 2
# game state
CONST_PLAYER1_WIN = "player 1 Win"
CONST_PLAYER2_WIN = "player 2 Win"
CONST_GAME_DRAW = "draw"

class GameState:
    def __init__(self):
        self.player1Decision = CONST_NONE_DECISION  
        self.player2Decision = CONST_NONE_DECISION  
        self.winInfo = CONST_GAME_DRAW

    # NEED IMPLEMENTATION!!! 
    def Apply(self, gameEvent):
        # pass
        if gameEvent.isDecisionMade:
            # update user decision on this step
            if gameEvent.player == CONST_PLAYER1:
                self.player1Decision = gameEvent.decision
            else:
                self.player2Decision = gameEvent.decision
        elif gameEvent.isRoundEnd:
            # update game result based on current state and user inputs
             self.winInfo = gameEvent.winInfo

    def InitForGameStart(self):
        self.player1Decision = CONST_NONE_DECISION  
        self.player2Decision = CONST_NONE_DECISION  
        self.winInfo = CONST_GAME_DRAW

    def MakeCopy(self):
        copy  = GameState()
        copy.player1Decision = self.player1Decision
        copy.player2Decision = self.player2Decision
        copy.winInfo = self.winInfo
        return copy

class UserInput:
    def __init__(self, playerTag, decision):
        self.playerTag =  playerTag
        self.decision = decision

class GameEvent:
     def __init__(self):
        self.isDecisionMade = False
        self.player = CONST_PLAYER1
        self.decision = CONST_NONE_DECISION
        self.isRoundEnd = False
        self.winInfo= CONST_GAME_DRAW
    
class Kernal:
    def __init__(self):
        self.__gameState = GameState()

    def ResetGame(self):
        self.__gameState.winInfo = CONST_GAME_DRAW
        self.__gameState.player1Decision = CONST_NONE_DECISION
        self.__gameState.player2Decision = CONST_NONE_DECISION

    # NEED IMPLEMENTATION!!! 
    def OnUserInput(self, userInput): # return GameEvent[]
        # pass
        # calculate event triggered by this input
        events = self.__CalculateEvents(userInput)
        # apply gameEvent to change State
        for e in events:
            self.__gameState.Apply(e)
        return events

    # NEED IMPLEMENTATION!!! 
    def OnEndOfRound(self): # return GameEvent[]
        # pass
        roundEndEvent = GameEvent()      
        roundEndEvent.isRoundEnd = True
        # calculate win info
        d1, d2 = self.__gameState.player1Decision, self.__gameState.player2Decision
        if d1 == d2:
            roundEndEvent.winInfo = CONST_GAME_DRAW
        elif d1 == CONST_DRAGON_DECISION:
            roundEndEvent.winInfo = CONST_PLAYER1_WIN
        elif d1 == CONST_ROCK_DECISION:
            roundEndEvent.winInfo = CONST_PLAYER1_WIN if d2 == CONST_SCISSOR_DECISION else CONST_PLAYER2_WIN
        elif d1 == CONST_PAPER_DECISION:
            roundEndEvent.winInfo = CONST_PLAYER1_WIN if d2 == CONST_ROCK_DECISION else CONST_PLAYER2_WIN
        elif d1 == CONST_SCISSOR_DECISION:
            roundEndEvent.winInfo = CONST_PLAYER1_WIN if d2 == CONST_PAPER_DECISION else CONST_PLAYER2_WIN
        else:
            # other cases
            roundEndEvent.winInfo = CONST_PLAYER1_WIN

        self.__gameState.Apply(roundEndEvent)
        return [roundEndEvent]  

    def GetGameState(self):  # return GameState
        return self.__gameState.MakeCopy()

    # NEED IMPLEMENTATION!!! 
    def __CalculateEvents(self, userInput):    # return GameEvent[]
        # pass
        playerDecisonEvent = GameEvent()      
        playerDecisonEvent.isDecisionMade = True
        playerDecisonEvent.decision = userInput.decision
        playerDecisonEvent.player = userInput.playerTag    
        return [playerDecisonEvent]  

