class CombatUnit:
    def __init__(self,initHp):
        self.maxHP = initHp
        self.currentHP = initHp
        self.block = 0
        self.activatedBuffs = [] # list of ActivatedBuff[]

class ActivatedBuff:
    def __init__(self,buffType,buffValue):
        self.buffType = buffType
        self.buffValue = buffValue