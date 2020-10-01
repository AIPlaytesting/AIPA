import game_manager
import json



#Purpose of this class is to take information about the game state and create a gym like interface for the AI to train with.

class AI_Transformer:

    def __init__(self):
        self.ReadStateActionDefFromFile("1.0")
        self.CreateEmptyStateActionDicts()
        pass

    def GetAIStateSpace(self, game_state, playable_cards):
        self.CreateEmptyStateActionDicts()
        self.MapGameStateToStateDicts(game_state, playable_cards)
        flat_state_space = self.GetFlatStateList()
        
        return flat_state_space

    def GetGameAction(self, action_neuron_number):
        action_card = self.action_space[str(action_neuron_number)]
        return action_card


    def ReadStateActionDefFromFile(self, version_string):
        with open("AI_Module/StateActionDef/state_action_def_" + version_string + ".json", "r") as file:
            raw_json_data = file.read()
            self.sa_json_data = json.loads(raw_json_data)
            
    def CreateEmptyStateActionDicts(self, version_string = None):
        self.player_basic = self.sa_json_data['state_dict']['player_basic']
        self.player_buffs = self.sa_json_data['state_dict']['player_buffs']
        self.boss_basic = self.sa_json_data['state_dict']['boss_basic']
        self.boss_buffs = self.sa_json_data['state_dict']['boss_buffs']
        self.boss_intent = self.sa_json_data['state_dict']['boss_intent']
        self.in_hand_cards = self.sa_json_data['state_dict']['in_hand_cards']
        self.in_hand_and_playable_cards = self.sa_json_data['state_dict']['in_hand_and_playable_cards']
        self.draw_pile = self.sa_json_data['state_dict']['draw_pile']
        self.discard_pile = self.sa_json_data['state_dict']['discard_pile']
        self.action_space = self.sa_json_data['action_space']


    def MapGameStateToStateDicts(self, game_state, playable_cards):
        
        self.player_basic['energy'] = game_state.player_energy
        self.player_basic['health'] = game_state.player.current_hp
        self.player_basic['block'] = game_state.player.block

        for key in self.player_buffs:
            self.player_buffs[key] = game_state.player.buff_dict[key]

        self.boss_basic['health'] = game_state.boss.current_hp
        self.boss_basic['block'] = game_state.boss.block

        for key in self.boss_buffs:
            self.boss_buffs[key] = game_state.boss.buff_dict[key]

        #TODO boss intent

        for key in self.in_hand_cards:
            cards_on_hand = game_state.deck.get_card_names_on_hand()
            self.in_hand_cards[key] = cards_on_hand.count(key)
            self.in_hand_and_playable_cards[key] = playable_cards.count(key)
            draw_pile = game_state.deck.get_card_names_in_draw_pile()
            discard_pile = game_state.deck.get_card_names_in_discard_pile()
            self.draw_pile[key] = draw_pile.count(key)
            self.discard_pile[key] = discard_pile.count(key)

        self.CreateEnemyIntentList(game_state)


    def GetFlatStateList(self):
        flat_list = []

        for key in self.player_basic : 
            flat_list.append(self.player_basic[key])

        for key in self.player_buffs : 
            flat_list.append(self.player_buffs[key])

        for key in self.boss_basic :
            flat_list.append(self.boss_basic[key])

        for key in self.boss_buffs :
            flat_list.append(self.boss_buffs[key])
        
        for key in self.in_hand_cards :
            flat_list.append(self.in_hand_cards[key])
        
        for key in self.in_hand_and_playable_cards :
            flat_list.append(self.in_hand_and_playable_cards[key])

        for key in self.draw_pile :
            flat_list.append(self.draw_pile[key])
        
        for key in self.discard_pile :
            flat_list.append(self.discard_pile[key])
        
        for i in range(len(self.intent_nums)):
            flat_list.append(self.intent_nums[i])

        return flat_list


    def CreateEnemyIntentList(self, game_state):
        current_intent = game_state.boss_intent.name

        intent_name_list = ['Charging Up', 'Fierce Bash', 'Vent Steam', 'Whirlwind' ,'Defensive Mode', 'Roll Attack', 'Twin slam']

        self.intent_nums = []

        for i in range(len(intent_name_list)):
            if intent_name_list[i] == current_intent:
                self.intent_nums.append(1)
            else:
                self.intent_nums.append(0)






