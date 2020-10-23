from gameplay.game_state import GameState
from gameplay.event_system import EventManager

class ExtensionContext:
    def __init__(self,game_state:GameState,event_manager:EventManager):
        self.game_state = game_state
        self.event_manager = event_manager