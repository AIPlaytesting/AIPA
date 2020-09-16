from game_manager import GameManager

game_manager = GameManager()
game_manager.init_game()
while(not game_manager.is_game_end()):
    # player turn
    game_manager.start_player_turn()
    # generate action space
    action_space = game_manager.get_player_action_space()
    print("action space: ",action_space)
    # wait for player input
    print("wait player input: none")
    # apply player action
    print("apply action: none")

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