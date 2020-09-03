from GameplayKernal import GameEvent,GameState
import json

class Recorder:
    def __init__(self):
        self.gamesHistory = []
    def RecordEvents(self,gameEvents):
        self.__CurrentGameLog().gameEvents.extend(gameEvents)

    def RecordGameStart(self, initState):
        self.gamesHistory.append(SingleGameHistory(initState.MakeCopy()))

    def RecordGameEnd(self,endState):
        self.__CurrentGameLog().endGameState = endState.MakeCopy()

    def PrintLatestGameResult(self):
        endState = self.__CurrentGameLog().endGameState
        print("result: ",endState.winInfo," |player1: ",endState.player1Decision," |player2: ",endState.player2Decision)

    def SaveToFile(self,fileName):
        f = open(fileName, "w")
        for gameHistory in self.gamesHistory:
            f.write(gameHistory.ToJSON())
            f.write("\n")
        f.close()

    def __CurrentGameLog(self):
        return self.gamesHistory[-1]
    
class SingleGameHistory:
    def __init__(self,startGameState):
        self.startGameState = startGameState
        self.gameEvents = []
        self.endGameState = None

    def ToJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__)