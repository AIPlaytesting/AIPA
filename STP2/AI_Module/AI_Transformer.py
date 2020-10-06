import game_manager
import json
import db.game_database

#Purpose of this class is to take information about the game state and create a gym like interface for the AI to train with.

class AI_Transformer:

    def __init__(self):
        self.ReadStateActionDefFromFile("v1")
        self.ReadSelectorFromFile("v1")
        
        self.state_space_dim = 0
        self.state_space_strings = []
        self.action_space_dim = 0

        db_root = db.game_database.calculate_root_dir()
        game_db = db.game_database.GameDatabase(db_root)
        self.deck_config = game_db.game_app_data.deck_config.copy()
        print(self.deck_config)
        
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
        self.action_space = {}
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
            self.selector = json.loads(raw_json_data)


    def CreateEmptyStateDicts(self, version_string = None):
        self.player_basic = self.sa_json_data['state_dict']['player_basic']
        self.player_buffs = self.sa_json_data['state_dict']['player_buffs']
        self.boss_basic = self.sa_json_data['state_dict']['boss_basic']
        self.boss_buffs = self.sa_json_data['state_dict']['boss_buffs']
        self.boss_intent = self.sa_json_data['state_dict']['boss_intent']

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

        for key in self.boss_buffs:
            self.boss_buffs[key] = game_state.boss.buff_dict[key]

        for key in self.in_hand_cards:
            cards_on_hand = game_state.deck.get_card_names_on_hand()
            self.in_hand_cards[key] = cards_on_hand.count(key)
            self.in_hand_and_playable_cards[key] = playable_cards.count(key)
            draw_pile = game_state.deck.get_card_names_in_draw_pile()
            discard_pile = game_state.deck.get_card_names_in_discard_pile()
            self.draw_pile[key] = draw_pile.count(key)
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

        
        #Player Buffs
        if self.selector['player_buffs']:
            if self.selector['buff_minimal']:
                flat_list.append(self.player_buffs['Weakened'])
                flat_list.append(self.player_buffs['Vulnerable'])
                flat_list.append(self.player_buffs['Strength'])
                flat_list.append(self.player_buffs['Flex'])
                #TODO flat_list.append(self.player_buffs['DoubleTapActive'])
            else:
                #include all buffs if buff minimal is false
                for key in self.player_buffs : 
                    flat_list.append(self.player_buffs[key])


        #Boss Buffs
        if self.selector['boss_buffs']:
            if self.selector['buff_minimal']:
                flat_list.append(self.boss_buffs['Weakened'])
                flat_list.append(self.boss_buffs['Vulnerable'])
                flat_list.append(self.boss_buffs['Strength'])
                flat_list.append(self.boss_buffs['Thorns'])
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
        self.state_space_strings = []

        #Basics
        if self.selector['player_energy']:
            self.state_space_strings.append(str(len(self.state_space_strings) + 1) + " Player energy")
        
        if self.selector['player_health']:
            self.state_space_strings.append(str(len(self.state_space_strings) + 1) + " Player health")

        if self.selector['player_block']:
            self.state_space_strings.append(str(len(self.state_space_strings) + 1) + " Player block")
        
        if self.selector['boss_health']:
            self.state_space_strings.append(str(len(self.state_space_strings) + 1) + " Boss health")
        
        if self.selector['boss_block']:
            self.state_space_strings.append(str(len(self.state_space_strings) + 1) + " Boss block")

        
        #Player Buffs
        if self.selector['player_buffs']:
            if self.selector['buff_minimal']:
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Player buff - Weakened')
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Player buff - Vulnerable')
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Player buff - Strength')
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Player buff - Flex')
                #TODO self.state_space_strings.append(self.player_buffs['DoubleTapActive'])
            else:
                #include all buffs if buff minimal is false
                for key in self.player_buffs : 
                    self.state_space_strings.append(str(len(self.state_space_strings) + 1)+ ' Player buff - ' + key)


        #Boss Buffs
        if self.selector['boss_buffs']:
            if self.selector['buff_minimal']:
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Boss buff - Weakened')
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Boss buff - Vulnerable')
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Boss buff - Strength')
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Boss buff - Thorns')
            else:
                #include all buffs if buff minimal is false
                for key in self.boss_buffs : 
                    self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Boss buff - ' + key)
        
        #Cards
        if self.selector['in_hand_cards']:
            for key in self.in_hand_cards :
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' In hand card - ' + key)
        
        if self.selector['in_hand_playable_cards']:
            for key in self.in_hand_and_playable_cards :
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' In hand and playable card - ' + key)

        if self.selector['draw_pile']:
            for key in self.draw_pile :
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Draw Pile - ' + key)
        
        if self.selector['discard_pile']:
            for key in self.discard_pile :
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Discard Pile - ' + key)

        if self.selector['boss_intent']:
            for key in self.boss_intent:
                self.state_space_strings.append(str(len(self.state_space_strings) + 1) + ' Boss Intent - ' + key)

        self.state_space_dim = len(self.state_space_strings)


    def PrintStateActionDef(self):
        print("Detailed State Space : ")
        for state_space_string in self.state_space_strings:
            print(state_space_string)
        print("State Space Length = " + str(self.state_space_dim))
        print("Detailed Action Space : ")
        print(self.action_space)
        print("Action Space Length = " + str(self.action_space_dim)) 






