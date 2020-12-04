from gameplay.game_state import GameState
from gameplay.combat_unit import CombatUnit

class ExtensionContext:
    def __init__(self,game_state:GameState):
        self.game_state = game_state

class BuffExtensionCtx(ExtensionContext):
    def __init__(self,game_state:GameState,buffname:str,buffvalue:int,buffhost:CombatUnit,extra_info = {}):
        ExtensionContext.__init__(self,game_state)
        self.buffname = buffname
        self.buffvalue = buffvalue
        self.buffhost = buffhost
        self.extra_info = extra_info

class KeywordExtensionCtx(ExtensionContext):
    def __init__(self,game_state:GameState):
        ExtensionContext.__init__(self,game_state)