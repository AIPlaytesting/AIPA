import tensorflow as tf
from tensorflow import keras
from . import ReplayBuffer
import numpy as np


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
            #Dont want any activation for the output layer since it is the Q-value
            keras.layers.Dense(action_space_dim, activation=None)
        ])

        model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy', 'mean_squared_error'])

        self.model = model



class AI_Brain:
    
    def __init__(self, gamma,
        state_space_dim, action_space_dim, hidden_layer_dims,
        epsilon, epsilon_dec, epsilon_min, 
        mem_size, batch_size, gamma_max = 0.99):

        self.state_space_dim = state_space_dim
        self.hidden_layer_dims = hidden_layer_dims
        self.action_space_dim = action_space_dim

        self.replay_buffer = ReplayBuffer.ReplayBuffer(self.state_space_dim, mem_size)
        self.action_space = [i for i in range(self.action_space_dim)]
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

        if self.replay_buffer.mem_ctr < self.batch_size :
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


        #training model 0
        self.q_model_current.model.train_on_batch(states, q_target)
        #self.q_model.fit(states, q_target)
        

        #epsilon update
        if(self.epsilon <= 0):
            self.epsilon = self.epsilon_min
        elif self.epsilon > self.epsilon_min :
            self.epsilon -= self.epsilon_dec
        else:
            self.epsilon = self.epsilon_min

        #update q_model training count
        self.q_model_current.training_counter += 1

        if self.q_model_current.training_counter >= 500000:
            self.SwitchQModels()


    def SwitchQModels(self):
        
        #increase gamma until the upper limit = 0.99
        if self.gamma < self.gamma_max:
            self.gamma += 0.2

        if self.gamma > self.gamma_max:
            self.gamma = self.gamma_max
        
        self.q_model_trained = self.q_model_current
        self.q_model_current = self.InitializeNewQModel()
        self.q_model_switch_count += 1
    

    def StoreTransition(self, state, new_state, action, reward, isTerminal):
        self.replay_buffer.StoreTransition(state, new_state, action, reward, isTerminal)


    def SaveModel(self, filepath):
        self.q_model_current.save(filepath)

    def LoadModel(self, filepath):
        self.q_model_current = self.q_model_current.load_model(filepath)
    