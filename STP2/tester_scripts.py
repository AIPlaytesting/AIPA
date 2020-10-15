import AI_Module.AI_Transformer
import AI_Module.AI_Player_v1
import game_manager
from game_manager import GameManager
from enemy_intent import EnemyIntent
import db.game_database


# ai_t = AI_Module.AI_Transformer.AI_Transformer()

# ai_t.PrintStateActionDef()


# load game data based 
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

print(np.argmax(vec[0]))

print("reward------------------------")
for reward in vec[0]:
    print(reward)