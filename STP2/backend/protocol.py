import json

from gameplay.game_manager import GameState
from gameplay.combat_unit import CombatUnit
from gameplay.game_event import GameEvent

from db.game_app_data import Card
from db.game_database import calculate_resouces_dir

# The naming style is C#, becuase the name of class need to be the same as 
# front end in Unity 

INPUT_TYPE_NONE = 0
INPUT_TYPE_PLAY_CARD = 1
INPUT_TYPE_END_TURN = 2
INPUT_TYPE_START_GAME = 3

MESSAGE_TYPE_NONE = 0 # content is invalid message
MESSAGE_TYPE_GAME_SEQUENCE = 1 # contetnt is the json string of GameSequenceMarkup
MESSAGE_TYPE_ERROR = 2 # content is the string of error message
MESSAGE_TYPE_DBQUERY = 3 # content is the string of error message

class DBQuery:
    def __init__(self,query_id:int,query_santence:str):
        self.query_id = query_id 
        self.query_sentence = query_santence

class PlayerStep:
    def __init__(self,type,card_name,card_guid):
        self.type = type # type can be 'PlayCard' or 'EndTurn'
        self.cardName = card_name
        self.cardGUID = card_guid


# each method has its own field,
# for example, method 'UserInput' has its inforamtion stored in field 'self.user_input'
class RequestMessage:
    def __init__(self,method,player_step:PlayerStep,db_query:DBQuery):
        self.method = method # method can be: 'ResetGame'/'PlayerStep'/'DBQuery'/'None'
        self.player_step = player_step # PlayerStep
        self.db_query = db_query

    @classmethod
    def create_request_message_from(cls,request_dict:dict):
        method = request_dict['method']
        if method  == 'PlayerStep':
            player_step_dict = request_dict['playerStep']
            player_step = PlayerStep(
                player_step_dict['type'],
                player_step_dict['cardName'],
                player_step_dict['cardGUID'])
            return RequestMessage(method,player_step,"")
        elif method == 'DBQuery':
            dbquery_dict = request_dict['dbQuery']
            dbquery = DBQuery(dbquery_dict['queryID'],dbquery_dict['querySentence'])
            return RequestMessage(method,None,dbquery)
        elif method == 'ResetGame':
            return RequestMessage(method,None,"")
        else:
            print("undefined method: ",method)
            return None

class ResponseMessage:
    def __init__(self,content_type,content):
        self.content_type = content_type # content type is const start with MESSAGE_TYPE_xxxx
        self.content = content
    
    @classmethod
    def cretate_dbquery_result_response(cls,query_id:int,query_reuslt:str):
        content_type = MESSAGE_TYPE_DBQUERY
        content_dict = {"queryID":query_id,"queryResult":query_reuslt}
        content_json = json.dumps(content_dict)
        response = ResponseMessage(content_type,content_json)
        return response

    @classmethod
    def create_game_sequence_response(cls,gamesequence_markup:dict):
        content_type = MESSAGE_TYPE_GAME_SEQUENCE
        game_sequence_markup_json = json.dumps(gamesequence_markup)
        response = ResponseMessage(content_type,game_sequence_markup_json)
        return response

    @classmethod
    def create_error_message_response(cls,error_message:str):
        return ResponseMessage(MESSAGE_TYPE_ERROR,error_message)

    def to_json(self):
        json_obj = {'contentType':self.content_type,'content':self.content}
        return json.dumps(json_obj)

class MarkupFactory:
    @classmethod
    def create_game_sequence_markup_file(cls,begining_state_markup:dict,gameEvents, ending_state_markup:dict):
        markup = {}
        markup['beginingState'] = begining_state_markup
        markup['gameEvents'] = [cls.create_game_event_markup(e) for e in gameEvents]
        markup['endingState'] = ending_state_markup
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
        game_state_markup['rlRewardValues'] = []      
        for reward in rlbot.get_rewards():
            rewardvalue_markup  = cls.create_value_markup(
                reward['cardname'],
                reward['reward'],
                reward['reward'],
                'rlreward')
            game_state_markup['rlRewardValues'].append(rewardvalue_markup)

    @classmethod
    def create_game_state_markup(cls,game_state:GameState):
        def create_cards_markup_by_card_instances(card_instances):
            card_markups = []
            for card_instance in card_instances:
                card = game_state.cards_dict[card_instance.card_name]
                card_markups.append(cls.create_card_markup(card,card_instance.game_unique_id))
            return card_markups

        markup ={}
        markup['gameStage'] = game_state.game_stage
        markup['player'] = cls.create_combat_unit_markup(game_state.player)
        boss_markup = cls.create_combat_unit_markup(game_state.boss)
        cls.add_boss_AI_inforamtion(boss_markup,game_state)
        markup['enemies'] = [boss_markup]
        markup['enemyIntents'] = [cls.create_enemy_intent_markup(game_state.boss_intent)]
        markup['cardsOnHand'] = create_cards_markup_by_card_instances(game_state.deck.get_card_instances_on_hand())
        markup['drawPile'] = create_cards_markup_by_card_instances(game_state.deck.get_draw_pile().cards)
        markup['discardPile'] = create_cards_markup_by_card_instances(game_state.deck.get_discard_pile().cards)
        markup['energy'] = cls.create_value_markup('energy',game_state.player_energy,3,'energy')
        markup['guadianModeValue'] = cls.create_value_markup(
            'guadianModeValue',
            game_state.boss_AI.accumulator,
            game_state.boss_AI.transformTriggerPoint,
            'guadian')
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
    def create_value_markup(cls,value_name,cur_value,max_value,renderclass):
        markup = {}
        markup['name'] = value_name
        markup['curValue'] = cur_value
        markup['maxValue'] = max_value
        markup['renderClass'] = renderclass
        return markup

    @classmethod
    def create_enemy_intent_markup(cls,enemy_intent):
        markup = vars(enemy_intent)
        return markup
    