from db.game_app_data import GameAppData
from .combat_unit import CombatUnit
from .enemy_AI import EnemyAI
from .deck import Deck
from .enemy_intent import EnemyIntent

PLAYER_ENERGY = 3
class GameState:
    def __init__(self,game_app_data:GameAppData):
        rules = game_app_data.rules
        all_buffnames = game_app_data.registered_buffnames
        self.game_stage = "PlayerTurn"# can be 'PlayerTurn'/'EnemyTurn'/'Win'/'Lost'
        self.player = CombatUnit('Player', "player",rules['player_hp'], all_buffnames) 
        self.boss = CombatUnit('The Guardian',"boss", rules['boss_hp'], all_buffnames) 
        # TODO: EnemyAI is not pure data, it is an object with methods.which against the concept of game state
        self.boss_AI = EnemyAI(self.boss)
        self.player_energy = PLAYER_ENERGY
        self.boss_intent = EnemyIntent()
        self.cards_dict = game_app_data.cards_dict.copy()# cardname:str , card:game_app_data.Card
        self.deck = Deck(game_app_data.deck_config)
