import tensorflow as tf
from tensorflow import keras
from . import ReplayBuffer
import numpy as np


def BuildDeepQNetwork(state_space_dim, action_space_dim, hl1_dim, hl2_dim, hl3_dim, hl4_dim):
    model = keras.Sequential([
        keras.layers.Dense(state_space_dim, activation='relu'),
        keras.layers.Dense(hl1_dim, activation='relu'),
        keras.layers.Dense(hl2_dim, activation='relu'),
        keras.layers.Dense(hl3_dim, activation='relu'),
        #Dont want any activation for the output layer since it is the Q-value
        keras.layers.Dense(action_space_dim, activation=None)
    ])

    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy', 'mean_squared_error'])
    return model

class AI_Brain:
    
    def __init__(self, gamma,
        action_space_dim,
        epsilon, epsilon_dec, epsilon_min, 
        mem_size, batch_size):

        self.buff_buffer = ReplayBuffer.ReplayBuffer(7, mem_size)
        self.cards_buffer = ReplayBuffer.ReplayBuffer(13, batch_size)
        self.action_space = [i for i in range(action_space_dim)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.mem_size = mem_size
        self.batch_size = batch_size

        self.buff_q_model = BuildDeepQNetwork(
            state_space_dim=7,
            action_space_dim= action_space_dim,
            hl1_dim= 32,
            hl2_dim = 32,
            hl3_dim = 32,
            hl4_dim = 32
        )

        self.cards_q_model = BuildDeepQNetwork(
            state_space_dim = 13,
            action_space_dim = action_space_dim,
            hl1_dim = 32,
            hl2_dim = 32,
            hl3_dim = 32,
            hl4_dim = 32
        )


    

    def PredictAction(self, state):
        
        if (np.random.random() < self.epsilon) :
            #create an array of random values
            actions = np.random.rand(len(self.action_space))
        else:
            buff_state, cards_state = self.CondenseState(state)
            buff_actions = self.buff_q_model.predict(np.array([buff_state], dtype=float))
            cards_action = self.cards_q_model.predict(np.array([cards_state], dtype=float))
            actions = 0.5*buff_actions[0] + 0.5*cards_action[0]

        return actions


    def CondenseState(self, state):
        buff_model_state = [state[3], state[4], state[5], state[16], state[24], state[25], state[28]]
        cards_model_state = [state[0], state[55], state[56], state[57], state[58], state[59], state[60], state[61], state[62], state[63], state[64], state[65], state[66]]
        boss_intent_model_state = [state[91], state[92], state[93], state[94], state[95], state[96], state[97]]

        return buff_model_state, cards_model_state
        

    def Learn(self):
        
        if self.buff_buffer.mem_ctr < self.batch_size :
            return
        
        buff_states, buff_new_states, rewards, actions, isTerminals = self.buff_buffer.SampleBuffer(self.batch_size)

        #predict function takes in state/s and returns action space predictions
        buff_state_predicts = self.buff_q_model.predict(buff_states)
        buff_new_state_predicts = self.buff_q_model.predict(buff_new_states)
        
        batch_index = np.arange(self.batch_size, dtype=int)
        actions = actions.astype(int)
        buff_q_target = np.copy(buff_state_predicts)

        buff_q_target[batch_index, actions] = rewards + self.gamma * np.max(buff_new_state_predicts) * isTerminals
        #training model
        self.buff_q_model.train_on_batch(buff_states, buff_q_target)

        cards_states, cards_new_states, rewards, actions, isTerminals = self.cards_buffer.SampleBuffer(self.batch_size)

        #predict function takes in state/s and returns action space predictions
        cards_state_predicts = self.cards_q_model.predict(cards_states)
        cards_new_state_predicts = self.cards_q_model.predict(cards_new_states)
        
        batch_index = np.arange(self.batch_size, dtype=int)
        actions = actions.astype(int)
        cards_q_target = np.copy(cards_state_predicts)

        cards_q_target[batch_index, actions] = rewards + self.gamma * np.max(cards_new_state_predicts) * isTerminals
        #training model
        self.cards_q_model.train_on_batch(cards_states, cards_q_target)

        #epsilon update
        if(self.epsilon <= 0):
            self.epsilon = self.epsilon_min
        elif self.epsilon > self.epsilon_min :
            self.epsilon -= self.epsilon_dec
        else:
            self.epsilon = self.epsilon_min



    def StoreTransition(self, state, new_state, action, reward, isTerminal):
        buff_state, cards_state = self.CondenseState(state)
        buff_new_state, cards_new_state = self.CondenseState(new_state)

        self.buff_buffer.StoreTransition(buff_state, buff_new_state, action, reward, isTerminal)
        self.cards_buffer.StoreTransition(cards_state, cards_new_state, action, reward, isTerminal)


    def SaveModel(self, filepath):
        self.buff_q_model.save(filepath)


    def LoadModel(self, filepath):
        self.buff_q_model = self.buff_q_model.load_model(filepath)
    