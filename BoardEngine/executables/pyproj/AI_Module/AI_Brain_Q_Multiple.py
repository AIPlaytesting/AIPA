import tensorflow as tf
from tensorflow import keras
import numpy as np
from . import ReplayBuffer


def BuildBuffModel():
    model1 = keras.Sequential([
        keras.layers.Dense(9, activation='sigmoid'),
        keras.layers.Dense(32, activation='sigmoid'),
        keras.layers.Dense(32, activation='sigmoid'),
        keras.layers.Dense(12, activation=None)
    ])

    model1.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'])
    return model1


def BuildCardsModel():
    model2 = keras.Sequential([
        keras.layers.Dense(15, activation='sigmoid'),
        keras.layers.Dense(32, activation='sigmoid'),
        keras.layers.Dense(32, activation='sigmoid'),
        #Dont want any activation for the output layer since it is the Q-value
        keras.layers.Dense(12, activation=None)
    ])

    model2.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'] )
    return model2


def BuildBossIntentModel():
    model3 = keras.Sequential([
        keras.layers.Dense(9, activation='sigmoid'),
        keras.layers.Dense(32, activation='sigmoid'),
        keras.layers.Dense(32, activation='sigmoid'),
        keras.layers.Dense(12, activation=None)
    ])

    model3.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'])
    return model3



class AI_Brain:

    def __init__(self, action_space_dim, batch_size, gamma, eps, eps_min, eps_dec):
        self.action_space =[i for i in range(action_space_dim)]
        self.batch_size = batch_size
        self.gamma = gamma
        self.epsilon = eps
        self.epsilon_min = eps_min
        self.epsilon_dec = eps_dec

        #models
        self.buff_q_model = BuildBuffModel()
        self.cards_q_model = BuildCardsModel()
        self.b_intent_q_model = BuildBossIntentModel()

        #buffers
        self.buff_buffer = ReplayBuffer.ReplayBuffer(9, 200000)
        self.cards_buffer = ReplayBuffer.ReplayBuffer(15, 200000)
        self.b_intent_buffer = ReplayBuffer.ReplayBuffer(9, 200000)


    #Diving the entire model into 3 parts
    
    # 1 : The buff model
    # 2 : The cards model
    # 3 : The boss intent model

    #Train all of these separately and then weight the output from each to get 
    #   the tota expected reward.

    def PredictAction(self, state):

        if(np.random.random() < self.epsilon):
            #create an array of random values sampled from guassian distribution
            actions = np.random.rand(12)
        else:
            buff_model_state, card_model_state, boss_intent_model_state = self.DivideStateSpace(state)
            buff_actions = self.buff_q_model.predict(np.array([buff_model_state], dtype=float))[0]
            card_actions = self.cards_q_model.predict(np.array([card_model_state], dtype=float))[0]
            boss_intent_actions = self.b_intent_q_model.predict(np.array([boss_intent_model_state], dtype=float))[0]

            actions = 0.4*buff_actions + 0.2*card_actions + 0.4*boss_intent_actions
            #actions = card_actions

        return actions


    def Learn(self):
        if (self.cards_buffer.mem_ctr < self.batch_size) :
            return

        #training for the buff model
        bu_states, bu_new_states, bu_actions, bu_rewards , bu_isTerminals = self.buff_buffer.SampleBuffer(self.batch_size)
        
        bu_state_predicts = self.buff_q_model.predict(bu_states)
        bu_new_state_predicts = self.buff_q_model.predict(bu_new_states)
        
        batch_index = np.arange(self.batch_size, dtype=int)
        bu_actions = bu_actions.astype(int)
        bu_target = np.copy(bu_state_predicts)
        
        bu_target[batch_index, bu_actions] = bu_rewards + self.gamma * np.max(bu_new_state_predicts) * bu_isTerminals
        self.buff_q_model.train_on_batch(bu_states, bu_target)
        
        #training for the cards model
        ca_states, ca_new_states, ca_actions, ca_rewards, ca_isTerminals = self.cards_buffer.SampleBuffer(self.batch_size)

        ca_state_predicts = self.cards_q_model.predict(ca_states)
        ca_new_state_predicts = self.cards_q_model.predict(ca_new_states)

        ca_actions = ca_actions.astype(int)
        ca_target = np.copy(ca_state_predicts)
        
        ca_target[batch_index, ca_actions] = ca_rewards + self.gamma * np.max(ca_new_state_predicts) * ca_isTerminals
        self.cards_q_model.train_on_batch(ca_states, ca_target)
        
        #training for the buff model
        bi_states, bi_new_states, bi_actions, bi_rewards, bi_isTerminals = self.b_intent_buffer.SampleBuffer(self.batch_size)
        
        bi_state_predicts = self.b_intent_q_model.predict(bi_states)
        bi_new_state_predicts = self.b_intent_q_model.predict(bi_new_states)
        
        bi_actions = bi_actions.astype(int)
        bi_target = np.copy(bi_state_predicts)
        
        bi_target[batch_index, bi_actions] = bi_rewards + self.gamma * np.max(bi_new_state_predicts) * bi_isTerminals
        self.b_intent_q_model.train_on_batch(bi_states, bi_target)
        
        #epsilon update
        if(self.epsilon <= 0):
            self.epsilon = self.epsilon_min
        elif self.epsilon > self.epsilon_min :
            self.epsilon -= self.epsilon_dec
        else:
            self.epsilon = self.epsilon_min


    def DivideStateSpace(self, state):

        buff_model_state = [state[1], state[22], state[3], state[4], state[5], state[16], state[24], state[25], state[28]]
        card_model_state = [state[1], state[22], state[0], state[55], state[56], state[57], state[58], state[59], state[60], state[61], state[62], state[63], state[64], state[65], state[66]]
        boss_intent_model_state = [state[1], state[22], state[91], state[92], state[93], state[94], state[95], state[96], state[97]]
        
        return buff_model_state, card_model_state, boss_intent_model_state

    
    def StoreTransition(self, state, new_state, action, reward, isTerminal):

        buff_model_state, card_model_state, boss_intent_model_state = self.DivideStateSpace(state)
        buff_model_n_state, card_model_n_state, boss_intent_model_n_state = self.DivideStateSpace(new_state)

        self.buff_buffer.StoreTransition(buff_model_state, buff_model_n_state, action,reward, isTerminal)
        self.cards_buffer.StoreTransition(card_model_state, card_model_n_state, action,reward, isTerminal)
        self.b_intent_buffer.StoreTransition(boss_intent_model_state, boss_intent_model_n_state, action,reward, isTerminal)
