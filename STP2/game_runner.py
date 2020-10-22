from gameplay.game_manager import GameManager
from gameplay.enemy_intent import EnemyIntent
import db.game_database

def run_game(is_AI_mode):
    # load game data based 
    db_root = db.game_database.calculate_root_dir()
    game_db = db.game_database.GameDatabase(db_root)
    game_db.print_data_to_terminal()

    # init 
    game_manager = GameManager(game_db.game_app_data)
    game_manager.init_game()
    # play
    while(not game_manager.is_game_end()):
       play_one_round(is_AI_mode,game_manager)
    # print result
    result = 'Win' if game_manager.is_player_win() else 'lost'
    print("result:---------------------\n"+result)
 
def play_one_round(is_AI_mode,game_manager:GameManager):
    # player turn
    game_manager.start_player_turn()

    # play card till choose to end
    while(not game_manager.is_player_finish_turn()):
        cards_on_hand = game_manager.get_current_cards_on_hand()
        playable_cards = game_manager.get_current_playable_cards()
        # print log of cards
        game_manager.print_cards_info_on_hand()
        # make decison based-on AI/player mode       
        if is_AI_mode:
            pass
            # TODO card_to_play = RL_AI.make_decision( )
        else:
            raw_input = input()
            player_input = process_player_input(raw_input,cards_on_hand,playable_cards)
            # process player input
            if player_input == 'end':
                game_manager.end_player_turn()
            elif player_input == 'invalid':
                print('make input again:')
            else:
                card_to_play = player_input
                print("player play card: ", card_to_play)
                game_manager.execute_play_card(card_to_play)   

        if is_AI_mode:
            pass
            # TODO RL_AI.calculate_reward(game_state,)

    # enemy turn
    game_manager.start_enemy_turn()
    
    # check is player killed all enemies
    if not game_manager.is_game_end():     
        # apply BOSS intent
        game_manager.execute_enemy_intent()    

# reutrn: 1) 'end' 2) "card name" 3) 'invalid'
def process_player_input(raw_input, cards_on_hand, playable_cards):
    if raw_input == 'end':
        return 'end'
    elif raw_input.isnumeric():
        card_index = int(raw_input)
        if card_index >= 0 and card_index < len(cards_on_hand):
            card_to_play = cards_on_hand[card_index]
            if card_to_play in playable_cards:
                return card_to_play
            else:
                print("[ERROR]: try to play unplayable card on hand: " + card_to_play)
    
    print("[WARNNING - invalid input]: "+raw_input)
    return 'invalid'

run_game(False)
