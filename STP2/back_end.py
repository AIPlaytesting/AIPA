import socket
import sys
import protocol
import json
import time
from game_manager import GameManager
from enemy_intent import EnemyIntent
from collections import namedtuple

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

    # play card till choose to end
    while(not game_manager.is_player_finish_turn()):
        cards_on_hand = game_manager.get_current_cards_on_hand()
        playable_cards = game_manager.get_current_playable_cards()
        # print log of cards
        game_manager.print_cards_info_on_hand()
        
        # get input    
        player_input = get_player_input(player_socket)
        # process player input
        if player_input.type == protocol.INPUT_TYPE_PLAY_CARD:
            card_name = player_input.cardName
            game_manager.card_play_manager.PlayCard(card_name)  
        elif player_input.type == protocol.INPUT_TYPE_END_TURN:
            game_manager.end_player_turn()             
        else:
            print('invalid input, type == ',player_input.type)      
        # send response every time play card
        send_response(player_socket,game_manager)

    # enemy turn
    game_manager.start_enemy_turn()
    
    # check is player killed all enemies
    if not game_manager.is_game_end():     
        # apply BOSS intent
        game_manager.execute_enemy_intent()   
    # send respone when enemy end
    send_response(player_socket,game_manager)

def send_response(player_socket,game_manager):
        game_state_markup = protocol.MarkupFactory.create_game_state_markup(game_manager.game_state,game_manager.card_play_manager)
        game_sequence_markup_file = protocol.MarkupFactory.create_game_sequence_markup_file(
            game_state_markup,[],game_state_markup
        )
        game_sequence_markup_json = json.dumps(game_sequence_markup_file)
        print("markup json: ",game_sequence_markup_json)
        response_message ={'gameSequenceMarkupJSON':game_sequence_markup_json} 
        response_message_json = json.dumps(response_message)
        player_socket.send(response_message_json.encode())

def get_player_input(socket)->protocol.UserInput:
    data = socket.recv(1024) 
    print('recv json: ',data.decode())
    message_json_data = data.decode()
    message_dict = json.loads(message_json_data) 
    user_input_dict = message_dict['userInput']
    user_input = protocol.UserInput(user_input_dict['type'],user_input_dict['cardName'])
    print("type: ",user_input.type,"cardName",user_input.cardName)
    return user_input

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 9999)
print ('connecting to: ',server_address)
sock.connect(server_address)
print ('connected to: ',server_address)

# play game
try:
    run_game(sock)
except Exception as e:
    print(e)

time.sleep(2)

# try:     
#     while True:
#         # recv data
#         data = sock.recv(1024) 
#         print('recv:',data.decode())
#         # echo back
#         sock.send("I received your message!".encode())
# finally:
#     print ('closing socket') 
#     sock.close()