from .connection import Connection
from .gameplay_kernel import GameplayKernel
from .db_accessor import DBAccessor
from .protocol import RequestMessage,ResponseMessage, PlayerStep,DBQuery, MarkupFactory

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
            elif request.method == 'DBQuery':
                self.__on_recv_dbquery(request.db_query)
    
    def __on_recv_dbquery(self,dbquery:DBQuery):
        query_result = self.__db_accessor.process_dbquery(dbquery)
        response = ResponseMessage.cretate_dbquery_result_response(dbquery.query_id,query_result)
        self.__connection.send_response(response)

    def __on_recv_reset_game(self):
        # reset game 
        gamesequence_markup = self.__execute_change_gamestate_func(self.__gameplay_kernal.reset_game)
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
        gamesequence_markup = self.__execute_change_gamestate_func(lambda: self.__gameplay_kernal.execute_player_step(player_step))
        # send response for this playerStep
        response = ResponseMessage.create_game_sequence_response(gamesequence_markup)
        self.__connection.send_response(response)

        # if it became enemy turn, then execute enemy turn
        if self.__gameplay_kernal.get_game_state().game_stage == 'EnemyTurn':
            gamesequence_markup = self.__execute_change_gamestate_func(self.__gameplay_kernal.execute_enemy_turn)
            # send response for this playerStep
            response = ResponseMessage.create_game_sequence_response(gamesequence_markup)
            self.__connection.send_response(response)     


    # execute functions that change game state create game sequence
    # change_gamestate_func: this func MUST return GameEvent[]
    # return gamesequence_markup(dict)
    def __execute_change_gamestate_func(self,change_gamestate_func)->dict:
        gamestate_markup_before = self.__snapshot_gamestate_as_markup()
        game_events =  change_gamestate_func()      
        gamestate_markup_after = self.__snapshot_gamestate_as_markup()
        # encode game sequence of this step
        gamesequence_markup = MarkupFactory.create_game_sequence_markup_file(
            gamestate_markup_before,
            game_events,
            gamestate_markup_after)
        return gamesequence_markup

    # return gamestate markup of current gamestate
    def __snapshot_gamestate_as_markup(self)->dict:
        return MarkupFactory.create_game_state_markup(self.__gameplay_kernal.get_game_state())