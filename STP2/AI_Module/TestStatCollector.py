class AnomalyTracker():
    def __init__(self, state_space, action_space):
        self.state_space = state_space
        self.action_space = action_space

        self.shortest_games = {}
        self.max_dmg_games = {}
        self.longest_games = {}

        self.shortest_games_high = float('inf')
        self.longest_games_low = 0
        self.max_dmg_low = 0

    def CheckAnomaly(self, states_list, damage_list, game_number, isWin):
        
        for dmg in damage_list:
            if len(self.max_dmg_games) < 5:
                self.max_dmg_games[game_number] = dmg

                self.max_dmg_low = float('inf')
                for key in self.max_dmg_games:
                    if self.max_dmg_low > self.max_dmg_games[key]:
                        self.max_dmg_low = self.max_dmg_games[key]

            else:
                if dmg > self.max_dmg_low:
                    max_dmg_game = 0
                    for key in self.max_dmg_games:
                        if self.max_dmg_low == self.max_dmg_games[key]:
                            max_dmg_game = key
                            break
                    self.max_dmg_games.pop(max_dmg_game)
                    self.max_dmg_games[game_number] = dmg

                    self.max_dmg_low = float('inf')
                    for key in self.max_dmg_games:
                        if self.max_dmg_low > self.max_dmg_games[key]:
                            self.max_dmg_low = self.max_dmg_games[key]

        if not isWin:
            return

        game_len = 0

        for state_list in states_list:
            game_len += len(state_list)

        if len(self.longest_games) < 5:
            self.longest_games[game_number] = game_len
            self.longest_games_low = float('inf')
            for key in self.longest_games:
                if self.longest_games_low > self.longest_games[key]:
                    self.longest_games[key] = self.longest_games[key]
        else:
            if game_len > self.longest_games_low:
                shortest_long_game = 0
                for key in self.longest_games:
                    if self.longest_games[key] == self.longest_games_low:
                        shortest_long_game = key
                        break
                self.longest_games.pop(shortest_long_game)
                self.longest_games[game_number] = game_len
                self.longest_games_low = float('inf')
                for key in self.longest_games:
                    if self.longest_games_low > self.longest_games[key]:
                        self.longest_games[key] = self.longest_games[key]


        if len(self.shortest_games) < 5:
            self.shortest_games[game_number] = game_len
            self.shortest_games_high = 0
            for key in self.shortest_games:
                if self.shortest_games_high < self.shortest_games[key]:
                    self.shortest_games_high = self.shortest_games[key]
        else:
            if game_len < self.shortest_games_high:
                longest_short_game = 0
                for key in self.shortest_games:
                    if self.shortest_games[key] == self.shortest_games_high:
                        longest_short_game = key
                        break
                self.shortest_games.pop(longest_short_game)
                self.shortest_games[game_number] = game_len
                self.shortest_games_high = 0
                for key in self.shortest_games:
                    if self.shortest_games_high < self.shortest_games[key]:
                        self.shortest_games_high = self.shortest_games[key]


    def GenerateGameDictsFromAnomalies(self, all_game_states, all_card_seq):
        self.anomaly_dict = {}

        for shortest_game_number in self.shortest_games:
            game_dur = self.shortest_games[shortest_game_number]
            anom_dict = {}
            anom_dict['game_duration'] = game_dur
            selected_game_state_list = all_game_states[shortest_game_number]
            selected_card_seq = all_card_seq[shortest_game_number]
            anom_dict['game_states'] = self.GetGameDictFromGameNumber(shortest_game_number, selected_game_state_list, selected_card_seq)
            self.anomaly_dict['ShortestWonGame-' + str(shortest_game_number)] = anom_dict.copy()
        
        for longest_game_number in self.longest_games:
            game_dur = self.longest_games[longest_game_number]
            anom_dict = {}
            anom_dict['game_duration'] = game_dur
            selected_game_state_list = all_game_states[longest_game_number]
            selected_card_seq = all_card_seq[longest_game_number]
            anom_dict['game_states'] = self.GetGameDictFromGameNumber(longest_game_number, selected_game_state_list, selected_card_seq)
            self.anomaly_dict['LongestWonGame-' + str(longest_game_number)] = anom_dict.copy()
        
        for maxdmg_game_number in self.max_dmg_games:
            max_dmg = self.max_dmg_games[maxdmg_game_number]
            anom_dict = {}
            anom_dict['max_damage'] = max_dmg
            selected_game_state_list = all_game_states[maxdmg_game_number]
            selected_card_seq = all_card_seq[maxdmg_game_number]
            anom_dict['game_states'] = self.GetGameDictFromGameNumber(maxdmg_game_number, selected_game_state_list, selected_card_seq)
            self.anomaly_dict['MaxDmgTurnGame-' + str(maxdmg_game_number)] = anom_dict.copy()


    def GetGameDictFromGameNumber(self, game_number, selected_game_state_list, selected_card_seq):
        game_dict = {}

        for turn_idx in range(len(selected_game_state_list)):
            states_in_turn = selected_game_state_list[turn_idx]
            actions_in_turn = selected_card_seq[turn_idx]
            turn_dict = {}

            for state_idx in range(len(states_in_turn)):
                state = states_in_turn[state_idx]

                if state_idx >= len(actions_in_turn):
                    action = "End Turn"
                else:
                    action = actions_in_turn[state_idx]

                state_dict = self.GetGameStateInfoFromAIState(state, action)
                turn_dict['Step-' + str(state_idx)] = state_dict

            game_dict['Turn-' + str(turn_idx)] = turn_dict
        
        return game_dict


    def GetGameStateInfoFromAIState(self, game_state, game_action):
        state_dict = {}
        #prepare the return dict
        state_dict['player_energy'] = game_state[self.state_space['player_energy']]
        state_dict['player_health'] = game_state[self.state_space['player_health']]
        state_dict['player_block'] = game_state[self.state_space['player_block']]
        
        state_dict['boss_health'] = game_state[self.state_space['boss_health']]
        state_dict['boss_block'] = game_state[self.state_space['boss_block']]
        
        boss_buffs_list = []
        player_buffs_list = []
        boss_intent = ''
        available_cards = []


        for state_space_key in self.state_space.keys():

            if 'boss_buff-' in state_space_key:
                if game_state[self.state_space[state_space_key]] > 0:
                    boss_buffs_list.append(state_space_key.replace('boss_buff-', ''))

            if 'player_buff-' in state_space_key:
                if game_state[self.state_space[state_space_key]] > 0:
                    player_buffs_list.append(state_space_key.replace('player_buff-', ''))
            
            if 'boss_intent-' in state_space_key:
                if game_state[self.state_space[state_space_key]] > 0:
                    boss_intent = state_space_key.replace('boss_intent-', '')

            if 'in_hand_card-' in state_space_key:
                if game_state[self.state_space[state_space_key]] > 0:
                    available_cards.append(state_space_key.replace('in_hand_card-', ''))


        state_dict['boss_buffs'] = boss_buffs_list
        state_dict['player_buffs'] = player_buffs_list
        state_dict['boss_intent'] = boss_intent
        state_dict['available_cards'] = available_cards

        if game_action == "End Turn":
            state_dict['card_played'] = game_action
        else:
            state_dict['card_played'] = self.action_space[game_action]

        return state_dict



