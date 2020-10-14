from gameplay.game_manager import GameManager
from gameplay.game_event import GameEvent

# GameplayKernel is a highier level verision of GameManager
# while GameManager give you more contronal and deteils,
# GameplayKernel manage and hide those detials, make it more convenient to use
class GameplayKernel:
    def __init__(self):
        pass

    def reset_game(self):
        pass
    
    def get_game_state(self):
        pass

    # return GameEvents[]
    def apply_user_input(self):
        pass
