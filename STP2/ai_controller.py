import AI_Module.AI_Brain_Build_v1

import AI_Module.ReplayBuffer
import AI_Module.GameBuffer
import AI_Module.DataWriter
import Environment #also a part of the AI

import numpy as np
import csv
import time
import winsound


class AI_Trainer:
    def __init__(self):
        #initialize the environment
        self.env = Environment.Environment()

        self.game_buffer = AI_Module.GameBuffer.GameBuffer(self.env.ai_transformer.state_space, self.env.ai_transformer.action_space, self.env.unplayable_card_pun,isCustomCardRewards = False)
        self.game_buffer.data_collector.StoreDeckConfig(self.env.ai_transformer.deck_config)

        #Replace string with file description is needed
        self.data_writer = AI_Module.DataWriter.DataWriter(self.game_buffer.data_collector, 'batch size low - nn complex lowered')

        self.number_of_games = 15000
        self.start_time = time.time()

        #Double Q-Learning
        self.ai_agent = AI_Module.AI_Brain_Build_v1.AI_Brain_B(gamma=0, state_space = self.env.ai_transformer.state_space, action_space = self.env.ai_transformer.action_space,
                        hidden_layer_dims=[128, 64, 32, 32], epsilon=1.0, epsilon_dec=0.0003, epsilon_min = 0.01, mem_size = 250000, batch_size = 128, unplayable_pun = self.env.unplayable_card_pun)


    def TrainOneIteration(self, train_itr):

        #turn_buffer = AI_Module.ReplayBuffer.ReplayBuffer(98, 1000)

        done = False
        state = self.env.Reset()
        episode_len = 0

        game_start_time = time.time()
        prediction_time = 0

        while not done:
            start_prediction_time = time.time()
            
            action_space_vec, isRandom = self.ai_agent.PredictAction(state)
            
            end_prediction_time = time.time()
            prediction_time += end_prediction_time - start_prediction_time

            new_state, action, reward, done, isTurnEnd = self.env.Step(action_space_vec, isRandom)
            
            episode_len += 1
            
            if(action == -1):
                self.game_buffer.TurnEnd()

            self.game_buffer.StoreByTurns(state, new_state, action, reward, done, isTurnEnd)
                
            state = new_state

        game_end_time = time.time()
        game_play_time = (game_end_time - game_start_time) - prediction_time

        self.game_buffer.TurnEnd()
        self.game_buffer.RewardCalculations()

        start_train_time = time.time()
        
        self.game_buffer.TransferToReplayBuffer(self.ai_agent, self.env.win_int)
        
        end_train_time = time.time()
        train_time = end_train_time - start_train_time

        self.game_buffer.StoreGameData(self.ai_agent.epsilon, self.env.win_int, new_state, prediction_time, game_play_time, train_time)
        self.game_buffer.ResetBuffer()


        if (train_itr != 0 and (train_itr + 1) % 100 == 0):
            self.data_writer.WriteFile()
            self.ai_agent.SaveModel()

        return end_train_time - game_start_time



