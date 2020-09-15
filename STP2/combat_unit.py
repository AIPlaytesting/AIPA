from STP2.buff_type import BuffType

class CombatUnit:
    def __init__(self,initHp):
        self.maxHP = initHp
        self.currentHP = initHp
        self.block = 0
        self.activatedBuffs = [] # list of ActivatedBuff[]

    def add_new_buff(self, buffType: BuffType,buffValue:int):
        newBuff = ActivatedBuff(buffType,buffValue)
        self.activatedBuffs.append(newBuff)
        
class ActivatedBuff:
    def __init__(self,buffType,buffValue):
        self.buffType = buffType
        self.buffValue = buffValue