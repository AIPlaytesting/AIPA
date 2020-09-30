# keys in information dict
TURN_NAME_KEY = "turnName"
CARD_GUID_KEY = "cardGUID"
COMBAT_UNIT_GUID_KEY = "combatUnitGUID"
BUFF_NAME_KEY = "buffName"
HURT_VALUE_KEY = "hurtValue"
NEW_BLOCK_VALUE_KEY = "newBlockValue"
NEW_BUFF_VALUE_KEY = "newBuffValue"

# event channel enum
EVENTCHANNLE_NONE = 0
EVENTCHANNLE_NEW_TURN = 1
EVENTCHANNLE_CARD = 2
EVENTCHANNLE_COMBAT_UNIT = 3

# card event type nume
CARD_EVENT_NONE = 0
CARD_EVENT_PLAYED = 1
CARD_EVENT_DRAW = 2

# character event type nume
COMBAT_UNIT_EVENT_NONE = 0
COMBAT_UNIT_EVENT_GETHURT = 1
COMBAT_UNIT_EVENT_BLOCKCHANGE = 2
COMBAT_UNIT_EVENT_BUFFCHANGE = 3

class GameEvent:
    def __init__(self,event_channel,card_event_type,combat_unit_event_type,information:dict):
        self.event_channel = event_channel
        self.card_event_type = card_event_type
        self.combat_unit_event_type = combat_unit_event_type
        self.information = information
    
    @classmethod
    def create_play_card_event(cls,card_game_unique_id:str):
        event_channel = EVENTCHANNLE_CARD
        card_event_type = CARD_EVENT_PLAYED
        combat_unit_event_type = COMBAT_UNIT_EVENT_NONE
        information ={CARD_GUID_KEY:card_game_unique_id}
        return GameEvent(
            event_channel,
            card_event_type, 
            combat_unit_event_type,
            information)

    @classmethod
    def create_draw_card_event(cls,card_game_unique_id:str):
        event_channel = EVENTCHANNLE_CARD
        card_event_type = CARD_EVENT_DRAW
        combat_unit_event_type = COMBAT_UNIT_EVENT_NONE
        information ={CARD_GUID_KEY:card_game_unique_id}
        return GameEvent(
            event_channel,
            card_event_type, 
            combat_unit_event_type,
            information)

    @classmethod
    def create_get_hurt_event(cls,combat_unit_game_unique_id:str,hurt_value:int):
        event_channel = EVENTCHANNLE_COMBAT_UNIT
        card_event_type = CARD_EVENT_NONE
        combat_unit_event_type = COMBAT_UNIT_EVENT_GETHURT
        information ={
            COMBAT_UNIT_GUID_KEY:combat_unit_game_unique_id,
            HURT_VALUE_KEY:str(hurt_value)}
        return GameEvent(
            event_channel,
            card_event_type, 
            combat_unit_event_type,
            information)

    @classmethod
    def create_buff_change_event(cls,combat_unit_game_unique_id:str, buff_name:str,new_value:int):
        event_channel = EVENTCHANNLE_COMBAT_UNIT
        card_event_type = CARD_EVENT_NONE
        combat_unit_event_type = COMBAT_UNIT_EVENT_BUFFCHANGE
        information ={
            COMBAT_UNIT_GUID_KEY:combat_unit_game_unique_id,
            BUFF_NAME_KEY:buff_name,
            NEW_BUFF_VALUE_KEY:str(new_value)}
        return GameEvent(
            event_channel,
            card_event_type, 
            combat_unit_event_type,
            information)

    @classmethod
    def create_block_change_event(cls,combat_unit_game_unique_id:str, new_block_value:int):
        event_channel = EVENTCHANNLE_COMBAT_UNIT
        card_event_type = CARD_EVENT_NONE
        combat_unit_event_type = COMBAT_UNIT_EVENT_BLOCKCHANGE
        information ={
            COMBAT_UNIT_GUID_KEY:combat_unit_game_unique_id,
            NEW_BLOCK_VALUE_KEY:str(new_block_value)}
        return GameEvent(
            event_channel,
            card_event_type, 
            combat_unit_event_type,
            information)