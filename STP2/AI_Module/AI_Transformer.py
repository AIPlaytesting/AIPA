import gameplay.game_manager
import json
import db.game_database

#Purpose of this class is to take information about the game state and create a gym like interface for the AI to train with.

class AI_Transformer:

    def __init__(self):
        self.ReadStateActionDefFromFile("v1")
        self.ReadSelectorFromFile("v1")
        
        self.state_space_dim = 0
        self.state_space_strings = []
        self.state_space = {} #key : string name, value : index
        self.action_space_dim = 0
        self.action_space = {} #key : index, valuee : name

        db_root = db.game_database.calculate_root_dir()
        game_db = db.game_database.GameDatabase(db_root)
        self.deck_config = game_db.game_app_data.deck_config.copy()
        registered_buffnames = game_db.game_app_data.registered_buffnames.copy()
        self.empty_buff_dict = {}
        for buff_name in registered_buffnames:
            self.empty_buff_dict[buff_name] = 0
        
        self.CreateEmptyStateDicts()
        self.InitializeActionSpace()
        self.GetStateSpaceStringList()


    def GetAIStateSpace(self, game_state, playable_cards):
        self.CreateEmptyStateDicts()
        self.MapGameStateToStateDicts(game_state, playable_cards)
        flat_state_space = self.GetFlatStateList()
        
        return flat_state_space


    def GetGameAction(self, action_neuron_number):
        action_card = self.action_space[action_neuron_number]
        return action_card


    def InitializeActionSpace(self):
        itr = 0
        for key in self.deck_config:
            if self.deck_config[key] > 0:
                self.action_space[itr] = key
                itr += 1
        self.action_space_dim = len(self.action_space)
        


    def ReadStateActionDefFromFile(self, version_string):
        with open("AI_Module/StateActionDef/state_action_def_" + version_string + ".json", "r") as file:
            raw_json_data = file.read()
            self.sa_json_data = json.loads(raw_json_data)


    def ReadSelectorFromFile(self, version_string):
        with open("AI_Module/StateActionDef/state_space_selector_" + version_string + ".json", "r") as file:
            raw_json_data = file.read()
            selection_data = json.loads(raw_json_data)
            self.selector = selection_data['selectors']
            self.player_buffs_minimal = selection_data['player_minimal_buffs']
            self.boss_buffs_minimal = selection_data['boss_minimal_buffs']


    def CreateEmptyStateDicts(self, version_string = None):
        self.player_basic = self.sa_json_data['state_dict']['player_basic']
        self.boss_basic = self.sa_json_data['state_dict']['boss_basic']
        
        self.boss_intent = self.sa_json_data['state_dict']['boss_intent']

        self.player_buffs = self.empty_buff_dict.copy()
        self.boss_buffs = self.empty_buff_dict.copy()

        self.in_hand_cards = self.deck_config.copy()
        self.in_hand_and_playable_cards = self.deck_config.copy()
        self.draw_pile = self.deck_config.copy()
        self.discard_pile = self.deck_config.copy()


    def MapGameStateToStateDicts(self, game_state, playable_cards):
        
        self.player_basic['energy'] = game_state.player_energy
        self.player_basic['health'] = game_state.player.current_hp
        self.player_basic['block'] = game_state.player.block

        for key in self.player_buffs:
            #one hot encoding of player buffs
            self.player_buffs[key] = 1 if game_state.player.buff_dict[key] > 0 else 0

        self.boss_basic['health'] = game_state.boss.current_hp
        self.boss_basic['block'] = game_state.boss.block
        self.boss_basic['boss_phase_switch_damage'] = game_state.boss_AI.transformTriggerPoint - game_state.boss_AI.accumulator

        for key in self.boss_buffs:
            self.boss_buffs[key] = game_state.boss.buff_dict[key]

        for key in self.in_hand_cards:
            cards_on_hand = game_state.deck.get_card_names_on_hand()
            self.in_hand_cards[key] = cards_on_hand.count(key)
            self.in_hand_and_playable_cards[key] = playable_cards.count(key)
            draw_pile = game_state.deck.get_card_names_in_draw_pile()
            self.draw_pile[key] = draw_pile.count(key)
            discard_pile = game_state.deck.get_card_names_in_discard_pile()
            self.discard_pile[key] = discard_pile.count(key)

        current_intent = game_state.boss_intent.name
        for key in self.boss_intent:
            self.boss_intent[key] = 1 if key == current_intent else 0


    def GetFlatStateList(self):
        flat_list = []

        #Basics
        if self.selector['player_energy']:
            flat_list.append(self.player_basic['energy'])
        
        if self.selector['player_health']:
            flat_list.append(self.player_basic['health'])

        if self.selector['player_block']:
            flat_list.append(self.player_basic['block'])
        
        if self.selector['boss_health']:
            flat_list.append(self.boss_basic['health'])
        
        if self.selector['boss_block']:
            flat_list.append(self.boss_basic['block'])
        
        if self.selector['boss_phase_switch_damage']:
            flat_list.append(self.boss_basic['boss_phase_switch_damage'])

        
        #Player Buffs
        if self.selector['player_buffs']:
            if self.selector['player_buff_minimal']:
                for buff_name in self.player_buffs_minimal:
                    flat_list.append(self.player_buffs[buff_name])
            else:
                #include all buffs if buff minimal is false
                for key in self.player_buffs : 
                    flat_list.append(self.player_buffs[key])


        #Boss Buffs
        if self.selector['boss_buffs']:
            if self.selector['boss_buff_minimal']:
                for buff_name in self.boss_buffs_minimal:
                    flat_list.append(self.boss_buffs[buff_name])
            else:
                #include all buffs if buff minimal is false
                for key in self.boss_buffs : 
                    flat_list.append(self.boss_buffs[key])

        
        #Cards
        if self.selector['in_hand_cards']:
            for key in self.in_hand_cards :
                flat_list.append(self.in_hand_cards[key])
        
        if self.selector['in_hand_playable_cards']:
            for key in self.in_hand_and_playable_cards :
                flat_list.append(self.in_hand_and_playable_cards[key])

        if self.selector['draw_pile']:
            for key in self.draw_pile :
                flat_list.append(self.draw_pile[key])
        
        if self.selector['discard_pile']:
            for key in self.discard_pile :
                flat_list.append(self.discard_pile[key])

        if self.selector['boss_intent']:
            for key in self.boss_intent:
                flat_list.append(self.boss_intent[key])

        return flat_list


    def GetStateSpaceStringList(self):
        state_space_index = 0

        #Basics
        if self.selector['player_energy']:
            self.state_space['player_energy'] = state_space_index
            state_space_index += 1
        
        if self.selector['player_health']:
            self.state_space['player_health'] = state_space_index
            state_space_index += 1

        if self.selector['player_block']:
            self.state_space['player_block'] = state_space_index
            state_space_index += 1
        
        if self.selector['boss_health']:
            self.state_space['boss_health'] = state_space_index
            state_space_index += 1
        
        if self.selector['boss_block']:
            self.state_space['boss_block'] = state_space_index
            state_space_index += 1
        
        if self.selector['boss_phase_switch_damage']:
            self.state_space['boss_phase_switch_damage'] = state_space_index
            state_space_index += 1

        
        #Player Buffs
        if self.selector['player_buffs']:
            if self.selector['player_buff_minimal']:
                for buff_name in self.player_buffs_minimal:
                    self.state_space["player_buff-" + buff_name] = state_space_index
                    state_space_index += 1
            else:
                #include all buffs if buff minimal is false
                for key in self.player_buffs : 
                    self.state_space["player_buff-" + key] = state_space_index
                    state_space_index += 1


        #Boss Buffs
        if self.selector['boss_buffs']:
            if self.selector['boss_buff_minimal']:
                for buff_name in self.boss_buffs_minimal:
                    self.state_space["boss_buff-" + buff_name] = state_space_index
                    state_space_index += 1
            else:
                #include all buffs if buff minimal is false
                for key in self.boss_buffs : 
                    self.state_space["boss_buff-" + key] = state_space_index
                    state_space_index += 1
        
        #Cards
        if self.selector['in_hand_cards']:
            for key in self.in_hand_cards :
                self.state_space["in_hand_card-" + key] = state_space_index
                state_space_index += 1
        
        if self.selector['in_hand_playable_cards']:
            for key in self.in_hand_and_playable_cards :
                self.state_space["in_hand_playable_card-" + key] = state_space_index
                state_space_index += 1

        if self.selector['draw_pile']:
            for key in self.draw_pile :
                self.state_space["draw_pile-" + key] = state_space_index
                state_space_index += 1
        
        if self.selector['discard_pile']:
            for key in self.discard_pile :
                self.state_space["discard_pile-" + key] = state_space_index
                state_space_index += 1

        if self.selector['boss_intent']:
            for key in self.boss_intent:
                self.state_space["boss_intent-" + key] = state_space_index
                state_space_index += 1

        self.state_space_dim = state_space_index


    def PrintStateActionDef(self):
        print("Detailed State Space : ")
        for key in self.state_space:
            print(str(self.state_space[key])+ " - " + key)
        print("State Space Length = " + str(self.state_space_dim))
        print("Detailed Action Space : ")
        print(self.action_space)
        print("Action Space Length = " + str(self.action_space_dim)) 






