from STP2.combat_unit import CombatUnit
from STP2.enemy_intent import EnemyIntent
class GameState:
    def __init__(self):
        self.player = CombatUnit(100) # placehold: hp value all 100
        self.boss = CombatUnit(100) # placehold: hp value all 100
        self.currentBossIntent = EnemyIntent()
        # self.deck = Deck()

class GameManager:
    def __init__(self):
        self.gameState = GameState()

    def init_game(self):
        gameManager.gameState = GameState()

    def is_game_end(self):
        return self.gameState.player.currentHP <= 0 or self.gameState.boss.currentHP < 0

    def start_turn(self):
        pass

    def get_player_action_space(self):
        pass

    def execute_enemy_intent(self):
        pass

gameManager = GameManager()