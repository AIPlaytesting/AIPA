from enemy_intent import EnemyIntent 
import random

class EnemyAI:
    def __init__(self):
        pass

    def make_intent(self)->EnemyIntent:
        intent = EnemyIntent()
        intent.is_attack = True
        intent.attack_value = random.randint(1,20)
        print("BOSS intent: -[attack]-",intent.attack_value)
        return intent