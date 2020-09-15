from enemy_intent import EnemyIntent 
import random
import buff_type

class EnemyAI:
    def __init__(self):
        pass

    # place holder AI: make 3 kinds of decison randomly 
    def make_intent(self)->EnemyIntent:
        intent = EnemyIntent()
        intent_type_rand = random.random()
        if intent_type_rand < 0.33:
            # attack intent
            intent.is_attack = True
            intent.attack_value = random.randint(1,20)
            print("BOSS intent: -[attack]-",intent.attack_value)
        elif intent_type_rand < 0.66:
            # debuff intent
            intent.is_debuff = True
            intent.debuff_type = buff_type.BuffType.Weakened
            intent.debuff_value = 1
            print("BOSS intent: -[debuff]-",intent.debuff_type)
        else:
            # enbuff intent
            intent.is_enbuff = True
            intent.enbuff_type = buff_type.BuffType.Artifact
            intent.enbuff_value = 1
            print("BOSS intent: -[enbuff]-",intent.enbuff_type)
        return intent