class CardRelationshipTrackers():
    def __init__(self, action_space):
        self.action_space = action_space

        self.empty_card_data_dict = {}
        for card_index in self.action_space:
            self.empty_card_data_dict[self.action_space[card_index]] = 0

        self.card_pair_counter = self.empty_card_data_dict.copy() # card pair counter must 2 dimensional because it represents relationship between 2 cards
        for card in self.card_pair_counter:
            self.card_pair_counter[card] = self.empty_card_data_dict.copy()
        
        self.card_trio_counter = {} #counts how many times sequence of 3 cards was played
        self.card_quadro_counter = {} #counts how many times sequence of 4 cards was played


    
    def CountCardRelationships(self, card_seq_lists):
        
        for card_seq in card_seq_lists:
            for idx in range(len(card_seq)):
                if idx+1 < len(card_seq):
                    self.card_pair_counter[self.action_space[card_seq[idx]]][self.action_space[card_seq[idx+1]]] += 1
            
                if idx+2 < len(card_seq):
                    #create key
                    key = self.action_space[card_seq[idx]] + "-" + self.action_space[card_seq[idx+1]] + "-" + self.action_space[card_seq[idx+2]]

                    if key not in self.card_trio_counter:
                        self.card_trio_counter[key] = 0
                    else:
                        self.card_trio_counter[key] += 1
        
                if idx+3 < len(card_seq):
                    #create key
                    key = self.action_space[card_seq[idx]] + "-" + self.action_space[card_seq[idx+1]] + "-" + self.action_space[card_seq[idx+2]] + "-" + self.action_space[card_seq[idx+3]]

                    if key not in self.card_quadro_counter:
                        self.card_quadro_counter[key] = 0
                    else:
                        self.card_quadro_counter[key] += 1

