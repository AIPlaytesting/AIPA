from .buff_extension import BuffExtension
from .extension_context import BuffExtensionCtx
from gameplay.combat_unit import CombatUnit

class Weaken(BuffExtension):
    def before_launch_attack(self,ctx:BuffExtensionCtx,attack_target:CombatUnit,attack_value:int)->int:
        print("[Buff Extension] WEAK EXECUTTED!!!!!!!")
        return attack_value*0.75

