import AI_Module.AI_Tester
import AI_Module.GameBuffer
import AI_Module.TestDataWriter

import Environment #also a part of the AI

import os
import time
from datetime import datetime



class AI_Tester:
    def __init__(self, app_id, deck_id, special_folder_name=""):
        self.app_id = app_id
        self.deck_id = deck_id
        self.special_path = special_folder_name
        
        #initialize the environment
        self.env = Environment.Environment()

        self.CreateDataSavingPath()

        self.game_buffer = AI_Module.GameBuffer.GameBuffer(self.env.ai_transformer.state_space, self.env.ai_transformer.action_space, self.env.unplayable_card_pun, isCustomCardRewards = False, isTrain=False)
        self.game_buffer.data_collector.StoreDeckConfig(self.env.ai_transformer.deck_config)

        self.test_data_writer = AI_Module.TestDataWriter.TestDataWriter(self.game_buffer.data_collector, test_data_path=self.test_data_path)
        
        self.start_time = time.time()

        #AI Tester
        self.ai_tester = AI_Module.AI_Tester.AI_Tester(self.model_path)


    def TestOneIteration(self, test_itr):

        done = False
        state = self.env.Reset()

        game_start_time = time.time()
        prediction_time = 0

        while not done:
            start_prediction_time = time.time()
            
            action_space_vec, isRandom = self.ai_tester.PredictAction(state)
            
            end_prediction_time = time.time()
            prediction_time += end_prediction_time - start_prediction_time

            new_state, action, reward, done, isTurnEnd = self.env.Step(action_space_vec, isRandom)
            
            if(action == -1):
                self.game_buffer.TurnEnd()

            self.game_buffer.StoreByTurns(state, new_state, action, reward, done, isTurnEnd)
                
            state = new_state

        game_end_time = time.time()
        game_play_time = (game_end_time - game_start_time) - prediction_time
        test_time = (game_end_time - game_start_time)

        self.game_buffer.TurnEnd()
        self.game_buffer.RewardCalculations()

        self.game_buffer.StoreGameData(0, self.env.win_int, new_state, prediction_time, game_play_time, test_time)
        self.game_buffer.ResetBuffer()

        return test_time


    def ProcessDataAndWriteFiles(self):
        self.test_data_writer.GetDataFromCollector()
        self.test_data_writer.WriteCSVFiles()
        self.test_data_writer.WriteJSONFiles()


    def CreateDataSavingPath(self):
        self.ai_data_root = self.env.ai_transformer.db_root + "\\AI_Data"
        self.main_folder_path = ""

        if self.special_path == "":
            #check subdirectories
            sub_dirs = [f.name for f in os.scandir(self.ai_data_root) if f.is_dir()]

            for dir_name in sub_dirs:
                name_comp = dir_name.split('~')
                if name_comp > 2:
                    app_id_l = name_comp[0].split('_')
                    app_id_l = app_id_l[1]
                    deck_id_l = name_comp[1].split('_')
                    deck_id_l = deck_id_l[1]
                    
                    if app_id_l == self.app_id and deck_id_l == self.deck_id:
                        self.main_folder_path = self.ai_data_root + "\\" + dir_name
                        break
        else:
            self.main_folder_path = self.ai_data_root + "\\" + self.special_path

        self.main_folder_path = self.ai_data_root

        #subfolder 1 - model
        self.model_path = self.main_folder_path + "\\Trained_Model\\"

        #subfolder 2 - training data collection
        self.train_data_path = self.main_folder_path + "\\Training_Data\\"

        #subfolder 3 - test data collection
        self.test_data_path = self.main_folder_path + "\\Test_Data\\"



