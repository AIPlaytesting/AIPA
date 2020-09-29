# keys in information dict
TURN_NAME_KEY = "turnName"
CARD_ID_KEY = "cardID"
BUFF_NAME_KEY = "buffName"
HURT_VALUE_KEY = "hurtValue"
BLOCK_VALUE_KEY = "blockValue"
BUFF_VALUE_KEY = "buffValue"

# event channel enum
EVENTCHANNLE_NONE = 0
EVENTCHANNLE_NEW_TURN = 1
EVENTCHANNLE_CARD = 2
EVENTCHANNLE_CHARACTER = 3

# card event type nume
CARD_EVENT_NONE = 0
CARD_EVENT_PLAYED = 1
CARD_EVENT_DRAW = 2

# character event type nume
CHARACTER_EVENT_NONE = 0
CHARACTER_EVENT_GETHURT = 1
CHARACTER_EVENT_GETBLOCK = 2
CHARACTER_EVENT_GETBUFF = 3

class GameEvent:
    def __init__(self,event_channel,card_event_type,character_event_type,information:dict):
        self.event_channel = event_channel
        self.card_event_type = card_event_type
        self.character_event_type = character_event_type
        self.information = information
    
    