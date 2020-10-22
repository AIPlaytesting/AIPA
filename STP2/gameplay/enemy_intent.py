from . import game_manager 
from . import combat_unit 
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