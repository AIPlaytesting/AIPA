import tensorflow as tf
from tensorflow import keras
from . import ReplayBuffer
import numpy as np
from datetime import datetime


class Q_Model:

    def __init__(self):
        self.model = None
        self.training_counter = 0

    def BuildDeepQNetwork(self, state_space_dim, action_space_dim, hl1_dim, hl2_dim, hl3_dim, hl4_dim):
        model = keras.Sequential([
            keras.layers.InputLayer(input_shape = state_space_dim),
            keras.layers.Dense(hl1_dim, activation='relu'),
            keras.layers.Dense(hl2_dim, activation='relu'),
            keras.layers.Dense(hl3_dim, activation='relu'),
            #keras.layers.Dense(hl4_dim, activation='relu'),
            #Dont want any activation for the output layer since it is the Q-value
            keras.layers.Dense(action_space_dim, activation=None)
        ])

        model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy', 'mean_squared_error'])

        self.model = model


class AI_Brain_B:
    
    def __init__(self, gamma,
        state_space, action_space, hidden_layer_dims,
        epsilon, epsilon_dec, epsilon_min, 
        mem_size, batch_size, unplayable_pun, model_save_path, gamma_max = 0.99):

        self.state_space_dim = len(state_space)
        self.hidden_layer_dims = hidden_layer_dims
        self.action_space_dim = len(action_space)
        self.state_space = state_space
        self.action_space = action_space
        self.unplayable_pun = unplayable_pun

        self.replay_buffer = ReplayBuffer.ReplayBuffer(self.state_space_dim, mem_size)
        self.gamma = gamma
        self.gamma_max = gamma_max 
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.mem_size = mem_size
        self.batch_size = batch_size

        self.q_model_current = self.InitializeNewQModel()
        self.q_model_trained = None
        self.q_model_switch_count = 0
        self.q_model_switch_threshold = 1e8
        self.model_save_path = model_save_path + "Training_Model"



    def InitializeNewQModel(self):
        q_model = Q_Model()
        q_model.BuildDeepQNetwork(
            state_space_dim= self.state_space_dim,
            action_space_dim= self.action_space_dim,
            hl1_dim = self.hidden_layer_dims[0],
            hl2_dim = self.hidden_layer_dims[1],
            hl3_dim = self.hidden_layer_dims[2],
            hl4_dim = self.hidden_layer_dims[3]
        )

        return q_model



    def PredictAction(self, state):
        #use the condense function to reduce the state space
        isRandom = False

        if (np.random.random() < self.epsilon) :
            #create an array of random values
            actions = np.random.rand(len(self.action_space))
            isRandom = True
        else:
            if self.q_model_trained != None:
                actions = self.q_model_trained.model.__call__(np.array([state], dtype=float))
            else:
                actions = self.q_model_current.model.__call__(np.array([state], dtype=float))
            
            actions = actions[0]

        return actions, isRandom


    def Learn(self):

        if self.replay_buffer.mem_ctr < max(self.batch_size, 5000):
            return

        sample_indexes = np.arange(self.batch_size)
        sample_indexes += (self.replay_buffer.mem_ctr % self.replay_buffer.mem_size) - self.batch_size

        states, new_states, actions, rewards, isTerminals = self.replay_buffer.SampleBuffer(self.batch_size)
        #states, new_states, actions, rewards, isTerminals = self.replay_buffer.GetFromBuffer(sample_indexes)

        #predict function takes in state/s and returns action space predictions
        if self.q_model_trained != None:
            q_state_predicts = self.q_model_trained.model.predict(states)
            q_new_state_predicts = self.q_model_trained.model.predict(new_states)
        else:
            q_state_predicts = self.q_model_current.model.predict(states)
            q_new_state_predicts = self.q_model_current.model.predict(new_states)
        
        batch_index = np.arange(self.batch_size, dtype=int)
        actions = actions.astype(int)

        for i in range(len(batch_index)):
            q_state_predicts[i][self.CreateActionMask(states[i])] = -2

        q_target = np.copy(q_state_predicts)

        for i in range(self.batch_size):
            q_target[i, actions[i]] = rewards[i] + self.gamma * np.max(q_new_state_predicts[i]) * isTerminals[i]



        #training model 0
        self.q_model_current.model.train_on_batch(states, q_target)

        #epsilon update
        if(self.epsilon <= 0):
            self.epsilon = self.epsilon_min
        elif self.epsilon > self.epsilon_min :
            self.epsilon -= self.epsilon_dec
        else:
            self.epsilon = self.epsilon_min

        #update q_model training count
        self.q_model_current.training_counter += 1

        if self.q_model_current.training_counter >= self.q_model_switch_threshold:
            self.SwitchQModels()
            #self.q_model_switch_threshold = int(1e7)


    def SwitchQModels(self):
        
        #increase gamma until the upper limit = 0.99
        if self.gamma < self.gamma_max:
            self.gamma += 0.2

        if self.gamma > self.gamma_max:
            self.gamma = self.gamma_max
        
        self.q_model_trained = self.q_model_current
        self.q_model_current = self.InitializeNewQModel()
        self.q_model_current.training_counter = 0
        self.q_model_switch_count += 1


    def StoreTransition(self, state, new_state, action, reward, isTerminal):
        self.replay_buffer.StoreTransition(state, new_state, action, reward, isTerminal)


    def SaveModel(self):
        if self.q_model_trained == None:
            self.q_model_current.model.save(self.model_save_path)
        else:
            self.q_model_trained.model.save(self.model_save_path)

    def LoadModel(self, filepath):
        self.q_model_current = self.q_model_current.load_model(filepath)


    def CreateActionMask(self, state):
        #first we need to get the state values pertaining to the in and and playable cards_state
        action_mask = np.zeros(len(self.action_space), dtype=bool)
        for key in self.action_space:
            action_card = self.action_space[key]
            action_index = key
            card_index_in_state = self.state_space['in_hand_playable_card-' + action_card]
            not_card_in_hand = False if state[card_index_in_state] > 0 else True
            action_mask[action_index] = not_card_in_hand
        
        return action_mask


    def SetModelSaveParams(self, filepath):
        pass