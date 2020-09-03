import GameplayKernal
from AutoPlayerDef import AutoPlayer 
import AutoPlayerDef
from GameRecorder import Recorder

def SimulateGame(count):
    # prepare kernal and players
    kernal = GameplayKernal.Kernal()
    player1 = AutoPlayer(AutoPlayerDef.CONST_RANDOM_MODE,GameplayKernal.CONST_PLAYER1)
    player2 = AutoPlayer(AutoPlayerDef.CONST_RANDOM_MODE,GameplayKernal.CONST_PLATER2)
    recorder = Recorder()
    # simulate game for many times 
    for i in range(count):
        # reset game to start
        kernal.ResetGame()
        recorder.RecordGameStart(kernal.GetGameState())
        # play till game end
        while kernal.GetGameState().winInfo == GameplayKernal.CONST_GAME_DRAWN:
            curState = kernal.GetGameState()
            # players make decisions
            events1 = kernal.OnUserInput(player1.GetInput(curState))
            events2 = kernal.OnUserInput(player2.GetInput(curState))
            # inform keranl one round end
            events3 = kernal.OnEndOfRound()
            # record
            recorder.RecordEvents(events1+events2+events3)
        # record ending
        recorder.RecordGameEnd(kernal.GetGameState())
        recorder.PrintLatestGameResult()

    # save log files
    recorder.SaveToFile("playData.txt")
SimulateGame(50)