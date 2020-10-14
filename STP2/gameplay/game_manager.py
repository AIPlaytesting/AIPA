from .combat_unit import CombatUnit
from .enemy_intent import EnemyIntent
from .enemy_AI import EnemyAI
from .game_event import GameEvent
from .deck import Deck
from db.game_app_data import GameAppData
from . import CardPlayManager
from . import EffectCalculator

PLAYER_ENERGY = 3
class GameState:
    def __init__(self,game_app_data:GameAppData,all_card_names):
        rules = game_app_data.rules
        all_buffnames = game_app_data.registered_buffnames
        self.player = CombatUnit('Player', "player",rules['player_hp'], all_buffnames) 
        self.boss = CombatUnit('The Guardian',"boss", rules['boss_hp'], all_buffnames) 
        # TODO: EnemyAI is not pure data, it is an object with methods.which against the concept of game state
        self.boss_AI = EnemyAI(self.boss)
        self.player_energy = PLAYER_ENERGY
        self.boss_intent = EnemyIntent()
        self.cards_dict = game_app_data.cards_dict.copy()# cardname:str , card:game_app_data.Card
        self.deck = Deck(game_app_data.deck_config)

class GameManager:
    def __init__(self,game_app_data:GameAppData):
        self.game_app_data = game_app_data
        self.effect_calculator = EffectCalculator.EffectCalculator(self)
        self.card_play_manager = CardPlayManager.CardPlayManager(self, self.effect_calculator)
        self.game_state = GameState(game_app_data,self.card_play_manager.cards_dict.keys())
        self.__end_player_turn_flag = False

        #set to false when training AI
        self.isLoggingEnabled = True

    def init_game(self):
        self.game_state = GameState(self.game_app_data,self.card_play_manager.cards_dict.keys())

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
        self.game_state.boss_intent = self.game_state.boss_AI.make_intent()
        # draw cards
        self.game_state.deck.draw_cards(5)
        # refresh buffs
        self.game_state.player.refresh_buff_on_new_turn()
        # log player status
        self.game_state.player.print_status_info("Player")
        if self.game_state.boss_AI.mode == "Offensive":
            print("Boss will switch mode in", self.game_state.boss_AI.transformTriggerPoint - self.game_state.boss_AI.accumulator, "damages")

    def end_player_turn(self):
        self.__end_player_turn_flag = True
        
    def start_enemy_turn(self):
        print("start enemy turn *****************************")
        # refresh block
        self.game_state.boss.block = 0
        # call back for AI
        self.game_state.boss_AI.onEnemyTurnStart(self.game_state)
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

    # return: game_event.GameEvent[]
    def execute_enemy_intent(self):
        game_events = []
        game_events.append(GameEvent.create_enemy_intent_event(self.game_state.boss.game_unique_id))
        intent_execte_events = self.game_state.boss_intent.apply_to(self.game_state,self.effect_calculator)
        game_events.extend(intent_execte_events)
        return game_events

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
