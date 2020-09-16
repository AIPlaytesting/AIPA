from game_manager import GameManager

def run_game(is_AI_mode):
    game_manager = GameManager()
    game_manager.init_game()
    while(not game_manager.is_game_end()):
        # player turn
        game_manager.start_player_turn()
        # generate action space
        action_space = game_manager.get_current_playable_cards()
        print("action space: ",action_space)
        
        # play card till no energy 
        dead_loop_counter = 0
        while(not game_manager.is_player_finish_turn()):
            dead_loop_counter += 1
            if is_AI_mode:
                pass
                # TODO card_to_play = RL_AI.make_decision( )
            else:
                player_input= input()
                if player_input == 'end':
                    game_manager.end_player_turn()
                else:
                    card_to_play = player_input
                    print("player play card: ",card_to_play)
                    # game_manager.card_play_manager.PlayCard(card_to_play)
                    # TODO remove it when energy is calculated by Play
                    game_manager.game_state.player_energy -= 1
                
            if is_AI_mode:
                pass
                # TODO RL_AI.calculate_reward(game_state,)

        # enemy turn
        game_manager.start_enemy_turn()
        # check is player killed all enemies
        if game_manager.is_game_end():
            break
        # apply BOSS intent
        game_manager.execute_enemy_intent()

    if game_manager.is_player_win():
        print("result:---------------------\nWin")
    else:
        print("result:---------------------\nlost")

run_game(False)