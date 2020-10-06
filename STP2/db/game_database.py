import sys
import os 
import json
import shutil

from pathlib import Path
from distutils.dir_util import copy_tree

from . import manifest
from . import game_app_data
from . import const_setting

class GameDatabase:
    def __init__(self,root_dir:str):
        manifest_path = root_dir + "\\" + const_setting.MANIFEST_FILENAME
        print("try read manifest at: "+manifest_path)
        self.manifest = manifest.Manifest.load_from_file(manifest_path)

        gameapp_root_dir = self.search_gameapp_root_with_name(root_dir,self.manifest.game_app)

        print("try load game app data at: " + gameapp_root_dir)
        self.game_app_data = game_app_data.GameAppData(gameapp_root_dir)

        print("succeeed to create GameDataBase from root: "+root_dir)

    def search_gameapp_root_with_name(self,db_root_dir,gameapp_name):
        for path in Path(db_root_dir).rglob('init.json'):
            if path.parent.name == gameapp_name:
                return  os.path.dirname(path)
        raise Exception("fail to game app named: "+gameapp_name)

    def print_data_to_terminal(self):
        print("[manifest]----------------------------------------------------")
        print(self.manifest.__dict__)
        print("[game app data]----------------------------------------------")
        print("cards:")
        print([name for name in self.game_app_data.cards_dict.keys()])
        print("deck config:")
        print(self.game_app_data.deck_config)
        print("rules:")
        print(self.game_app_data.rules)
        print("[data base end]----------------------------------------------")

    def check_consistency(self):
        is_consist = True
        print("[data base] check consistency")
        print("[data base] current app: "+ self.manifest.game_app)

        print("[data base] check cards and deck...")
        for card_name in self.game_app_data.deck_config.keys():
            if card_name not in self.game_app_data.cards_dict: 
                is_consist = False
                print("[data base]-[ERROR]: ",card_name," in deckConfig is not found in Cards")
        for card_name in self.game_app_data.cards_dict.keys():
            if card_name not in self.game_app_data.deck_config: 
                is_consist = False
                print("[data base]-[ERROR]]: ",card_name," in Cards is not used in DeckConfig")
                
        print("[data base] check cards and buffs...")
        for card in self.game_app_data.cards_dict.values():
            for buff_name in card.buffs.keys():
                if buff_name not in self.game_app_data.buff_dict:
                    is_consist = False
                    print("[data base]-[ERROR]: buffname ",buff_name,"int",card.name, "is not found in buffs")
        return is_consist

def calculate_root_dir():
    ROOT_FOLDER_NAME = "DATA" 
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir =  os.path.dirname(Path(cur_dir))
    root_dir = parent_dir+'\\'+ROOT_FOLDER_NAME
    return root_dir

def clear_game_database():
    root_dir = calculate_root_dir()
    shutil.rmtree(root_dir)

def init_game_database():
    print("[game database] - start to init database...")

    root_dir = calculate_root_dir()
    print("[game database] - root folder : "+root_dir)

    if os.path.exists(root_dir):
        print("[game database] - [Is folder exist?]: yes")
        print ("[Fail] root folder already existed: "+root_dir+" !!!!!!!!!!!!!!!!!!!")
        print("(run 'db_manager.py clear' or delete it mannualy)")
        return
    else:
        print("[game database] - [Is folder exist?]: no")

    print("[game database] - make root folder: "+root_dir)
    os.makedirs(root_dir)

    # create manifest file
    manifest_path = root_dir + '\\'+ const_setting.MANIFEST_FILENAME
    print("[game database] - make manifest file at: "+manifest_path)
    mf = manifest.Manifest()    
    mf.game_app = "DefaultApp"
    mf.root_directory = root_dir
    mf_json = json.dumps(mf.__dict__, indent = 4)
    f= open(manifest_path,"w+")
    f.write(mf_json)
    f.close()

    # create default game app
    print("[game database] - create default game app")
    default_app_dir = root_dir + "\\" + "DefaultApp"
    os.makedirs(default_app_dir)
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    app_src_dir = cur_dir+"\\" + "DefaultApp"
    copy_tree(app_src_dir, default_app_dir)

def check_game_database():
    root_dir = calculate_root_dir()
    game_db = GameDatabase(root_dir)
    game_db.print_data_to_terminal()
    game_db.check_consistency()