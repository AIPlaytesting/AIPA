from gameplay.game_state import GameState

# things a customize keywords/buff can do
class ActionSpace:
    def do_damage_to(self):
        pass

    def change_block_value(self):
        pass

    def play_card(self):
        pass

    def draw_card(self):
        pass

    def exhaust_card(self):
        pass