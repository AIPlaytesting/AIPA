
import tensorflow as tf
from tensorflow import keras
import AI_Module.AI_Transformer
import game_manager
import numpy as np

class AI_Player:

    def __init__(self, game_manager: game_manager.GameManager = None):
        self.LoadModel('14-Oct-20 21-22 saved-model')
        self.ai_transformer = AI_Module.AI_Transformer.AI_Transformer()
        self.state_space = self.ai_transformer.state_space
        self.action_space = self.ai_transformer.action_space
        self.game_manager = game_manager

    #This class should be able to load a saved model file and convert it into a tensorflow model
    def LoadModel(self, model_folder_name=''):

        if model_folder_name == '':
            model_folder_name = '14-Oct-20 21-22 saved-model'

        model_path = 'Shared Models\\' + model_folder_name
        self.q_model = tf.keras.models.load_model(model_path)
        self.q_model.summary()
        print("Model Loaded at Path -  " + model_path)
        


    #Communicate with the AI_Transformer to get the lastest state
    #Use the state information to predict an action
    def GetActionVector(self):
        ai_state = self.ai_transformer.GetAIStateSpace(self.game_manager.game_state, self.game_manager.get_current_playable_cards())
        print(ai_state)
        action_vec = self.q_model.__call__(np.array([ai_state], dtype = np.float))

        return action_vec

    #TODO : Need some code to save the state and action space in the Saved Model folder in order to make sure that this class can get the same action space


