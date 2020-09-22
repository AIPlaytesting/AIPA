from combat_unit import CombatUnit
from enemy_intent import EnemyIntent
from enemy_AI import EnemyAI
from deck import Deck
import CardPlayManager
import EffectCalculator

PLAYER_ENERGY = 3
class GameState:
    def __init__(self, empty_buff_dict,all_card_names):
        self.player = CombatUnit('Player', 100, empty_buff_dict) # placehold: hp value all 100
        self.boss = CombatUnit('The Guardian', 100, empty_buff_dict) # placehold: hp value all 100
        self.player_energy = PLAYER_ENERGY
        self.boss_intent = EnemyIntent()
        self.deck = Deck(all_card_names)

class GameManager:
    def __init__(self):
        self.effect_calculator = EffectCalculator.EffectCalculator(self)
        self.card_play_manager = CardPlayManager.CardPlayManager(self, self.effect_calculator)
        self.game_state = GameState(self.card_play_manager.GetEmptyBuffDict(), self.card_play_manager.cards_dict.keys())
        self.boss_AI = EnemyAI(self.game_state.boss)
        self.__end_player_turn_flag = False

        #set to false when training AI
        self.isLoggingEnabled = True

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
        # log player status
        self.game_state.player.print_status_info("Player")

    def end_player_turn(self):
        self.__end_player_turn_flag = True
        
    def start_enemy_turn(self):
        print("start enemy turn *****************************")
        # refresh block
        self.game_state.boss.block = 0
        # call back for AI
        self.boss_AI.onEnemyTurnStart(self.game_state)
        # discard player cards on hand
        self.game_state.deck.discard_all_cards()
        # refresh boss buffs
        self.game_state.boss.refresh_buff_on_new_turn()
        # log status
        self.game_state.boss.print_status_info("BOSS")

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

    def get_current_cards_on_hand(self):
        return self.game_state.deck.get_card_names_on_hand()

    def execute_enemy_intent(self):
        self.game_state.boss_intent.apply_to(self.game_state,self.effect_calculator)

    def print_cards_info_on_hand(self):
        cards_on_hand = self.get_current_cards_on_hand()
        playable_cards = self.get_current_playable_cards()
        cards_info = []
        for i,card in enumerate(cards_on_hand):
            if card in playable_cards:
                cards_info.append(str(i)+'-'+"("+card+")")
            else:
                cards_info.append(card)
        print("cards on hand: ", cards_info)
