from combat_unit import CombatUnit
from enemy_intent import EnemyIntent
from enemy_AI import EnemyAI
PLAYER_ENERGY = 3
class GameState:
    def __init__(self):
        self.player = CombatUnit(100) # placehold: hp value all 100
        self.boss = CombatUnit(100) # placehold: hp value all 100
        self.player_energy = PLAYER_ENERGY
        self.boss_intent = EnemyIntent()
        # self.deck = Deck()

class GameManager:
    def __init__(self):
        self.game_state = GameState()
        self.boss_AI = EnemyAI()

    def init_game(self):
        self.game_state = GameState()

    def is_game_end(self):
        player_hp, boss_hp = self.game_state.player.current_hp,self.game_state.boss.current_hp
        print("player HP:", player_hp," boss HP: ",boss_hp)
        return player_hp <= 0 or boss_hp < 0

    def is_player_win(self):
        boss_hp = self.game_state.boss.current_hp
        return boss_hp <= 0
        
    def start_turn(self):
        print("start turn ===========================")
        # refresh energy
        self.game_state.player_energy = PLAYER_ENERGY
        # refresh boss intent
        self.game_state.boss_intent = self.boss_AI.make_intent()
        # refresh buffs

    def get_player_action_space(self):
        return ["card1","card2","card3","card4","card5"]

    def execute_enemy_intent(self):
        self.game_state.boss_intent.apply_to(self.game_state)
