import buff_type 
import game_manager 
import combat_unit 
import json

class EnemyIntent:
    def __init__(self):
        self.name = "unnamed_intent"
        self.is_attack = False
        self.attack_value = 0
        self.is_debuff = False
        self.debuff_type = buff_type.BuffType.Empty
        self.debuff_value = 1
        self.is_enbuff = False
        self.enbuff_type = buff_type.BuffType.Empty
        self.enbuff_value = 1

    def apply_to(self, game_state:game_manager):
        ### TODO: apply effect manager calculation
        if self.is_attack :
            game_state.player.current_hp -= self.attack_value
        elif self.is_debuff:
            game_state.player.add_new_buff(self.debuff_type,self.debuff_value)
        elif self.is_enbuff:
            game_state.boss.add_new_buff(self.enbuff_type,self.enbuff_value)
# class EnemyIntentPool:
#     def __init__(self,intents:[]):
#         self.intents = intents

#     @classmethod
#     def load_from_path(cls,path):
#         with open(path, "r") as file:
#             raw_json_data = file.read()
#         self.__dict__ = json.loads(raw_json_data)   

#     def to_json(self):
#         return json.dumps(self,default=lambda o: o.__dict__)

# print("TEST: ")
# dummy_intent = EnemyIntent()
# intentPool = EnemyIntentPool([dummy_intent,dummy_intent,dummy_intent])
# print(intentPool.to_json())