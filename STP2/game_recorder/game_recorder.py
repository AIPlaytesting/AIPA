from .record_data import SingleBattleData,FragmentRecord
from ..protocol import MarkupFactory

class GameRecorder:
    def __init__(self):
        self.battle_record = SingleBattleData()
        self.current_fragment = None

    def start_record_one_battle(self):
        self.battle_record = SingleBattleData()
        self.current_fragment = None
        
    def record_game_state(self,game_state):
        if self.current_fragment != None:
            self.battle_record.fragments.append(self.current_fragment)
        # TODO ：BUG create markup to store
        self.current_fragment = FragmentRecord(game_state)#should be game_state_markup

    def record_game_events(self,game_events):
        if self.current_fragment == None:
            raise Exception("at least record gameState once before record any game events")
        self.current_fragment.game_events.extend(game_events)#should be game_event_markup

    def save_record_data(self):
        pass