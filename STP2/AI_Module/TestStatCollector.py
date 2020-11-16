class AnomalyTracker():
    def __init__(self):
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
                    key = card_seq[idx] + "-" + card_seq[idx+1] + "-" + card_seq[idx+2] + "-" + card_seq[idx+3]

                    if key not in self.card_quadro_counter:
                        self.card_quadro_counter[key] = 0
                    else:
                        self.card_quadro_counter[key] += 1

