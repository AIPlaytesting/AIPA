import numpy as np
import GameplayKernal as gk

class PlayerBrain:

    def __init__(self, playerTag):
        self.playerTag = playerTag
        self.q_table = np.zeros((4), dtype = 'float')
        self.epsilon = 0.5
        self.learningRate = 0.1


    def CreateUserInput(self, decision):
        
        if(decision == 0):
            decision = gk.CONST_ROCK_DECISION
        elif(decision == 1):
            decision = gk.CONST_PAPER_DECISION
        elif(decision == 2):
            decision = gk.CONST_SCISSOR_DECISION
        elif(decision == 3):
            decision = gk.CONST_DRAGON_DECISION
            
        userInput = gk.UserInput(self.playerTag, decision)
        return userInput

    def GetInput(self, currentState, epsilon):
        
        #Uses epsilon greedy method to decide a value
        if np.random.random() >= epsilon:
            q_value = np.max(self.q_table)
            self.decision = np.where(self.q_table == q_value)[0][0]
        else:
            self.decision = np.random.randint(0,4)
            q_value = self.q_table[self.decision]
            
        inputFromDecision = self.CreateUserInput(self.decision)
        
        return inputFromDecision
    
    def UpdateCurrentReward(self, currentState):
        if(self.playerTag == 1):
            if(currentState == gk.CONST_PLAYER1_WIN):
                self.currentReward = 1
            else:
                self.currentReward = 0
        else:
            if(currentState == gk.CONST_PLAYER2_WIN):
                self.currentReward = 1
            else:
                self.currentReward = 0
        
        q_value = self.q_table[self.decision]
        self.q_table[self.decision]  = q_value + self.learningRate * self.currentReward
    
        
        
