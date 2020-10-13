import json

from game_manager import GameState
from combat_unit import CombatUnit
from db.game_app_data import Card
from db.game_database import calculate_resouces_dir
from CardPlayManager import CardPlayManager
from game_event import GameEvent

# The naming style is C#, becuase the name of class need to be the same as 
# front end in Unity 

INPUT_TYPE_NONE = 0
INPUT_TYPE_PLAY_CARD = 1
INPUT_TYPE_END_TURN = 2
INPUT_TYPE_START_GAME = 3

MESSAGE_TYPE_NONE = 0 # content is invalid message
MESSAGE_TYPE_GAME_SEQUENCE = 1 # contetnt is the json string of GameSequenceMarkup
MESSAGE_TYPE_ERROR = 2 # content is the string of error message
MESSAGE_TYPE_GAMESTAGE_CHANGE = 3 # content is string (can parsed to enum of GameStage)

GAMESTAGE_PLAYER_TURN = 'PlayerTurn'
GAMESTAGE_ENEMY_TURN = 'EnemyTurn'
GAMESTAGE_WIN = 'Win'
GAMESTAGE_LOST = 'Lost'

class ResponseMessage:
    def __init__(self,content_type,content):
        self.content_type = content_type
        self.content = content
    
    def to_json(self):
        json_obj = {'contentType':self.content_type,'content':self.content}
        return json.dumps(json_obj)

class UserInput:
    def __init__(self,type,card_name,card_guid):
        self.type = type
        self.cardName = card_name
        self.cardGUID = card_guid

class MarkupFactory:
    @classmethod
    def create_game_sequence_markup_file(cls,beginingState,gameEvents, endingState):
        markup = {}
        markup['beginingState'] = beginingState
        markup['gameEvents'] = [cls.create_game_event_markup(e) for e in gameEvents]
        markup['endingState'] = endingState
        return markup

    @classmethod
    def create_game_event_markup(cls,game_event:GameEvent):
        if game_event == None:
            print("[ERROR]: gameEvent is none!")
            return {}

        markup = {}
        markup['eventChannel'] = game_event.event_channel
        markup['cardEvent'] = game_event.card_event_type
        markup['combatUnitEvent'] = game_event.combat_unit_event_type
        markup['information'] = game_event.information
        return markup

    @classmethod
    def enrich_game_state_markup_with_RLinfo(cls,game_state_markup,rlbot):
        game_state_markup['rlRewardValues'] = [reward for reward in rlbot.get_rewards()]       

    @classmethod
    def create_game_state_markup(cls,game_state:GameState):
        def create_cards_markup_by_card_instances(card_instances):
            card_markups = []
            for card_instance in card_instances:
                card = game_state.cards_dict[card_instance.card_name]
                card_markups.append(cls.create_card_markup(card,card_instance.game_unique_id))
            return card_markups

        markup ={}
        markup['player'] = cls.create_combat_unit_markup(game_state.player)
        boss_markup = cls.create_combat_unit_markup(game_state.boss)
        cls.add_boss_AI_inforamtion(boss_markup,game_state)
        markup['enemies'] = [boss_markup]
        markup['enemyIntents'] = [cls.create_enemy_intent_markup(game_state.boss_intent)]
        markup['cardsOnHand'] = create_cards_markup_by_card_instances(game_state.deck.get_card_instances_on_hand())
        markup['drawPile'] = create_cards_markup_by_card_instances(game_state.deck.get_draw_pile().cards)
        markup['discardPile'] = create_cards_markup_by_card_instances(game_state.deck.get_discard_pile().cards)
        markup['energy'] = cls.create_value_markup('energy',game_state.player_energy,3)
        markup['guadianModeValue'] = cls.create_value_markup(
            'guadianModeValue',
            game_state.boss_AI.accumulator,
            game_state.boss_AI.transformTriggerPoint)
        return markup

    @classmethod
    def create_combat_unit_markup(cls,combat_unit:CombatUnit):
        markup = {}

        markup['name'] = combat_unit.name
        markup['currentHP'] = combat_unit.current_hp
        markup['maxHP'] = combat_unit.max_hP
        markup['block'] = combat_unit.block
        markup['gameUniqueID'] = combat_unit.game_unique_id
        markup['buffs'] = []
        # must be <str,str> dict
        markup['information'] = {}
        for buff_name,buff_value in combat_unit.buff_dict.items():
            if buff_value != 0:
                markup['buffs'].append({"buffName":buff_name,"buffValue":buff_value})

        return markup
    
    @classmethod
    def add_boss_AI_inforamtion(cls,combat_unit_markup,game_state:GameState):
        combat_unit_markup['information']['mode'] = game_state.boss_AI.mode

    @classmethod
    def create_card_markup( cls,card:Card,game_unique_id:str):
        markup = {}
        markup['gameUniqueID'] = game_unique_id
        markup['name'] = card.name
        markup['energyCost'] = card.energy_cost
        markup['description'] = card.description
        resource_dir = calculate_resouces_dir()
        markup['imgAbsPath'] = resource_dir +'\\'+ card.img_relative_path
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
    