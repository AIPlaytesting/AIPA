import socket
import sys
import protocol
import json
import time
import db.game_database
from game_manager import GameManager
from game_event import GameEvent
from enemy_intent import EnemyIntent
from collections import namedtuple
from game_recorder.game_recorder import GameRecorder

def back_end_main_loop(player_socket):
    while True:
        wait_start_game_request(player_socket)
        run_game(player_socket)

def wait_start_game_request(player_socket):
    while True:
        player_input = get_player_input(player_socket)
        if player_input.type == protocol.INPUT_TYPE_START_GAME:
            break
    print("start game request received!")

def wait_end_boss_turn_request(player_socket):
    while True:
        player_input = get_player_input(player_socket)
        if player_input.type == protocol.INPUT_TYPE_END_TURN:
            break
    print("end boss turn request received!")

def run_game(player_socket): 
    # load database
    db_root = db.game_database.calculate_root_dir()
    game_db = db.game_database.GameDatabase(db_root)
    # init 
    game_manager = GameManager(game_db.game_app_data)
    game_manager.init_game()
    game_recorder.start_record_one_battle()
    # play
    while(not game_manager.is_game_end()):
       play_one_round(game_manager,player_socket)

    # process result
    if game_manager.is_player_win():
        print("Player win")
        send_gamestage_change_message(player_socket,protocol.GAMESTAGE_WIN)
    else:
        print("Player lost")
        send_gamestage_change_message(player_socket,protocol.GAMESTAGE_LOST)

    # save recorded data
    game_recorder.save_record_data()
 
def play_one_round(game_manager,player_socket):
    # player turn
    game_manager.start_player_turn()
    send_gamestage_change_message(player_socket,protocol.GAMESTAGE_PLAYER_TURN)

    # record player turn start state
    game_recorder.record_game_state(game_manager.game_state)
    # send resonce back
    print('send response, start turn')
    gamestate_markup = protocol.MarkupFactory.create_game_state_markup(game_manager.game_state)    
    send_game_sequence_response(player_socket, gamestate_markup,[],gamestate_markup)
    # play card till choose to end
    while(not game_manager.is_player_finish_turn()):
        # record state before play card
        game_recorder.record_game_state(game_manager.game_state)
        # record end game state markup
        playerturn_start_gamestate_markup = protocol.MarkupFactory.create_game_state_markup(game_manager.game_state)

        cards_on_hand = game_manager.get_current_cards_on_hand()
        playable_cards = game_manager.get_current_playable_cards()
        # print log of cards
        game_manager.print_cards_info_on_hand()
        
        # get input    
        player_input = get_player_input(player_socket)
        # game events triggered after apply this player input
        game_events_of_input = []
        if player_input.type == protocol.INPUT_TYPE_PLAY_CARD:
            # validate card play input
            valid, message = validate_play_card_input(player_input.cardName,game_manager.game_state)
            if not valid:
                send_error_message_response(player_socket, message)
                continue

            # record play card event
            play_card_event = GameEvent.create_play_card_event(player_input.cardGUID)
            game_events_of_input.append(play_card_event)
            # play card
            card_name = player_input.cardName
            events_after_played_card = game_manager.card_play_manager.PlayCard(card_name)  
            # record events after played card
            game_events_of_input.extend(events_after_played_card)
        elif player_input.type == protocol.INPUT_TYPE_END_TURN:
            game_manager.end_player_turn()             
        else:
            print('invalid input, type == ',player_input.type)      

        # record game events
        game_recorder.record_game_events(game_events_of_input)
        # record end game state markup
        playerturn_end_gamestate_markup = protocol.MarkupFactory.create_game_state_markup(game_manager.game_state)
        # send response every time play card
        print('send response, card play')
        send_game_sequence_response(
            player_socket,
            playerturn_start_gamestate_markup,
            game_events_of_input,
            playerturn_end_gamestate_markup)

    # enemy turn
    game_manager.start_enemy_turn()

    send_gamestage_change_message(player_socket,protocol.GAMESTAGE_ENEMY_TURN)
    # record start game state as markup
    bossturn_start_gamestate_markup = protocol.MarkupFactory.create_game_state_markup(game_manager.game_state)
    
    enemy_intent_game_events = []
    # check is player killed all enemies
    if not game_manager.is_game_end():     
        # apply BOSS intent
        enemy_intent_game_events = game_manager.execute_enemy_intent()   
    
    #record start game state as markup
    bossturn_end_gamestate_markup = protocol.MarkupFactory.create_game_state_markup(game_manager.game_state)
    # send game sequence of boss turn
    send_game_sequence_response(
        player_socket,
        bossturn_start_gamestate_markup,
        enemy_intent_game_events, 
        bossturn_end_gamestate_markup)

    # wait player input to end boss turn_buffer
    wait_end_boss_turn_request(player_socket)

def validate_play_card_input(card_name_to_play,game_state):
    card = game_state.cards_dict[card_name_to_play]
    card_energy = card.energy_cost
    player_energy = game_state.player_energy
    if card_energy <= player_energy:
        return True,""
    else:
        return False,"no energy to play this card"

def send_error_message_response(player_socket,error_message):
    response_message = protocol.ResponseMessage(protocol.MESSAGE_TYPE_ERROR,error_message)
    player_socket.send(response_message.to_json().encode())

def send_game_sequence_response(player_socket,start_gamestate_markup,game_events,end_gamestate_markup):
        # encode game sequence markup file to json      
        game_sequence_markup_file = protocol.MarkupFactory.create_game_sequence_markup_file(
            start_gamestate_markup,game_events,end_gamestate_markup)
        game_sequence_markup_json = json.dumps(game_sequence_markup_file)
        # send message
        response_message = protocol.ResponseMessage(protocol.MESSAGE_TYPE_GAME_SEQUENCE,game_sequence_markup_json)
        player_socket.send(response_message.to_json().encode())

def send_gamestage_change_message(player_socket,gamestage):
    response_message = protocol.ResponseMessage(protocol.MESSAGE_TYPE_GAMESTAGE_CHANGE,gamestage)
    player_socket.send(response_message.to_json().encode())

def get_player_input(socket)->protocol.UserInput:
    data = socket.recv(1024) 
    print('recv json: ',data.decode())
    message_json_data = data.decode()
    message_dict = json.loads(message_json_data) 
    user_input_dict = message_dict['userInput']
    user_input = protocol.UserInput(
        user_input_dict['type'],
        user_input_dict['cardName'],
        user_input_dict['cardGUID'])
    print("type: ",user_input.type,"cardName",user_input.cardName)
    return user_input

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 9999)
print ('connecting to: ',server_address)
sock.connect(server_address)
print ('connected to: ',server_address)

# create game_recorder 
game_recorder = GameRecorder()

# play game
back_end_main_loop(sock)

time.sleep(2)
