

class GameBuffer:
    
    def __init__(self):

        self.cur_states = []
        self.cur_new_states = []
        self.cur_actions = []
        self.cur_rewards = []
        self.cur_add_rewards = []
        self.cur_terminals = []

        self.state_list_turns = []
        self.new_state_list_turns = []
        self.action_list_turns = []
        self.reward_list_turns = []
        self.add_reward_list_turns = []
        self.terminal_list_turns = []


    def ResetCurrentLists(self):
        self.cur_states = []
        self.cur_new_states = []
        self.cur_actions = []
        self.cur_rewards = []
        self.cur_add_rewards = []
        self.cur_terminals = []

    def ResetBuffer(self):
        self.state_list_turns = []
        self.new_state_list_turns = []
        self.action_list_turns = []
        self.reward_list_turns = []
        self.add_reward_list_turns = []
        self.terminal_list_turns = []
        self.ResetCurrentLists()


    def AddCurrentListsToTurnList(self):
        self.state_list_turns.append(self.cur_states)
        self.new_state_list_turns.append(self.cur_new_states)
        self.action_list_turns.append(self.cur_actions)
        self.reward_list_turns.append(self.cur_rewards)
        self.add_reward_list_turns.append(self.cur_add_rewards)
        self.terminal_list_turns.append(self.cur_terminals)
        

    def StoreByTurns(self, state, new_state, action, reward, isTerminal, isTurnEnd):
        
        self.cur_states.append(state)
        self.cur_new_states.append(new_state)
        self.cur_actions.append(action)
        self.cur_rewards.append(reward)
        self.cur_add_rewards.append(0)
        self.cur_terminals.append(isTerminal)


    def TurnEnd(self):
        if(len(self.cur_states) > 0):
            self.AddCurrentListsToTurnList()
        self.ResetCurrentLists()


    def TransferToReplayBuffer(self, ai_agent):

        for state_list, new_state_list, action_list, reward_list, add_reward_list, terminal_list in \
            zip(self.state_list_turns, self.new_state_list_turns, self.action_list_turns, self.reward_list_turns, self.add_reward_list_turns, self.terminal_list_turns):

            for state, new_state, action, reward, add_reward, terminal in zip(state_list, new_state_list, action_list, reward_list, add_reward_list, terminal_list):

                ai_agent.StoreTransition(state, new_state, action, reward + add_reward, terminal)
                ai_agent.Learn()


    def RewardCalculations(self):
        end_reward_discounted = 0

        for turn_index in range(len(self.state_list_turns) - 1, -1, -1):
            for step_index in range(len(self.state_list_turns[turn_index]) - 1, -1, -1):

                state = self.state_list_turns[turn_index][step_index]
                new_state = self.new_state_list_turns[turn_index][step_index]

                old_player_hp = state[1]
                old_player_block = state[2]
                old_player_energy = state[0]
                new_player_hp = new_state[1]
                new_player_block = new_state[2]
                new_player_energy = new_state[0]

                player_energy_used = old_player_energy - new_player_energy
                energy_multiplier = 2 if player_energy_used == 0 else 1/(player_energy_used)

                old_boss_hp = state[22]
                old_boss_block = state[24]
                new_boss_hp = new_state[22]
                new_boss_block = new_state[24]

                reward_damage = 0

                #REWARD for dealing damage
                damage_dealt = 0
                
                if(old_boss_hp > new_boss_hp):
                    damage_dealt += old_boss_hp - new_boss_hp

                if(old_boss_block > new_boss_block):
                    damage_dealt += old_boss_block - new_boss_block

                reward_damage = damage_dealt * 0.01 * energy_multiplier
                self.add_reward_list_turns[turn_index][step_index] += reward_damage

                #REWARD for BLOCKing damage
                reward_blocked = 0

                if(old_player_block > new_player_block):
                    reward_blocked += (old_player_block - new_player_block) * 0.01
                
                #check when block was added in the steps before this step (in the same turn)
                block_indexes = []
                for another_step_index in range(step_index, -1, -1):
                    defend_played = self.action_list_turns[turn_index][another_step_index] == 1
                    shrug_it_off_played = self.action_list_turns[turn_index][another_step_index] == 2
                    iron_wave_played = self.action_list_turns[turn_index][another_step_index] == 6

                    if(defend_played or shrug_it_off_played or iron_wave_played):
                        block_indexes.append(another_step_index)
                
                for i in range(0, len(block_indexes)):
                    self.add_reward_list_turns[turn_index][i] += reward_blocked / len(block_indexes)

                #REWARD for clothesline
                reward_clothesline = 0
                if (self.action_list_turns[turn_index][step_index] == 11):
                    player_hp_two_turn_end = 0
                    hp_loss_under_weak = 0

                    if turn_index + 2 < len(self.state_list_turns):
                        step_index_turn_end = len(self.state_list_turns[turn_index + 2]) - 1
                        player_hp_two_turn_end = self.state_list_turns[turn_index + 2][step_index_turn_end][1]
                    elif turn_index + 1 < len(self.state_list_turns):
                        step_index_turn_end = len(self.state_list_turns[turn_index + 1]) - 1
                        player_hp_two_turn_end = self.state_list_turns[turn_index + 1][step_index_turn_end][1]
                    else:
                        step_index_turn_end = len(self.state_list_turns[turn_index]) - 1
                        player_hp_two_turn_end = self.state_list_turns[turn_index][step_index_turn_end][1]
                    
                    if(old_player_hp > player_hp_two_turn_end):
                        hp_loss_under_weak = old_player_hp - player_hp_two_turn_end
                    
                    reward_clothesline = (hp_loss_under_weak/3) * 0.01
                

                #REWARD for disarm
                reward_disarm = 0
                if (self.action_list_turns[turn_index][step_index] == 10):
                    boss_damage_instances = 0

                    for another_turn_index in range(turn_index, len(self.state_list_turns)):
                        step_index_turn_end = len(self.state_list_turns[another_turn_index]) - 1

                        old_hp = self.state_list_turns[another_turn_index][step_index_turn_end][1]
                        new_hp = self.new_state_list_turns[another_turn_index][step_index_turn_end][1]
                        old_block = self.state_list_turns[another_turn_index][step_index_turn_end][2]
                        new_block = self.new_state_list_turns[another_turn_index][step_index_turn_end][2]

                        if(old_hp > new_hp) or (old_block > new_block):
                            boss_damage_instances += 1
                        
                    reward_disarm = boss_damage_instances * 2 * 0.01

                #REWARD for Flex damage
                reward_flex = 0

                if(self.action_list_turns[turn_index][step_index] == 8):
                    step_end_index = len(self.state_list_turns[turn_index])
                    cumulative_reward = 0

                    for another_step_index in range(step_index, step_end_index):
                        cumulative_reward += self.add_reward_list_turns[turn_index][another_step_index]

                    reward_flex = cumulative_reward * 0.25 * energy_multiplier

                
                #REWARD for Double Tap
                reward_double_tap = 0

                if(self.action_list_turns[turn_index][step_index] == 9):
                    for another_step_index in range(step_index, len(self.state_list_turns[turn_index])):
                        action_used = self.action_list_turns[turn_index][another_step_index]
                        
                        if action_used in [0, 3, 4, 6, 7, 11]:
                            reward_double_tap += self.add_reward_list_turns[turn_index][another_step_index] * 0.75

                    if (reward_double_tap == 0) and (turn_index + 1 < len(self.state_list_turns)):
                        for another_step_index in range(step_index, len(self.state_list_turns[turn_index + 1])):
                            action_used = self.action_list_turns[turn_index + 1][another_step_index]
                            
                            if action_used in [0, 3, 4, 6, 7, 11]:
                                reward_double_tap += self.add_reward_list_turns[turn_index + 1][another_step_index] * 0.75

                self.add_reward_list_turns[turn_index][step_index] += reward_disarm + reward_clothesline + reward_flex + reward_double_tap


        for turn_index in range(len(self.state_list_turns) - 1, -1, -1):
            for step_index in range(len(self.state_list_turns[turn_index]) - 1, -1, -1):
            
                if (turn_index == len(self.state_list_turns) - 1) and (step_index == len(self.state_list_turns[turn_index]) - 1):
                    if self.reward_list_turns[turn_index][step_index] != -1:
                        end_reward_discounted = self.reward_list_turns[turn_index][step_index]
                else:
                    end_reward_discounted *= 0.9
                
                self.add_reward_list_turns[turn_index][step_index] += end_reward_discounted









