

class TrainingDataCollector:

    def __init__(self, state_space, action_space):
        
        self.state_space = state_space #key : string name, value : index
        self.action_space = action_space #key : index, value : string name

        #to keep track of win rate
        self.win_data_list = [] # (-1 : loss by boss damage), (-2 : loss by wrong card), (1 : win)
        self.player_end_hp_list = []
        self.boss_end_hp_list = []
        self.total_reward_list = []
        self.episode_length_list = []
        self.epsilon_list = []

        self.cur_available_card_turns = []
        self.cur_played_card_turns = []
        self.cur_damage_done_in_turns = []
        self.cur_card_play_sequence_turns = []
        self.cur_reward_list = []

        self.available_cards = []
        self.played_cards = []
        self.damage_done_per_turn = []
        self.card_play_sequence_per_turn = []
        self.reward_list_per_turn = []

    def StoreGameData(self, epsilon, win_int, player_end_hp, boss_end_hp, total_reward, episode_length):
        self.win_data_list.append(win_int)
        self.player_end_hp_list.append(player_end_hp)
        self.boss_end_hp_list.append(boss_end_hp)
        self.total_reward_list.append(total_reward)
        self.episode_length_list.append(episode_length)
        self.epsilon_list.append(epsilon)



    def CollectDataFromTurn(self, state_list, new_state_list, action_list, reward_list):

        #available cards
        available_cards = {}
        playable_card_indices = {}

        for index in self.action_space:
            if ('in_hand_card-' + self.action_space[index]) in self.state_space:
                playable_card_indices[self.action_space[index]] = self.state_space['in_hand_card-' + self.action_space[index]]

        for step_index in range(len(state_list)):
            for action_card in playable_card_indices:
                action_card_count = state_list[step_index][playable_card_indices[action_card]]
                if action_card_count > 0:
                    if action_card not in available_cards:
                        available_cards[action_card] = action_card_count
                    available_cards[action_card] = action_card_count if available_cards[action_card] < action_card_count else available_cards[action_card]

        #played cards
        played_cards = {}
        card_played_sequence = []
        
        for step_index in range(len(action_list)):
            action_number = action_list[step_index]
            card_played_sequence.append(action_number)
            played_card = self.action_space[action_number]
            played_cards[played_card] = 1 if played_card not in played_cards else played_cards[played_card] + 1
        
        #reward sequence
        rewards_in_turn = []
        for step_index in range(len(reward_list)):
            rewards_in_turn.append(reward_list[step_index])


        damage_done_in_turn = 0

        boss_hp_index = self.state_space['boss_health']

        turn_start_boss_hp = state_list[0][boss_hp_index]
        turn_end_boss_hp = state_list[len(state_list)-1][boss_hp_index]

        damage_done_in_turn = (turn_start_boss_hp - turn_end_boss_hp) if (turn_start_boss_hp - turn_end_boss_hp) > 0 else 0

        self.StoreTurnData(available_cards, played_cards, card_played_sequence, rewards_in_turn, damage_done_in_turn)


    def StoreTurnData(self, available_cards, played_cards, card_played_sequence, rewards_in_turn, damage_done_in_turn):
        self.cur_available_card_turns.append(available_cards)
        self.cur_played_card_turns.append(played_cards)
        self.cur_card_play_sequence_turns.append(card_played_sequence)
        self.cur_damage_done_in_turns.append(damage_done_in_turn)
        self.cur_reward_list.append(rewards_in_turn)


    def AddCurrentTurnDataToGameLists(self):
        self.available_cards.append(self.cur_available_card_turns)
        self.cur_available_card_turns = []

        self.played_cards.append(self.cur_played_card_turns)
        self.cur_played_card_turns = []

        self.card_play_sequence_per_turn.append(self.cur_card_play_sequence_turns)
        self.cur_card_play_sequence_turns = []

        self.damage_done_per_turn.append(self.cur_damage_done_in_turns)
        self.cur_damage_done_in_turns = []

        self.reward_list_per_turn.append(self.cur_reward_list)
        self.cur_reward_list = []













