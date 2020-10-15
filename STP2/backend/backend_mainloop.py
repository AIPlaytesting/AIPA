from .connection import Connection
from .gameplay_kernel import GameplayKernel
from .db_accessor import DBAccessor
from .protocol import RequestMessage,ResponseMessage, PlayerStep, MarkupFactory

class BackendMainloop:
    def __init__(self,connection:Connection,gameplay_kernal:GameplayKernel,db_accessor:DBAccessor):
        self.__connection  = connection
        self.__gameplay_kernal = gameplay_kernal
        self.__db_accessor = db_accessor

    def run(self):
        print("back end running....")
        while True:
            request = self.__connection.wait_one_request()
            if request.method == 'ResetGame':
                self.__on_recv_reset_game()
            elif request.method == 'PlayerStep':
                self.__on_recv_player_step(request.player_step)
    
    def __on_recv_reset_game(self):
        # reset game 
        gamestate_markup_before = self.__snapshot_gamestate_as_markup()
        game_events_during_reset = self.__gameplay_kernal.reset_game()
        gamestate_markup_after = self.__snapshot_gamestate_as_markup()
        # encode game sequence
        gamesequence_markup = MarkupFactory.create_game_sequence_markup_file(
            gamestate_markup_before,
            game_events_during_reset,
            gamestate_markup_after)
        # send response
        response = ResponseMessage.create_game_sequence_response(gamesequence_markup)
        self.__connection.send_response(response)

    def __on_recv_player_step(self,player_step:PlayerStep):
        is_valid,error_message = self.__gameplay_kernal.validate_player_step(player_step)
        
        if not is_valid:
            # send error message back
            response = ResponseMessage.create_error_message_response(error_message)
            self.__connection.send_response(response)
            return

        # execute step and send sequence back
        gamestate_markup_before = self.__snapshot_gamestate_as_markup()
        game_events =  self.__gameplay_kernal.execute_player_step(player_step)      
        gamestate_markup_after = self.__snapshot_gamestate_as_markup()
        # encode game sequence of this step
        gamesequence_markup = MarkupFactory.create_game_sequence_markup_file(
            gamestate_markup_before,
            game_events,
            gamestate_markup_after)
        # send response for this playerStep
        response = ResponseMessage.create_game_sequence_response(gamesequence_markup)
        self.__connection.send_response(response)

        # if it became enemy turn, then execute enemy turn
        if self.__gameplay_kernal.get_game_state().game_stage == 'EnemyTurn':
            gamestate_markup_before = self.__snapshot_gamestate_as_markup()
            game_events =  self.__gameplay_kernal.execute_enemy_turn()    
            gamestate_markup_after = self.__snapshot_gamestate_as_markup()
            # encode game sequence of this step
            gamesequence_markup = MarkupFactory.create_game_sequence_markup_file(
                gamestate_markup_before,
                game_events,
                gamestate_markup_after)
            # send response for this playerStep
            response = ResponseMessage.create_game_sequence_response(gamesequence_markup)
            self.__connection.send_response(response)     

    # return gamestate markup of current gamestate
    def __snapshot_gamestate_as_markup(self)->dict:
        return MarkupFactory.create_game_state_markup(self.__gameplay_kernal.get_game_state())