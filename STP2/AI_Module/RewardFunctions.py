
# USES CARD NAMES TO REFERENCE CARDS
class RewardFunctions:

    def __init__(self, state_space, action_space):

        self.state_space = state_space #key : string name, value : index
        self.action_space = action_space #key : index, value : name

        self.player_hp_index = self.state_space['player_health']     
        self.player_block_index = self.state_space['player_block']
        self.player_energy_index = self.state_space['player_energy']
        self.boss_hp_index = self.state_space['boss_health']
        self.boss_block_index = self.state_space['boss_block']

        self.state_list_turns = []
        self.new_state_list_turns = []
        self.action_list_turns = []
        self.reward_list_turns = [] 
        self.add_reward_list_turns = [] 
        self.terminal_list_turns = []

    def AssignGameLists(self, state_lists, new_state_lists, action_lists, reward_lists, add_reward_lists, terminal_lists):
        self.state_list_turns = state_lists
        self.new_state_list_turns = new_state_lists
        self.action_list_turns = action_lists
        self.reward_list_turns = reward_lists 
        self.add_reward_list_turns = add_reward_lists 
        self.terminal_list_turns = terminal_lists
    

    def AddRewardFromDamageBlock(self, turn_index, step_index):
        state = self.state_list_turns[turn_index][step_index]
        new_state = self.new_state_list_turns[turn_index][step_index]

        self.old_player_hp = state[self.player_hp_index]
        self.new_player_hp = new_state[self.player_hp_index]

        self.old_player_block = state[self.player_block_index]
        self.new_player_block = new_state[self.player_block_index]
        
        self.old_player_energy = state[self.player_energy_index]
        self.new_player_energy = new_state[self.player_energy_index]

        player_energy_used = self.old_player_energy - self.new_player_energy
        energy_multiplier = 2 if player_energy_used == 0 else 1/(player_energy_used)

        self.old_boss_hp = state[self.boss_hp_index]
        self.new_boss_hp = new_state[self.boss_hp_index]

        self.old_boss_block = state[self.boss_block_index]
        self.new_boss_block = new_state[self.boss_block_index]

        action_number = self.action_list_turns[turn_index][step_index]
        action_card = self.action_space[action_number]



        reward_damage = 0

        #REWARD for dealing damage
        damage_dealt = 0
        
        if(self.old_boss_hp > self.new_boss_hp):
            damage_dealt += self.old_boss_hp - self.new_boss_hp

        if(self.old_boss_block > self.new_boss_block):
            damage_dealt += self.old_boss_block - self.new_boss_block

        reward_damage = damage_dealt * 0.01 * energy_multiplier
        self.add_reward_list_turns[turn_index][step_index] += reward_damage

        if(action_card == 'Bludgeon'): 
            a = 1

        #REWARD for BLOCKing damage
        reward_blocked = 0

        attack_boss_intents = ['boss_intent-Fierce Bash', 'boss_intent-Whirlwind', 'boss_intent-Roll Attack', 'boss_intent-Twin slam']
        attack_boss_intent_indices = []
        for boss_intent in attack_boss_intents:
            attack_boss_intent_indices.append(self.state_space[boss_intent])
        
        is_boss_intent_attack = False
        turn_end_step_index = len(self.state_list_turns[turn_index]) - 1

        for attack_boss_intent_index in attack_boss_intent_indices:
            if self.state_list_turns[turn_index][turn_end_step_index][attack_boss_intent_index] > 0:
                is_boss_intent_attack = True

        if(self.new_player_block > self.old_player_block) and is_boss_intent_attack:
            reward_blocked += (self.new_player_block - self.old_player_block) * 0.03

        #check when block was added in the steps before this step (in the same turn)
        
        blocking_cards = {
            "Defend Plus" : 8,
            "Defend" : 5,
            "Shrug It Off Plus" : 11,
            "Shrug It Off" : 8,
            "Iron Wave Plus" : 7,
            "Iron Wave" : 5
        }

        total_block_gained = 0

        block_indices = []
        for another_step_index in range(step_index, -1, -1):
            action_neuron_number = self.action_list_turns[turn_index][another_step_index]
            card_name = self.action_space[action_neuron_number]

            if card_name in blocking_cards:
                block_indices.append(another_step_index)
                total_block_gained += blocking_cards[card_name]

        for block_index in block_indices:
            action_neuron_number = self.action_list_turns[turn_index][block_index]
            card_name = self.action_space[action_neuron_number]

            self.add_reward_list_turns[turn_index][block_index] += reward_blocked * (blocking_cards[card_name] / total_block_gained) / len(block_indices)



    def RewardFromClothesline(self, turn_index, step_index, isPlus):
        reward_clothesline = 0
        player_hp_three_turn_end = 0
        hp_loss_under_weak = 0

        if (turn_index + 2 < len(self.state_list_turns)) and isPlus:
            step_index_turn_end = len(self.state_list_turns[turn_index + 2]) - 1
            player_hp_three_turn_end = self.new_state_list_turns[turn_index + 2][step_index_turn_end][self.player_hp_index]
        elif turn_index + 1 < len(self.state_list_turns):
            step_index_turn_end = len(self.state_list_turns[turn_index + 1]) - 1
            player_hp_three_turn_end = self.new_state_list_turns[turn_index + 1][step_index_turn_end][self.player_hp_index]
        else:
            step_index_turn_end = len(self.state_list_turns[turn_index]) - 1
            player_hp_three_turn_end = self.new_state_list_turns[turn_index][step_index_turn_end][self.player_hp_index]
        
        if(self.old_player_hp > player_hp_three_turn_end):
            hp_loss_under_weak = self.old_player_hp - player_hp_three_turn_end
        
        reward_clothesline = (hp_loss_under_weak/3) * 0.01

        return reward_clothesline


    def RewardFromDisarm(self, turn_index, step_index, isPlus):
        #REWARD for disarm
        reward_disarm = 0

        boss_damage_instances = 0

        for another_turn_index in range(turn_index, len(self.state_list_turns)):
            step_index_turn_end = len(self.state_list_turns[another_turn_index]) - 1

            old_hp = self.state_list_turns[another_turn_index][step_index_turn_end][1]
            new_hp = self.new_state_list_turns[another_turn_index][step_index_turn_end][1]
            old_block = self.state_list_turns[another_turn_index][step_index_turn_end][2]
            new_block = self.new_state_list_turns[another_turn_index][step_index_turn_end][2]

            if(old_hp > new_hp) or (old_block > new_block):
                boss_damage_instances += 1
            
        strength_reduction = 3 if isPlus else 2

        reward_disarm = boss_damage_instances * strength_reduction * 0.01
    
        return reward_disarm
    
    
    def RewardFromFlex(self, turn_index, step_index, isPlus):
        reward_flex = 0

        strength_multiplier = 1.5 if isPlus else 1

        step_end_index = len(self.state_list_turns[turn_index])
        cumulative_reward = 0

        for another_step_index in range(step_index, step_end_index):
            cumulative_reward += self.add_reward_list_turns[turn_index][another_step_index]

        reward_flex = cumulative_reward * strength_multiplier * 2    #2 is the energy multiplier

        return reward_flex

    
    def RewardFromDoubleTap(self, turn_index, step_index):
        reward_double_tap = 0

        doubletap_index = self.state_space['player_buffs-DoubleTapActive']

        for another_step_index in range(step_index, len(self.state_list_turns[turn_index])):
            
            isDoubleTapActive = self.state_list_turns[turn_index][another_step_index][doubletap_index]
            
            if not isDoubleTapActive:
                reward_double_tap += self.add_reward_list_turns[turn_index][another_step_index] * 0.75

        temp_turn_index = turn_index + 1

        while (reward_double_tap == 0) and (temp_turn_index < len(self.state_list_turns)):
            for another_step_index in range(0, len(self.state_list_turns[temp_turn_index])):
                isDoubleTapActive = self.state_list_turns[temp_turn_index][another_step_index][doubletap_index]
                temp_turn_index += 1
                if isDoubleTapActive:
                    reward_double_tap += self.add_reward_list_turns[turn_index + 1][another_step_index] * 0.75

        return reward_double_tap


    def RewardFromBash(self, turn_index, step_index, isPlus):
        boss_hp_three_turn_end = 0
        hp_loss_under_vul = 0

        if (turn_index + 2 < len(self.state_list_turns)) and isPlus:
            step_index_turn_end = len(self.state_list_turns[turn_index + 2]) - 1
            boss_hp_three_turn_end = self.new_state_list_turns[turn_index + 2][step_index_turn_end][self.boss_hp_index]
        elif turn_index + 1 < len(self.state_list_turns):
            step_index_turn_end = len(self.state_list_turns[turn_index + 1]) - 1
            boss_hp_three_turn_end = self.new_state_list_turns[turn_index + 1][step_index_turn_end][self.boss_hp_index]
        else:
            step_index_turn_end = len(self.state_list_turns[turn_index]) - 1
            boss_hp_three_turn_end = self.new_state_list_turns[turn_index][step_index_turn_end][self.boss_hp_index]
        
        if(self.old_boss_hp > boss_hp_three_turn_end):
            hp_loss_under_vul = self.old_boss_hp - boss_hp_three_turn_end

        reward_bash = hp_loss_under_vul * 0.25 * 0.01 * 0.5 
        #0.25 - vulnerable
        #0.01 - damage reward multiplier
        #0.5 energy multiplier (bash costs 2 energy)
        return reward_bash


    def RewardFromThunderclap(self, turn_index, step_index):
        step_index_turn_end = len(self.state_list_turns[turn_index]) - 1
        boss_hp_turn_end = self.new_state_list_turns[turn_index][step_index_turn_end][self.boss_hp_index]
        hp_loss_under_vul = 0

        if(self.old_boss_hp > boss_hp_turn_end):
            hp_loss_under_vul = self.old_boss_hp - boss_hp_turn_end

        reward_thunderclap = hp_loss_under_vul * 0.25 * 0.01
        #0.25 - vulnerable
        #0.01 - damage reward multiplier

        return reward_thunderclap

    
    def RewardFromUppercut(self, turn_index, step_index, isPlus):
        reward_uppercut = 0
        hp_loss_under_vul = 0
        hp_loss_under_weak = 0

        #reward from vulnerable
        if (turn_index + 1 < len(self.state_list_turns)) and isPlus:
            step_index_turn_end = len(self.state_list_turns[turn_index + 1]) - 1
            boss_hp_two_turn_end = self.new_state_list_turns[turn_index + 1][step_index_turn_end][self.boss_hp_index]
        else:
            step_index_turn_end = len(self.state_list_turns[turn_index]) - 1
            boss_hp_two_turn_end = self.new_state_list_turns[turn_index][step_index_turn_end][self.boss_hp_index]
        
        if(self.old_boss_hp > boss_hp_two_turn_end):
            hp_loss_under_vul = self.old_boss_hp - boss_hp_two_turn_end

        reward_uppercut += hp_loss_under_vul * 0.25 * 0.01 * 0.5
        #0.25 - vulnerable
        #0.01 - damage reward multiplier
        #0.5 energy multiplier (bash costs 2 energy)

        #reward from weakened
        if (turn_index + 1 < len(self.state_list_turns)) and isPlus:
            step_index_turn_end = len(self.state_list_turns[turn_index + 1]) - 1
            player_hp_two_turn_end = self.new_state_list_turns[turn_index + 1][step_index_turn_end][self.player_hp_index]
        else:
            step_index_turn_end = len(self.state_list_turns[turn_index]) - 1
            player_hp_two_turn_end = self.new_state_list_turns[turn_index][step_index_turn_end][self.player_hp_index]
        
        if(self.old_player_hp > player_hp_two_turn_end):
            hp_loss_under_weak = self.old_player_hp - player_hp_two_turn_end
        
        reward_uppercut += (hp_loss_under_weak/3) * 0.01

        return reward_uppercut


