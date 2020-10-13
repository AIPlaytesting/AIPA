class RLBot:
    def __init__(self,game_manager):
        self.game_manager = game_manager

    def get_rewards(self):
        return [x for x in range(10)]