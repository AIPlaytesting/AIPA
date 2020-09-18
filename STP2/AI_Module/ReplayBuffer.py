import numpy as np


class ReplayBuffer:
    
    def __init__(self, state_space_dim, action_space_dim, mem_size):
        self.mem_size = mem_size
        self.mem_ctr = 0

        self.state_memory = np.zeros((mem_size, state_space_dim), dtype=np.int)
        self.new_state_memory = np.zeros((mem_size, state_space_dim), dtype=np.int)

        self.action_memory = np.zeros((mem_size), dtype=np.float)
        self.reward_memory = np.zerps((mem_size), dtype=np.float)

        self.terminal_memory = np.zeros((mem_size), dtype=np.int)


    def StoreTransition(self, state, new_state, action, reward, isTerminal):
        index = self.mem_ctr % self.mem_size

        self.state_memory[index] = state
        self.new_state_memory[index] = new_state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = isTerminal
    
    def SampleBuffer(self, batch_size):
        pass



    

