import AI_Module.AI_Brain_Build_v1

import AI_Module.ReplayBuffer
import AI_Module.GameBuffer
import AI_Module.TrainDataWriter
import Environment #also a part of the AI

import os
import time
from datetime import datetime



class AI_Trainer:
    def __init__(self, app_id, deck_id):
        self.app_id = app_id
        self.deck_id = deck_id
        
        #initialize the environment
        self.env = Environment.Environment()

        self.CreateDataSavingPath()

        self.game_buffer = AI_Module.GameBuffer.GameBuffer(self.env.ai_transformer.state_space, self.env.ai_transformer.action_space, self.env.unplayable_card_pun,isCustomCardRewards = False, isTrain=True)
        self.game_buffer.data_collector.StoreDeckConfig(self.env.ai_transformer.deck_config)

        #Replace string with file description is needed
        self.data_writer = AI_Module.TrainDataWriter.TrainDataWriter(self.game_buffer.data_collector, self.train_data_path)

        self.number_of_games = 15000
        self.start_time = time.time()

        #Double Q-Learning
        self.ai_agent = AI_Module.AI_Brain_Build_v1.AI_Brain_B(gamma=0, state_space = self.env.ai_transformer.state_space, action_space = self.env.ai_transformer.action_space,
                        hidden_layer_dims=[128, 64, 32, 32], epsilon=1.0, epsilon_dec=0.0003, epsilon_min = 0.01, mem_size = 250000, batch_size = 128, 
                        model_save_path = self.train_data_path, unplayable_pun = self.env.unplayable_card_pun)


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


    def CreateDataSavingPath(self):
        self.ai_data_root = self.env.ai_transformer.db_root + "\\AI_Data"

        #create special token for this training run
        #time component
        now = datetime.now()
        dt_string = now.strftime("%d-%b-%y %H-%M")
        
        self.main_folder_path = self.ai_data_root
        self.main_folder_path += "\\App_" + self.app_id + "~"
        self.main_folder_path += "Deck_" + self.deck_id + "~"
        self.main_folder_path += dt_string

        os.makedirs(self.main_folder_path)

        #subfolder 1 - model
        self.model_path = self.main_folder_path + "\\Trained_Model\\"

        #subfolder 2 - training data collection
        self.train_data_path = self.main_folder_path + "\\Training_Data\\"
        os.makedirs(self.train_data_path)

        #subfolder 3 - test data collection
        self.test_data_path = self.main_folder_path + "\\Test_Data\\"
        os.makedirs(self.test_data_path)







        
        

