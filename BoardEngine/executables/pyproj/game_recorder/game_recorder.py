import os
from .record_data import SingleBattleData,FragmentRecord
from backend.protocol import MarkupFactory

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
        game_state_markup = MarkupFactory.create_game_state_markup(game_state)
        self.current_fragment = FragmentRecord(game_state_markup)

    def record_game_events(self,game_events):
        if self.current_fragment == None:
            raise Exception("at least record gameState once before record any game events")
        
        game_event_markups = []
        for game_event in game_events:
            markup = MarkupFactory.create_game_event_markup(game_event)
            game_event_markups.append(markup)

        self.current_fragment.game_events.extend(game_event_markups)#should be game_event_markup

    def save_record_data(self):
        save_path = self.calculate_save_path()
        print("[game recorder] - save record at: "+ save_path)
        record_json = self.battle_record.encode_to_json()
        f= open(save_path,"w+")
        f.write(record_json)
        f.close()
    
    def calculate_save_path(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        save_path = cur_dir+ "\\"+"game_record.json"
        return save_path
