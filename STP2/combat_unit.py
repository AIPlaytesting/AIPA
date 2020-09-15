from buff_type import BuffType

class CombatUnit:
    def __init__(self,init_hp):
        self.max_hP = init_hp
        self.current_hp = init_hp
        self.block = 0
        self.activated_buffs = [] # list of ActivatedBuff[]

    def add_new_buff(self, buff_type: BuffType,buff_value:int):
        new_buff = ActivatedBuff(buff_type,buff_value)
        self.activated_buffs.append(new_buff)
        
class ActivatedBuff:
    def __init__(self,buff_type,buff_value):
        self.buff_type = buff_type
        self.buff_value = buff_value