from game_manager import GameState
from combat_unit import CombatUnit
from CardBase import Card
from CardPlayManager import CardPlayManager
from game_event import GameEvent

INPUT_TYPE_NONE = 0
INPUT_TYPE_PLAY_CARD = 1
INPUT_TYPE_END_TURN = 2
INPUT_TYPE_START_GAME = 3
# The naming style is C#, becuase the name of class need to be the same as 
# front end in Unity 
class UserInput:
    def __init__(self,type,card_name):
        self.type = type
        self.cardName = card_name

class MarkupFactory:
    @classmethod
    def create_game_sequence_markup_file(cls,beginingState,gameEvents, endingState):
        markup = {}
        markup['beginingState'] = beginingState
        markup['gameEvents'] = gameEvents
        markup['endingState'] = endingState
        return markup

    @classmethod
    def create_game_event_markup(cls,game_event:GameEvent):
        markup = {}
        markup['eventChannel'] = game_event.event_channel
        markup['cardEventType'] = game_event.card_event_type
        markup['characterEventType'] = game_event.character_event_type
        markup['inforamtion'] = game_event.inforamtion
        return markup
        
    @classmethod
    def create_game_state_markup(cls,game_state:GameState,card_play_manager:CardPlayManager):
        def create_cards_markup_by_names(names):
            card_markups = []
            for card_name in names:
                card = card_play_manager.cards_dict[card_name]
                card_markups.append(cls.create_card_markup(card))
            return card_markups

        markup ={}
        markup['player'] = cls.create_combat_unit_markup(game_state.player)
        markup['enemies'] = [cls.create_combat_unit_markup(game_state.boss)]
        markup['enemyIntents'] = [cls.create_enemy_intent_markup(game_state.boss_intent)]
        markup['cardsOnHand'] = create_cards_markup_by_names(game_state.deck.get_card_names_on_hand())
        markup['drawPile'] = create_cards_markup_by_names(game_state.deck.getDrawPile().cards)
        markup['discardPile'] = create_cards_markup_by_names(game_state.deck.getDiscardPile().cards)
        markup['energy'] = cls.create_value_markup('energy',game_state.player_energy,3)
        return markup

    @classmethod
    def create_combat_unit_markup(cls,combat_unit:CombatUnit):
        markup = {}
        markup['name'] = combat_unit.name
        markup['currentHP'] = combat_unit.current_hp
        markup['maxHP'] = combat_unit.max_hP
        markup['block'] = combat_unit.block
        markup['buffs'] = []
        for buff_name,buff_value in combat_unit.buff_dict.items():
            if buff_value != 0:
                markup['buffs'].append({"buffName":buff_name,"buffValue":buff_value})

        return markup

    @classmethod
    def create_card_markup( cls,card:Card):
        markup = {}
        markup['name'] = card.name
        markup['energyCost'] = card.energy_cost
        return markup

    @classmethod
    def create_value_markup(cls,value_name,cur_value,max_value):
        markup = {}
        markup['name'] = value_name
        markup['curValue'] = cur_value
        markup['maxValue'] = max_value
        return markup
    @classmethod
    def create_enemy_intent_markup(cls,enemy_intent):
        markup = vars(enemy_intent)
        return markup
                
class GameStateMarkup:
    # TODO: card information should get from data in disk
    def __init__(self,game_state:GameState,card_play_manager:CardPlayManager):
        self.player = CombatUnitMarkup(game_state.player)
        self.enimes = [CombatUnitMarkup(game_state.boss)]

        self.cardsOnHand = []
        for card_name in game_state.deck.get_card_names_on_hand():
            card = card_play_manager.cards_dict[card_name]
            self.cardsOnHand.append(CardMarkup(card))

        self.drawPile = []
        self.discardPile = []
        self.energy = []

