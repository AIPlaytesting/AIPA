from game_manager import GameManager

game_manager = GameManager()
game_manager.init_game()
while(not game_manager.is_game_end()):
    # init for game start
    game_manager.start_turn()
    # generate action space
    action_space = game_manager.get_player_action_space()
    print("action space: ",action_space)
    # wait for player input
    print("wait player input: none")
    # apply player action
    print("apply action: none")

    # check is player killed all enemies
    if game_manager.is_game_end():
        break
    else:
        # apply BOSS intent
        game_manager.execute_enemy_intent()

if game_manager.is_player_win():
    print("result:---------------------\nWin")
else:
    print("result:---------------------\nlost")