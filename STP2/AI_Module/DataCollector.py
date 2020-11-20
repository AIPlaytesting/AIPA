import AI_Module.TestStatCollector

class DataCollector:

    def __init__(self, state_space, action_space, isTrain):
        
        self.state_space = state_space #key : string name, value : index
        self.action_space = action_space #key : index, value : string name
        self.isTrain = isTrain

        self.anomaly_tracker = AI_Module.TestStatCollector.AnomalyTracker(self.state_space, self.action_space)
        self.card_rel_tracker = AI_Module.TestStatCollector.CardRelationshipTrackers(self.action_space)

        #to keep track of win rate
        self.win_data_list = [] # (-1 : loss by boss damage), (-2 : loss by wrong card), (1 : win)
        self.episode_index_list = []
        self.player_end_hp_list = []
        self.boss_end_hp_list = []
        self.total_reward_list = []
        self.episode_length_list = []
        self.epsilon_list = []
        self.max_damage = []
        self.average_damage = []
        self.roll_avg_reward = []
        self.q_model_switch_episode_index = []

        self.game_play_time = []
        self.prediction_time = []
        self.total_game_play_time = []
        self.train_time = []

        self.cur_available_card_turns = []
        self.cur_played_card_turns = []
        self.cur_damage_done_in_turns = []
        self.cur_card_play_sequence_turns = []
        self.cur_reward_list = []
        self.cur_state_list = []

        self.all_damage_per_turn = []
        self.all_card_seq = []
        self.all_reward_per_turn = []
        self.all_game_states = []

        self.empty_card_data_dict = {}
        for card_index in self.action_space:
            self.empty_card_data_dict[self.action_space[card_index]] = 0

        self.card_count_in_deck = self.empty_card_data_dict.copy()
        self.card_play_count = self.empty_card_data_dict.copy()
        self.available_cards = self.empty_card_data_dict.copy()
        self.average_card_play_pos = self.empty_card_data_dict.copy()
        self.card_played_when_available = self.empty_card_data_dict.copy()
        self.card_average_reward = self.empty_card_data_dict.copy()

    def StoreGameData(self, epsilon, win_int, player_end_hp, boss_end_hp, total_reward, episode_length):
        self.episode_index_list.append(len(self.episode_index_list))
        self.win_data_list.append(win_int)
        self.player_end_hp_list.append(player_end_hp)
        self.boss_end_hp_list.append(boss_end_hp)
        self.total_reward_list.append(total_reward)
        self.episode_length_list.append(episode_length)
        self.epsilon_list.append(epsilon)

    def StoreTimeInformation(self, prediction_time, game_play_time, training_time):
        self.prediction_time.append(prediction_time)
        self.game_play_time.append(game_play_time)
        self.train_time.append(training_time)
        self.total_game_play_time.append(game_play_time + prediction_time)

    def PostDataCollectionAnalysis(self):
        self.average_card_play_pos = self.empty_card_data_dict.copy()
        self.card_average_reward = self.empty_card_data_dict.copy()
        self.UpdateRollingReward()

        #average damage and max damage
        for damage_done_per_turn in self.all_damage_per_turn:
            self.max_damage.append(max(damage_done_per_turn))
            self.average_damage.append(sum(damage_done_per_turn) / len(damage_done_per_turn))

        #win int interpretation
        for win_index in range(len(self.win_data_list)):
            if self.win_data_list[win_index] == 1:
                self.win_data_list[win_index] = 'Win'
            elif self.win_data_list[win_index] == -1:
                self.win_data_list[win_index] = 'Loss by Boss Damage'
            elif self.win_data_list[win_index] == -2:
                self.win_data_list[win_index] = 'Loss by Wrong Card'

        #card count in deck
        for card_index in self.action_space:
            card_name = self.action_space[card_index]
            self.card_count_in_deck[card_name] = self.deck_config[card_name]

        #average card play position
        for game_index in range(len(self.all_card_seq)):
            for turn_index in range(len(self.all_card_seq[game_index])):
                action_turn_list = self.all_card_seq[game_index][turn_index]
                reward_turn_list = self.all_reward_per_turn[game_index][turn_index]
                for index in range(len(action_turn_list)):
                    card_name = self.action_space[action_turn_list[index]]
                    #card position is the same as the index of the card in the turn list (index + 1 because index starts with 0 but card is playes as FIRST card of turn)
                    self.average_card_play_pos[card_name] += index + 1
                    #reward taken from the reward list
                    self.card_average_reward[card_name] += reward_turn_list[index]
        
        #to average, divide the sum of all card play pos (and reward) by the total times card was played
        for card_name in self.average_card_play_pos:
            if self.card_play_count[card_name] != 0:
                self.average_card_play_pos[card_name] /= self.card_play_count[card_name]
                self.card_average_reward[card_name] /= self.card_play_count[card_name]

        #card played when available percentage
        for card_name in self.card_played_when_available:
            if not self.available_cards[card_name] == 0:
                self.card_played_when_available[card_name] = self.card_play_count[card_name] / self.available_cards[card_name]
        
        if not self.isTrain:
            self.anomaly_tracker.GenerateGameDictsFromAnomalies(self.all_game_states, self.all_card_seq)
            self.anomaly_dict = self.anomaly_tracker.anomaly_dict

    def UpdateRollingReward(self):
        if(len(self.total_reward_list) < 100):
            return 

        # fill the index gap
        for gap in range(len(self.roll_avg_reward),len(self.total_reward_list)):
            self.roll_avg_reward.append(0)
        # update the latest value (in case when iteartion very high, update 10k+ very iteartion has high overhead)
        update_start_index = max(len(self.total_reward_list)-100,0)
        for r_index in range(update_start_index,len(self.total_reward_list)):
            end_index = r_index + 50
            start_index = r_index
            if end_index > len(self.total_reward_list) - 1: 
                end_index = len(self.total_reward_list) - 1
                start_index = start_index - 50

                if start_index < 0:
                    start_index = 0

            else:
                start_index = r_index

            self.roll_avg_reward[r_index] = sum(self.total_reward_list[start_index:end_index]) / len(self.total_reward_list[start_index:end_index])

    def StoreDeckConfig(self, deck_config):
        self.deck_config = deck_config


    def CollectDataFromTurn(self, state_list, new_state_list, action_list, reward_list):
        #available cards
        playable_card_indices = {}
        available_cards = self.empty_card_data_dict.copy()

        for index in self.action_space:
            if ('in_hand_card-' + self.action_space[index]) in self.state_space:
                playable_card_indices[self.action_space[index]] = self.state_space['in_hand_card-' + self.action_space[index]]

        for step_index in range(len(state_list)):
            for action_card in playable_card_indices:
                action_card_count = state_list[step_index][playable_card_indices[action_card]]
                if action_card_count > 0:
                    #the available card count should be equal to the max count of the card in all states in the state list
                    available_cards[action_card] = action_card_count if action_card_count > available_cards[action_card] else available_cards[action_card]

        #add the available cards data directly to the class variable
        for card_name in available_cards:
            self.available_cards[card_name] += available_cards[card_name]

        #played cards
        card_played_sequence = []
        
        for step_index in range(len(action_list)):
            action_number = action_list[step_index]
            if action_number != -1: # -1 action is for end turn
                card_played_sequence.append(action_number)
                played_card = self.action_space[action_number]
                self.card_play_count[played_card] += 1
        
        #reward sequence
        rewards_in_turn = []
        for step_index in range(len(reward_list)):
            rewards_in_turn.append(reward_list[step_index])

        damage_done_in_turn = 0

        boss_hp_index = self.state_space['boss_health']

        turn_start_boss_hp = state_list[0][boss_hp_index]
        turn_end_boss_hp = state_list[len(state_list)-1][boss_hp_index]

        damage_done_in_turn = (turn_start_boss_hp - turn_end_boss_hp) if (turn_start_boss_hp - turn_end_boss_hp) > 0 else 0

        self.StoreTurnData(state_list, card_played_sequence, rewards_in_turn, damage_done_in_turn)


    def StoreTurnData(self, state_list, card_played_sequence, rewards_in_turn, damage_done_in_turn):
        self.cur_card_play_sequence_turns.append(card_played_sequence)
        self.cur_damage_done_in_turns.append(damage_done_in_turn)
        self.cur_reward_list.append(rewards_in_turn)
        self.cur_state_list.append(state_list)



    def AddCurrentTurnDataToGameLists(self, isWin):
        self.all_card_seq.append(self.cur_card_play_sequence_turns)
        self.all_damage_per_turn.append(self.cur_damage_done_in_turns)
        self.all_reward_per_turn.append(self.cur_reward_list)

        if not self.isTrain:
            self.all_game_states.append(self.cur_state_list)
            self.anomaly_tracker.CheckAnomaly(self.cur_state_list, self.cur_damage_done_in_turns, game_number=len(self.all_game_states)-1, isWin=isWin)
            self.card_rel_tracker.CountCardRelationships(self.cur_card_play_sequence_turns)

        self.cur_card_play_sequence_turns = []
        self.cur_damage_done_in_turns = []
        self.cur_reward_list = []
        self.cur_state_list = []


    def RecordQModelSwitch(self):
        self.q_model_switch_episode_index.append(len(self.episode_index_list) - 1)

    





