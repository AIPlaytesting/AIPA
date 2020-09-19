import tensorflow as tf
from tensorflow import keras
import ReplayBuffer
import numpy as np


def BuildDeepQNetwork(state_space_dim, action_space_dim, hl1_dim, hl2_dim, hl3_dim, hl4_dim):
    model = keras.Sequential(
        keras.layers.Dense(state_space_dim, activation='relu'),
        keras.layers.Dense(hl1_dim, activation='relu'),
        keras.layers.Dense(hl2_dim, activation='relu'),
        keras.layers.Dense(hl3_dim, activation='relu'),
        keras.layers.Dense(hl4_dim, activation='relu'),
        #Dont want any activation for the output layer since it is the Q-value
        keras.layers.Dense(action_space_dim, activation=None)
    )

    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy', 'mean_squared_error'])

    return model

class AI_Brain:
    
    def __init__(self, gamma,
        state_space_dim, action_space_dim, hidden_layer_dims,
        epsilon, epsilon_dec, epsilon_min, 
        mem_size, batch_size):

        self.replay_buffer = ReplayBuffer.ReplayBuffer(state_space_dim, mem_size)
        self.action_space = np.arange(action_space_dim)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.mem_size = mem_size
        self.batch_size = batch_size

        self.q_model = BuildDeepQNetwork(
            state_space_dim=state_space_dim,
            action_space_dim=action_space_dim,
            hl1_dim=hidden_layer_dims[0],
            hl2_dim = hidden_layer_dims[1],
            hl3_dim = hidden_layer_dims[2],
            hl4_dim = hidden_layer_dims[3]
        )


    

    def PredictAction(self, state):
        
        if (np.random.random() < self.epsilon) :
            action = np.random.choice(self.action_space)
        else:
            state = np.array([state])
            actions = self.q_model.predict(state)
            action = np.argmax(actions)
        
        return action


    def Learn(self):
        
        if self.replay_buffer.mem_ctr < self.batch_size :
            return
        
        states, new_states, rewards, actions, terminals = self.replay_buffer.SampleBuffer(self.batch_size)




    def StoreTransition(self, state, new_state, action, reward, isTerminal):
        self.replay_buffer.StoreTransition(state, new_state, action, reward, isTerminal)


    