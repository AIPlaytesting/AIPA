from gameplay.combat_unit import CombatUnit
from .extension_context import BuffExtensionCtx

class BuffExtension:
    def after_turn_start(self,ctx:BuffExtensionCtx):
        pass

    # attack_source attack buff_host
    # return the final attack value 
    def before_receive_attack(self,ctx:BuffExtensionCtx,attack_source:CombatUnit,attack_value:int)->int:
        return attack_value
    
    def before_launch_attack(self,ctx:BuffExtensionCtx,attack_target:CombatUnit,attack_value:int)->int:
        return attack_value
