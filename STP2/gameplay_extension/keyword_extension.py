from gameplay.combat_unit import CombatUnit
from .extension_context import KeywordExtensionCtx

class KeywordExtension:
    def before_played(self,ctx:KeywordExtensionCtx):
        pass
    
    def after_played(self,ctx:KeywordExtensionCtx):
        pass