import sys
import os 
import json
from pathlib import Path
from manifest import Manifest
from game_app_data import GameAppData
from distutils.dir_util import copy_tree

class GameDataBase:
    def __init__(self):
        self.manifest = Manifest()
        self.game_app_data = GameAppData()

    @classmethod
    def load_database(cls,root_directory:str):
        pass

def InitGameDatabase():
    ROOT_FOLDER_NAME = "DATA"

    print("[game database] - start to init database...")
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    print("[game database] - current directoy: "+ cur_dir)
    parent_dir =  os.path.dirname(Path(cur_dir))

    print("[game database] - create root folder at: " + parent_dir)
    root_folder_dir = parent_dir+'\\'+ROOT_FOLDER_NAME

    if os.path.exists(root_folder_dir):
        print("[game database] - [Is folder exist?]: yes")
        print("[game database] - [Fail] need mannually delete existing folder")
        return
    else:
        print("[game database] - [Is folder exist?]: no")

    print("[game database] - make root folder: "+root_folder_dir)
    os.makedirs(root_folder_dir)

    # create manifest file
    manifest_path = root_folder_dir + '\\'+'manifest.json'
    print("[game database] - make manifest file at: "+manifest_path)
    manifest = Manifest(root_folder_dir)    
    manifest.game_app = "DafaultApp"
    manifest_json = json.dumps(manifest.__dict__, indent = 4)
    f= open(manifest_path,"w+")
    f.write(manifest_json)
    f.close()

    # create default game app
    print("[game database] - create default game app")
    default_app_dir = root_folder_dir + "\\" + "DefaultAPP"
    os.makedirs(default_app_dir)
    app_src_dir = cur_dir+"\\" + "DefaultAPP"
    copy_tree(app_src_dir, default_app_dir)

argv = sys.argv
if len(argv) > 1 and argv[1] == 'init':
    InitGameDatabase()