from .buff_extension import BuffExtension
from .extension_context import BuffExtensionCtx
from gameplay.combat_unit import CombatUnit

class Strength(BuffExtension):
    def before_launch_attack(self,ctx:BuffExtensionCtx,attack_target:CombatUnit,attack_value:int)->int:
        print("[Buff Extension] strengh from ",attack_value,"to",attack_value + ctx.buffvalue)
        return attack_value + ctx.buffvalue
