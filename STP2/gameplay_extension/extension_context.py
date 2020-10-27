from gameplay.game_state import GameState
from gameplay.combat_unit import CombatUnit

class ExtensionContext:
    def __init__(self,game_state:GameState):
        self.game_state = game_state

class BuffExtensionCtx(ExtensionContext):
    def __init__(self,game_state:GameState,buffname:str,buffvalue:int,buffhost:CombatUnit):
        ExtensionContext.__init__(self,game_state)
        self.buffname = buffname
        self.buffvalue = buffvalue
        self.buffhost = buffhost


class KeywordExtensionCtx(ExtensionContext):
    def __init__(self,game_state:GameState):
        ExtensionContext.__init__(self,game_state)