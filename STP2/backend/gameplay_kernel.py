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
        if player_step.type == "PlayCard":
            game_state = self.__game_manager.game_state
            card_name_to_play = player_step.cardName
            card_to_play = game_state.cards_dict[card_name_to_play]
            player_energy = game_state.player_energy
            if card_to_play.energy_cost <= player_energy:
                return True,""
            else:
                return False,"no energy to play this card"
        elif player_step.type == "EndTurn":
            return False,"no implementation"
        else:
            return False,"able to validate player step"

    # return GameEvents[]
    def execute_player_step(self,player_step:PlayerStep):
        game_events_during_step = []

        if player_step.type == "PlayCard":
            # record play card event
            play_card_event = GameEvent.create_play_card_event(player_step.cardGUID)
            game_events_during_step.append(play_card_event)
            # play card
            events_after_played_card = self.__game_manager.card_play_manager.PlayCard(player_step.cardName)  
            # record events after played card
            game_events_during_step.extend(events_after_played_card)
        elif player_step.type == "EndTurn":
            pass

        # return game event
        return game_events_during_step

    # return GameEvents[]
    def execute_enemy_step(self):
        pass