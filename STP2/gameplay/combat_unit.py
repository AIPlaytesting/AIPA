class CombatUnit:
    def __init__(self,name, game_unique_id, init_hp, all_buffnames):
        self.game_unique_id = game_unique_id
        self.name = name
        self.max_hP = init_hp
        self.current_hp = init_hp
        self.block = 0
        # the value in buff dict is the value(int) of buff
        self.buff_dict = {}
        for buffname in all_buffnames:
            self.buff_dict[buffname] = 0

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
    
    def print_status_info(self,owner_name):
        buff_list= []
        for buff_name in self.buff_dict.keys():
            if(self.buff_dict[buff_name] != 0):
                buff_list.append(buff_name+":"+str(self.buff_dict[buff_name]))
        print(owner_name,"(block): "+ str(self.block),"(buffs):",buff_list)