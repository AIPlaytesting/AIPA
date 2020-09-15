from combatUnit import CombatUnit

class GameState:
    def __init__(self):
        # placehold: hp value all 100
        self.player = CombatUnit(100)
        self.boss = CombatUnit(100)
        # self.deck = Deck()

class GameManager:
    def __init__(self):
        self.gameState = GameState()

def init_game():
    gameManager.gameState = GameState()

gameManager = GameManager()