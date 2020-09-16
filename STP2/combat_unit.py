from buff_type import BuffType

class CombatUnit:
    def __init__(self, init_hp, empty_buffs_dict):
        self.max_hP = init_hp
        self.current_hp = init_hp
        self.block = 0
        self.buff_dict = empty_buffs_dict

    def add_new_buff(self, buff_name: str,buff_value:int):
        self.buff_dict[buff_name] += buff_value
        
    def refresh_buff_on_new_turn(self):
        duration_buffs = ['Weakened','Vulnerable','Intangible','Frail','Entangled','Blur','DrawReduction']
        # handle duration buffs
        for duration_buff in duration_buffs:
            if self.buff_dict[duration_buff] > 0:
                self.buff_dict[duration_buff] -= 1
        # handle flex
        if self.buff_dict['Flex'] > 0:
            self.buff_dict['Strength'] -= self.buff_dict['Flex']
            self.buff_dict['Flex'] = 0