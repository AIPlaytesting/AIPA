import AI_Module.AI_Transformer
import AI_Module.AI_Player_v1
import db.game_database
from gameplay.game_manager import GameManager

class RLBot:
    def __init__(self,game_manager):
        self.game_manager = game_manager
        self.ai_player = AI_Module.AI_Player_v1.AI_Player(game_manager)

    def get_rewards(self):
        result = []
        vec = self.ai_player.GetActionVector()
        actions = self.ai_player.action_space
        for action in actions:
            print(actions[action])
            print(vec[0][action])
            reward = {'cardname':actions[action],'reward':float(vec[0][action])}
            result.append(reward)
        return result

# # load game database
# db_root = db.game_database.calculate_root_dir()
# game_db = db.game_database.GameDatabase(db_root)
# game_db.print_data_to_terminal()

# # init 
# game_manager = GameManager(game_db.game_app_data)

# rlbot = RLBot(game_manager)
# print(rlbot.get_rewards())