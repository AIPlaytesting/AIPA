class RLBot:
    def __init__(self,game_manager):
        self.game_manager = game_manager

    def get_rewards(self):
        result = []
        for i in range(5):
            reward = {'cardname':"card",'reward':i/10}
            result.append(reward)
        return result