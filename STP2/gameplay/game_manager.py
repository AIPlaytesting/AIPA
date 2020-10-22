from db.game_app_data import GameAppData

from .combat_unit import CombatUnit
from .enemy_intent import EnemyIntent
from .enemy_AI import EnemyAI
from .game_event import GameEvent
from .deck import Deck
from .game_state import GameState
from .event_system import EventManager

PLAYER_ENERGY = 3

# fucntions marked as "game flow func"
# it will change the game state, and always return GameEvent or GameEvent[]

# gameflow MUST follow is: 
# ->start_player_turn()
# ->execute_play_card()->execute_play_card()->execute_play_card()....
# ->start_enemy_turn()
# ->execute_enemy_intent()

class GameManager:
    def __init__(self,game_app_data:GameAppData):
        self.game_app_data = game_app_data
        self.event_manager = EventManager(self.game_app_data)
        self.game_state = GameState(game_app_data)
        # TODO:deprecate
        self.__end_player_turn_flag = False

        #set to false when training AI
        self.isLoggingEnabled = True

    def init_game(self):
        self.game_state = GameState(self.game_app_data)

    def is_game_end(self):
        player_hp, boss_hp = self.game_state.player.current_hp,self.game_state.boss.current_hp
        print("player HP:", player_hp," boss HP: ",boss_hp)
        return player_hp <= 0 or boss_hp < 0

    def is_player_win(self):
        boss_hp = self.game_state.boss.current_hp
        return boss_hp <= 0

    def is_player_finish_turn(self):
        return self.__end_player_turn_flag
    
    # game flow func
    # return start player turn GameEvent
    def start_player_turn(self)->GameEvent:
        print("start player turn ===========================")
        if not self.is_game_end():
            self.game_state.game_stage = 'PlayerTurn'
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
        return GameEvent.create_new_turn_event(True)

    # game flow func
    # (TODO: depricated, we don't need to maintain this flag since we have GameState.game_stage)
    def end_player_turn(self):
        self.__end_player_turn_flag = True
   
    # game flow func   
    # return start enemy turn GameEvent
    def start_enemy_turn(self)->GameEvent:
        print("start enemy turn *****************************")
        if not self.is_game_end():
            self.game_state.game_stage = 'EnemyTurn'
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
        return GameEvent.create_new_turn_event(False)

    # game flow func
    # return: game_event.GameEvent[]
    def execute_enemy_intent(self):
        game_events = []
        # create-intent event
        game_events.append(GameEvent.create_enemy_intent_event(self.game_state.boss.game_unique_id))
        # execut intent and get events
        intent_execte_events = self.event_manager.execute_enemy_intent(self.game_state)
        game_events.extend(intent_execte_events)
        # check if game is ended
        if self.is_game_end():
            self.game_state.game_stage = 'Win' if self.is_player_win() else 'Lost'
        return game_events
   
    # game flow func
    # return: game_event.GameEvent[]
    def execute_play_card(self, cardname):
        game_events = self.event_manager.execute_card(self.game_state,cardname)
        if self.is_game_end():
            self.game_state.game_stage = 'Win' if self.is_player_win() else 'Lost'
        return game_events

    # return the list of card names
    def get_current_playable_cards(self):
        playable_cards = []

        for card_name in self.game_state.deck.get_card_names_on_hand():
            if card_name in self.game_app_data.cards_dict:
                card = self.game_app_data.cards_dict[card_name]
                if card.energy_cost <= self.game_state.player_energy:
                    playable_cards.append(card_name)
            else:
                print("[ERROR]-GameManager.get_current_playable_cards(): ",card_name," is not in card_dict")
        
        return playable_cards

    def get_current_cards_on_hand(self):
        return self.game_state.deck.get_card_names_on_hand()

    
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
