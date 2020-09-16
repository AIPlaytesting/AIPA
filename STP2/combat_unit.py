from buff_type import BuffType

class CombatUnit:
    def __init__(self, init_hp, empty_buffs_dict):
        self.max_hP = init_hp
        self.current_hp = init_hp
        self.block = 0
        self.buff_dict = empty_buffs_dict

    def add_new_buff(self, buff_type: BuffType,buff_value:int):
        new_buff = ActivatedBuff(buff_type,buff_value)
        # TODO
        print("TO-DO: ","add buff of ", buff_type)
        #self.buff_dict.append(new_buff)


class ActivatedBuff:
    def __init__(self,buff_type,buff_value):
        self.buff_type = buff_type
        self.buff_value = buff_value