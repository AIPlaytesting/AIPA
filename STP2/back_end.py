import socket
import sys
import protocol
import json
import time
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

def run_game(player_socket): 
    # init 
    game_manager = GameManager()
    game_manager.init_game()
    # play
    while(not game_manager.is_game_end()):
       play_one_round(game_manager,player_socket)
    # print result
    result = 'Win' if game_manager.is_player_win() else 'lost'
    print("result:---------------------\n"+result)
 
def play_one_round(game_manager,player_socket):
    # player turn
    game_manager.start_player_turn()
    print('send response, start turn')
    send_response(player_socket,game_manager,[])
    # play card till choose to end
    while(not game_manager.is_player_finish_turn()):
        cards_on_hand = game_manager.get_current_cards_on_hand()
        playable_cards = game_manager.get_current_playable_cards()
        # print log of cards
        game_manager.print_cards_info_on_hand()
        
        # get input    
        player_input = get_player_input(player_socket)
        # game events triggered after apply this player input
        game_events_of_input = []
        if player_input.type == protocol.INPUT_TYPE_PLAY_CARD:
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

        # send response every time play card
        print('send response, card play')
        send_response(player_socket,game_manager,game_events_of_input)

    # enemy turn
    game_manager.start_enemy_turn()
    
    # check is player killed all enemies
    if not game_manager.is_game_end():     
        # apply BOSS intent
        game_manager.execute_enemy_intent()   

def send_response(player_socket,game_manager,game_events):
        game_state_markup = protocol.MarkupFactory.create_game_state_markup(game_manager.game_state,game_manager.card_play_manager)
        game_sequence_markup_file = protocol.MarkupFactory.create_game_sequence_markup_file(
            game_state_markup,game_events,game_state_markup
        )
        game_sequence_markup_json = json.dumps(game_sequence_markup_file)
        response_message ={'gameSequenceMarkupJSON':game_sequence_markup_json} 
        response_message_json = json.dumps(response_message)
        player_socket.send(response_message_json.encode())

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
