import buff_type 
import game_manager 
import combat_unit 

class EnemyIntent:
    def __init__(self):
        self.is_attack = False
        self.attack_value = 0
        self.is_debuff = False
        self.debuff_type = buff_type.BuffType.Empty
        self.debuff_value = 1
        self.is_enbuff = False
        self.enbuff_type = buff_type.BuffType.Empty
        self.enbuff_value = 1

    def apply_to(self, game_state:game_manager):
        if self.is_attack :
            game_state.player.current_hp -= self.attack_value
        elif self.is_debuff:
            game_state.player.add_new_buff(self.debuff_type,self.debuff_value)