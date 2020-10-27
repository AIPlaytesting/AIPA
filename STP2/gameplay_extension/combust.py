from .buff_extension import BuffExtension
from .extension_context import BuffExtensionCtx
from gameplay.combat_unit import CombatUnit

class Combust(BuffExtension):
    def before_turn_start(self,ctx:BuffExtensionCtx):
        pass
    