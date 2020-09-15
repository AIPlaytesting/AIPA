class CombatUnit:
    def __init__(self,initHp):
        self.maxHP = initHp
        self.currentHP = initHp
        self.block = 0
        # list of ActivatedBuff[]
        self.activatedBuffs = []

class ActivatedBuff:
    def __init__(self,buffType,buffValue):
        self.buffType = buffType
        self.buffValue = buffValue