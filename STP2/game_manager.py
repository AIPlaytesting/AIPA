from combat_unit import CombatUnit
from enemy_intent import EnemyIntent
from enemy_AI import EnemyAI
from deck import Deck
import CardPlayManager

PLAYER_ENERGY = 3
class GameState:
    def __init__(self, empty_buff_dict,all_card_names):
        self.player = CombatUnit(100, empty_buff_dict) # placehold: hp value all 100
        self.boss = CombatUnit(100, empty_buff_dict) # placehold: hp value all 100
        self.player_energy = PLAYER_ENERGY
        self.boss_intent = EnemyIntent()
        self.deck = Deck(all_card_names)

class GameManager:
    def __init__(self):
        self.card_play_manager = CardPlayManager.CardPlayManager(self)
        self.game_state = GameState(self.card_play_manager.GetEmptyBuffDict(),self.card_play_manager.cards_dict.keys())
        self.boss_AI = EnemyAI(self.game_state.boss)
        self.__end_player_turn_flag = False

    def init_game(self):
        self.game_state = GameState(self.card_play_manager.GetEmptyBuffDict(),self.card_play_manager.cards_dict.keys())
        self.boss_AI = EnemyAI(self.game_state.boss)

    def is_game_end(self):
        player_hp, boss_hp = self.game_state.player.current_hp,self.game_state.boss.current_hp
        print("player HP:", player_hp," boss HP: ",boss_hp)
        return player_hp <= 0 or boss_hp < 0

    def is_player_win(self):
        boss_hp = self.game_state.boss.current_hp
        return boss_hp <= 0

    def is_player_finish_turn(self):
        return self.__end_player_turn_flag

    def start_player_turn(self):
        print("start player turn ===========================")
        # refresh block
        self.game_state.player.block = 0
        # refresh flag
        self.__end_player_turn_flag = False
        # refresh energy
        self.game_state.player_energy = PLAYER_ENERGY
        # refresh boss intent
        self.game_state.boss_intent = self.boss_AI.make_intent()
        # draw cards
        self.game_state.deck.draw_cards(5)
        # refresh buffs
        self.game_state.player.refresh_buff_on_new_turn()

    def end_player_turn(self):
        self.__end_player_turn_flag = True

    def start_enemy_turn(self):
        print("start enemy turn *****************************")
        # refresh block
        self.game_state.boss.block = 0
        # call back for AI
        self.boss_AI.onEnemyTurnStart()
        # discard player cards on hand
        self.game_state.deck.discard_all_cards()
        # refresh boss buffs
        self.game_state.boss.refresh_buff_on_new_turn()

    # return the list of card names
    def get_current_playable_cards(self):
        playable_cards = []

        for card_name in self.game_state.deck.get_card_names_on_hand():
            if card_name in self.card_play_manager.cards_dict:
                card = self.card_play_manager.cards_dict[card_name]
                if card.energy_cost <= self.game_state.player_energy:
                    playable_cards.append(card_name)
            else:
                print("[ERROR]-GameManager.get_current_playable_cards(): ",card_name," is not in card_dict")
        
        return playable_cards

    def execute_enemy_intent(self):
        self.game_state.boss_intent.apply_to(self.game_state)
