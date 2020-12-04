from .buff_extension import BuffExtension
from .extension_context import BuffExtensionCtx
from gameplay.combat_unit import CombatUnit

class Strength(BuffExtension):
    def before_launch_attack(self,ctx:BuffExtensionCtx,attack_target:CombatUnit,attack_value:int)->int:
        multiplier = 1
        if 'strength_multiplier' in ctx.extra_info:
            multiplier = ctx.extra_info['strength_multiplier']
        atk_increment = ctx.buffvalue*multiplier
        print("[Buff Extension] strengh from ",attack_value,"to",attack_value + atk_increment)
        return attack_value + atk_increment
