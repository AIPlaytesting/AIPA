import AI_Module.RewardFunctions
import AI_Module.TrainingDataCollector

class GameBuffer:
    
    def __init__(self, state_space, action_space):
        
        self.state_space = state_space #key : string name, value : index
        self.action_space = action_space #key : index, value : name
        self.reward_functions = AI_Module.RewardFunctions.RewardFunctions(self.state_space, self.action_space)
        self.data_collector = AI_Module.TrainingDataCollector.TrainingDataCollector(self.state_space, self.action_space)

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

        self.q_model_switch_count = 0


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


    def TransferToReplayBuffer(self, ai_agent, win_int):

        store_count = 5 if win_int == 1 else 1

        for turn_index in range(len(self.reward_list_turns)):
            for step_index in range(len(self.reward_list_turns[turn_index])):
                self.reward_list_turns[turn_index][step_index] += self.add_reward_list_turns[turn_index][step_index]

            for state_list, new_state_list, action_list, reward_list, add_reward_list, terminal_list in \
                zip(self.state_list_turns, self.new_state_list_turns, self.action_list_turns, self.reward_list_turns, self.add_reward_list_turns, self.terminal_list_turns):

                self.data_collector.CollectDataFromTurn(state_list, new_state_list, action_list, reward_list)

                for state, new_state, action, reward, add_reward, terminal in zip(state_list, new_state_list, action_list, reward_list, add_reward_list, terminal_list):

                    for x in range(store_count):
                        ai_agent.StoreTransition(state, new_state, action, reward, terminal)
                    
                    ai_agent.Learn()

                    if self.CheckForQModelSwitch(ai_agent):
                        self.data_collector.RecordQModelSwitch()
            
            self.data_collector.AddCurrentTurnDataToGameLists()



    def RewardCalculations(self):
        end_reward_discounted = 0

        self.reward_functions.AssignGameLists(self.state_list_turns, self.new_state_list_turns, self.action_list_turns, \
            self.reward_list_turns, self.add_reward_list_turns, self.terminal_list_turns)

        for turn_index in range(len(self.state_list_turns) - 1, -1, -1):
            for step_index in range(len(self.state_list_turns[turn_index]) - 1, -1, -1):
                self.reward_functions.AddRewardFromDamageBlock(turn_index, step_index)

                action_neuron_number = self.action_list_turns[turn_index][step_index]
                action_card = self.action_space[action_neuron_number]

                reward_clothesline = 0
                reward_disarm = 0
                reward_flex = 0
                reward_doubletap = 0
                reward_bash = 0
                reward_thunderclap = 0
                reward_uppercut = 0

                if action_card == "Clothesline":
                    reward_clothesline = self.reward_functions.RewardFromClothesline(turn_index, step_index, isPlus = False)
                elif action_card == "Clothesline Plus": 
                    reward_clothesline = self.reward_functions.RewardFromClothesline(turn_index, step_index, isPlus = True)
                elif action_card == "Disarm":
                    reward_disarm = self.reward_functions.RewardFromDisarm(turn_index, step_index, isPlus = False)
                elif action_card == "Disarm Plus": 
                    reward_disarm = self.reward_functions.RewardFromDisarm(turn_index, step_index, isPlus = True)
                elif action_card == "Flex":
                    reward_flex = self.reward_functions.RewardFromFlex(turn_index, step_index, isPlus = False)
                elif action_card == "Flex Plus":
                    reward_flex = self.reward_functions.RewardFromFlex(turn_index, step_index, isPlus = True)
                elif action_card == "Double Tap":
                    reward_doubletap = self.reward_functions.RewardFromDoubleTap(turn_index, step_index)
                elif action_card == "Bash":
                    reward_bash = self.reward_functions.RewardFromBash(turn_index, step_index, isPlus = False)
                elif action_card == "Bash Plus":
                    reward_bash = self.reward_functions.RewardFromBash(turn_index, step_index, isPlus = True)
                elif (action_card == "Thunderclap") or (action_card == "Thunderclap Plus"):
                    reward_thunderclap = self.reward_functions.RewardFromThunderclap(turn_index, step_index)
                elif action_card == "Uppercut":
                    reward_uppercut = self.reward_functions.RewardFromUppercut(turn_index, step_index, isPlus = False)
                elif action_card == "Uppercut Plus":
                    reward_uppercut = self.reward_functions.RewardFromUppercut(turn_index, step_index, isPlus = True)

                special_reward_sum = reward_clothesline + reward_disarm + reward_flex + reward_doubletap + \
                                        + reward_bash + reward_thunderclap + reward_uppercut

                self.add_reward_list_turns[turn_index][step_index] += special_reward_sum

        for turn_index in range(len(self.state_list_turns) - 1, -1, -1):
            for step_index in range(len(self.state_list_turns[turn_index]) - 1, -1, -1):
            
                if (turn_index == len(self.state_list_turns) - 1) and (step_index == len(self.state_list_turns[turn_index]) - 1):
                    if self.reward_list_turns[turn_index][step_index] != -1:
                        end_reward_discounted = self.reward_list_turns[turn_index][step_index]
                else:
                    end_reward_discounted *= 0.9
                
                self.add_reward_list_turns[turn_index][step_index] += end_reward_discounted


    def StoreGameData(self, epsilon, win_int, new_state, prediction_time, game_time, train_time):
        #calculate total reward of episode
        total_reward = 0
        episode_length = 0

        for reward_list in self.reward_list_turns:
            for step_reward in reward_list:
                total_reward += step_reward
                episode_length += 1

        boss_hp_index = self.state_space['boss_health']
        boss_end_hp = new_state[boss_hp_index]

        player_hp_index = self.state_space['player_health']
        player_end_hp = new_state[player_hp_index]

        self.data_collector.StoreGameData(epsilon, win_int, player_end_hp, boss_end_hp, total_reward, episode_length)
        self.data_collector.StoreTimeInformation(prediction_time, game_time, train_time)


    def CheckForQModelSwitch(self, ai_agent):
        if not hasattr(ai_agent, 'q_model_switch_count'): 
            return False
        
        if self.q_model_switch_count < ai_agent.q_model_switch_count:
            self.q_model_switch_count = ai_agent.q_model_switch_count
            return True
        else:
            return False






