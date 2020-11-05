import os
from .record_data import SingleBattleData,FragmentRecord
from backend.protocol import MarkupFactory
from datetime import datetime

class GameRecorder:
    def __init__(self,game_root_dir):
        self.battle_record = SingleBattleData()
        self.current_fragment = None
        self.save_root_dir = game_root_dir + '\\Record'
        self.record_counter = 0

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

    def save_record_data(self, save_as_player = False):
        save_path = self.calculate_save_path(save_as_player)
        print("[game recorder] - save record at: "+ save_path)
        record_json = self.battle_record.encode_to_json()
        f= open(save_path,"w+")
        f.write(record_json)
        f.close()
    
    def calculate_save_path(self, save_as_player):
        save_dir =  self.save_root_dir
        if save_as_player:
            save_dir += '\\Player'
        else:
            save_dir += '\\AI'
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        now = datetime.now()
        filename = str(self.record_counter) + now.strftime("-%b-%d-%H-%M-%S")
        self.record_counter += 1

        save_path = save_dir + "\\"+filename+".json"
        return save_path
