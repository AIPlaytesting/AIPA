import GameplayKernal
from AutoPlayerDef import AutoPlayer 
import AutoPlayerDef
from GameRecorder import Recorder
import AI_Brain

#start with 80% exploration
start_epsilon = 0.8 

def SimulateGame(count):
    # prepare kernal and players
    kernal = GameplayKernal.Kernal()
    player1 = AI_Brain.PlayerBrain(1)
    player2 = AutoPlayer(AutoPlayerDef.CONST_RANDOM_MODE,GameplayKernal.CONST_PLATER2)
    recorder = Recorder()
    # simulate game for many times 
    for i in range(count):
        
        #manage epsilon decay
        epsilon = start_epsilon - (start_epsilon * i/count)
        
        # reset game to start
        kernal.ResetGame()
        recorder.RecordGameStart(kernal.GetGameState())
        # play till game end
        while kernal.GetGameState().winInfo == GameplayKernal.CONST_GAME_DRAW:
            # get current state
            curState = kernal.GetGameState()
            # players make decisions
            events1 = kernal.OnUserInput(player1.GetInput(curState, epsilon))
            events2 = kernal.OnUserInput(player2.GetInput(curState))
            # inform kernel at the end of this round
            events3 = kernal.OnEndOfRound()
            
            player1.UpdateCurrentReward(events3[0].winInfo)
            
            # record
            recorder.RecordEvents(events1+events2+events3)
        # record ending
        recorder.RecordGameEnd(kernal.GetGameState())
        #recorder.PrintLatestGameResult()

    print(player1.q_table)

    # save log files
    recorder.SaveToFile("playData.txt")
SimulateGame(500000)