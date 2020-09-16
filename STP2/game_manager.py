from combat_unit import CombatUnit
from enemy_intent import EnemyIntent
from enemy_AI import EnemyAI
from deck import Deck
import CardPlayManager

PLAYER_ENERGY = 3
class GameState:
    def __init__(self, empty_buff_dict):
        self.player = CombatUnit(100, empty_buff_dict) # placehold: hp value all 100
        self.boss = CombatUnit(100, empty_buff_dict) # placehold: hp value all 100
        self.player_energy = PLAYER_ENERGY
        self.boss_intent = EnemyIntent()
        self.deck = Deck()

class GameManager:
    def __init__(self):
        self.card_play_manager = CardPlayManager.CardPlayManager(self)
        self.game_state = GameState(self.card_play_manager.GetEmptyBuffDict())
        self.boss_AI = EnemyAI()

    def init_game(self):
        self.game_state = GameState(self.card_play_manager.GetEmptyBuffDict())

    def is_game_end(self):
        player_hp, boss_hp = self.game_state.player.current_hp,self.game_state.boss.current_hp
        print("player HP:", player_hp," boss HP: ",boss_hp)
        return player_hp <= 0 or boss_hp < 0

    def is_player_win(self):
        boss_hp = self.game_state.boss.current_hp
        return boss_hp <= 0
        
    def start_player_turn(self):
        print("start player turn ===========================")
        # refresh energy
        self.game_state.player_energy = PLAYER_ENERGY
        # refresh boss intent
        self.game_state.boss_intent = self.boss_AI.make_intent()
        # draw cards
        self.game_state.deck.draw_cards(5)
        # TODO -refresh buffs

    def start_enemy_turn(self):
        print("start enemy turn *****************************")
        self.game_state.deck.discard_all_cards()

    def get_current_playable_cards(self):
        return self.game_state.deck.get_card_names_on_hand()

    def execute_enemy_intent(self):
        self.game_state.boss_intent.apply_to(self.game_state)
