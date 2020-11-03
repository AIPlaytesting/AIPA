import AI_Module.AI_Transformer
import AI_Module.AI_Player_v1
from gameplay.game_manager import GameManager
from gameplay.enemy_intent import EnemyIntent
import db.game_database

# load game database
db_root = db.game_database.calculate_root_dir()
game_db = db.game_database.GameDatabase(db_root)
game_db.print_data_to_terminal()

# init 
game_manager = GameManager(game_db.game_app_data)
game_manager.init_game()

ai_player = AI_Module.AI_Player_v1.AI_Player(game_manager)

# game_manager.print_data_to_terminal()
vec = ai_player.GetActionVector()
print("vec",vec)
actions = ai_player.action_space
print("key------------------------")
for action in actions:
    print(actions[action])
    print(vec[0][action])

