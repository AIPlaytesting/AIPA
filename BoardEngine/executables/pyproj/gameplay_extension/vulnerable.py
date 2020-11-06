
from .buff_extension import BuffExtension
from .extension_context import BuffExtensionCtx
from gameplay.combat_unit import CombatUnit

class Vulnerable(BuffExtension):
    # attack_source attack buff_host
    # return the final attack value 
    def before_receive_attack(self,ctx:BuffExtensionCtx,attack_source:CombatUnit,attack_value:int)->int:
        print("[Buff Extension] valunerable exetued!")
        return attack_value*1.5
    
