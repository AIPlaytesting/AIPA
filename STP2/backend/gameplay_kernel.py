from gameplay.game_manager import GameManager
from gameplay.game_event import GameEvent
from gameplay.game_state import GameState
from .protocol import PlayerStep

# GameplayKernel is a highier level verision of GameManager
# while GameManager give you more contronal and deteils,
# GameplayKernel manage and hide those detials, make it more convenient to use
class GameplayKernel:
    def __init__(self,game_manager:GameManager):
        self.__game_manager = game_manager

    def reset_game(self):
        self.__game_manager.init_game()
        self.__game_manager.start_player_turn()
    
    def is_game_ended(self)->bool:
        return self.__game_manager.is_game_end()

    def get_game_state(self)->GameState:
        return self.__game_manager.game_state

    # if a step can be applied in current situation
    def validate_player_step(self,player_step:PlayerStep)->(bool,str):
        return False,"no implementation"
        
    # return GameEvents[]
    def execute_player_step(self,player_step:PlayerStep):
        if player_step.type == "PlarCard":
            pass
        elif player_step.type == "EndTurn":
            pass
        # apply input 

        # return game event
        pass

    # return GameEvents[]
    def execute_enemy_step(self):
        pass