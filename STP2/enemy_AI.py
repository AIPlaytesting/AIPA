from enemy_intent import EnemyIntent 
import random
import buff_type
class EnemyAI:
    def __init__(self):
        self.intents = ['Charging Up', 'Fierce Bash', 'Vent Steam', 'Whirlwind']
        self.curStateIndex = 0
        self.mode = ['Offensive', 'Defensive']
        self.modeIndex = 0
        self.modeShiftValue = 30

    # Offensive AI
    def make_intent(self)->EnemyIntent:
        intent = EnemyIntent()
        curState = self.intents[self.curStateIndex]
        if curState == 'Charging Up':
            intent.is_enbuff = True
            intent.enbuff_type = buff_type.BuffType.Defend
            intent.enbuff_value = 9
        elif curState == 'Fierce Bash':
            intent.is_attack = True
            intent.attack_value = 32
            print("BOSS intent: -[attack]-",intent.attack_value)
        elif curState == 'Vent Steam':
            intent.is_debuff = True
            intent.debuff_type = buff_type.BuffType.Weakened
            intent.debuff_value = 1
            print("BOSS intent: -[debuff]-",intent.debuff_type)
        elif curState == 'Whirlwind':
            intent.is_attack = True
            intent.attack_value = 32
            print("BOSS intent: -[attack]-",intent.attack_value)
        # move to the next intent
        self.curStateIndex = (self.curStateIndex + 1) % len(self.intents)
        return intent
        
    # whirlwind makes 4 attack, return a list of Enemy Intent?
    # 1 Enemy Intent for now

    # every time boss got hit and its offensive mode, it will calculate whether modeShiftValue < 0.
    # if yes, then turn to defensive mode.
    # 