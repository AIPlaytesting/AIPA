import tensorflow as tf
from tensorflow import keras
from . import ReplayBuffer
import numpy as np


def BuildDeepQNetwork(state_space_dim, action_space_dim, hl1_dim, hl2_dim, hl3_dim, hl4_dim):
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape = state_space_dim),
        keras.layers.Dense(hl1_dim, activation='relu'),
        keras.layers.Dense(hl2_dim, activation='relu'),
        #Dont want any activation for the output layer since it is the Q-value
        keras.layers.Dense(action_space_dim, activation=None)
    ])

    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy', 'mean_squared_error'])

    return model

class AI_Brain:
    
    def __init__(self, gamma,
        state_space_dim, action_space_dim, hidden_layer_dims,
        epsilon, epsilon_dec, epsilon_min, 
        mem_size, batch_size):

        self.replay_buffer = ReplayBuffer.ReplayBuffer(state_space_dim, mem_size)
        self.action_space = [i for i in range(action_space_dim)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.mem_size = mem_size
        self.batch_size = batch_size

        self.q_model = BuildDeepQNetwork(
            state_space_dim=state_space_dim,
            action_space_dim= action_space_dim,
            hl1_dim=hidden_layer_dims[0],
            hl2_dim = hidden_layer_dims[1],
            hl3_dim = hidden_layer_dims[2],
            hl4_dim = hidden_layer_dims[3]
        )



    def PredictAction(self, state):
        #use the condense function to reduce the state space
        state = self.CondenseStateSpace(state)
        isRandom = False

        if (np.random.random() < self.epsilon) :
            #create an array of random values
            actions = np.random.rand(len(self.action_space))
            isRandom = True
        else:
            actions = self.q_model.predict(np.array([state], dtype=float))
            actions = actions[0]

        return actions, isRandom


    def CondenseStateSpace(self,state):
        combat_stats = [state[1], state[2], state[22], state[23]]
        buff_model_state = [ state[3], state[4], state[5], state[16], state[24], state[25], state[28]]
        card_model_state = [state[0], state[55], state[56], state[57], state[58], state[59], state[60], state[61], state[62], state[63], state[64], state[65], state[66]]
        boss_intent_model_state = [state[91], state[92], state[93], state[94], state[95], state[96], state[97]]

        return combat_stats + buff_model_state + card_model_state + boss_intent_model_state
        #return card_model_state

    def Learn(self):
        
        if self.replay_buffer.mem_ctr < self.batch_size :
            return

        sample_indexes = np.arange(self.batch_size)
        sample_indexes += (self.replay_buffer.mem_ctr % self.replay_buffer.mem_size) - self.batch_size

        states, new_states, actions, rewards, isTerminals = self.replay_buffer.SampleBuffer(self.batch_size)
        #states, new_states, actions, rewards, isTerminals = self.replay_buffer.GetFromBuffer(sample_indexes)

        #predict function takes in state/s and returns action space predictions
        q_state_predicts = self.q_model.predict(states)
        q_new_state_predicts = self.q_model.predict(new_states)
        
        batch_index = np.arange(self.batch_size, dtype=int)
        actions = actions.astype(int)
        q_target = np.copy(q_state_predicts)

        #creating a target that can be used for training
        # indexing of the following is complex:
        # batch_size, actions, rewards, q_new_state_predicts.shape[0], isTerminals have the same dimensions
        # hence imagine that the following is iterating over the length
        # because of numpy indexing the following can be read like :
        # for i in range(len(batch_index)):
        #       q_target[batch_index[i], actions[i]] = rewards[i] + self.gamma * np.max(q_new_state_predicts[i])
        # 
        # notice that only one value (one action neuron's value) per action_space is going to be updated here
        # unsurprising, this value is going to be chosen by 'actions'. Therefore only the taken actions value is updated 
        q_target[batch_index, actions] = rewards + self.gamma * np.max(q_new_state_predicts) * isTerminals


        #training model
        self.q_model.train_on_batch(states, q_target)
        #self.q_model.fit(states, q_target)
        

        #epsilon update
        if(self.epsilon <= 0):
            self.epsilon = self.epsilon_min
        elif self.epsilon > self.epsilon_min :
            self.epsilon -= self.epsilon_dec
        else:
            self.epsilon = self.epsilon_min



    def StoreTransition(self, state, new_state, action, reward, isTerminal):
        state = self.CondenseStateSpace(state)
        new_state = self.CondenseStateSpace(new_state)
        self.replay_buffer.StoreTransition(state, new_state, action, reward, isTerminal)


    def SaveModel(self, filepath):
        self.q_model.save(filepath)

    def LoadModel(self, filepath):
        self.q_model = self.q_model.load_model(filepath)
    