import buff_type 
import game_manager 
import combat_unit 
import json

class EnemyIntent:
    def __init__(self):
        self.name = "unnamed_intent"
        self.is_attack = False
        self.attack_value = 0
        self.is_block = False
        self.block_value = 0
        self.is_debuff = False
        self.debuff_type = ""
        self.debuff_value = 1
        self.is_enbuff = False
        self.enbuff_type = ""
        self.enbuff_value = 1

    def apply_to(self, game_state,effect_calculator):
        if self.is_attack :
            effect_calculator.DealDamage(game_state.boss,game_state.player,self.attack_value,1)
        elif self.is_block:
            effect_calculator.AddBlock(game_state.boss,self.block_value)
        elif self.is_debuff:
            effect_calculator.ApplyBuff(game_state.boss,game_state.player,self.debuff_type,self.debuff_value)
        elif self.is_enbuff:
            effect_calculator.ApplyBuff(game_state.boss,game_state.boss,self.enbuff_type,self.enbuff_value)
