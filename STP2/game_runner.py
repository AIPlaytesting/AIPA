from STP2.game_manager import GameManager

game_manager = GameManager()
game_manager.init_game()
while(not game_manager.is_game_end()):
    # init for game start
    game_manager.start_turn()
    # generate action space
    action_space = game_manager.get_player_action_space()
    # wait for player input

    # apply player action

    # apply BOSS intent
    game_manager.execute_enemy_intent()