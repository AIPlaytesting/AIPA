from gameplay.combat_unit import CombatUnit
from .extension_context import ExtensionContext

class BuffBase:
    def __init__(self,buffname:str,ctx:ExtensionContext):
        self.ctx = ctx
        self.buffname = buffname
        self.buffvalue = 0
    
    def after_turn_start(self,buff_host:CombatUnit):
        pass

    # attack_source attack buff_host
    # return the final attack value 
    def before_receive_attack(self,buff_host:CombatUnit,attack_source:CombatUnit,attack_value:int)->int:
        return attack_value
    
    def before_launch_attack(self,buff_host:CombatUnit,attack_target:CombatUnit,attack_value:int)->int:
        return attack_value
