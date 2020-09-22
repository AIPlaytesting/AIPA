import numpy as np


class ReplayBuffer:
    
    def __init__(self, state_space_dim, mem_size):
        self.mem_size = mem_size
        self.mem_ctr = 0

        self.state_memory = np.zeros((mem_size, state_space_dim), dtype=np.int)
        self.new_state_memory = np.zeros((mem_size, state_space_dim), dtype=np.int)

        self.action_memory = np.zeros((mem_size), dtype=np.float)
        self.reward_memory = np.zeros((mem_size), dtype=np.float)

        self.terminal_memory = np.zeros((mem_size), dtype=np.int)


    def StoreTransition(self, state, new_state, action, reward, isTerminal):
        index = self.mem_ctr % self.mem_size

        self.state_memory[index] = state
        self.new_state_memory[index] = new_state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = isTerminal

        self.mem_ctr += 1    


    def SampleBuffer(self, batch_size):
        max_mem = min(self.mem_ctr, self.mem_size)

        #np.random.choice below returns an array of size batch_size. Contains elements from 0 - max_mem. No replacement
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        new_states = self.new_state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        terminals = self.terminal_memory[batch]

        return states, new_states, actions, rewards, terminals

