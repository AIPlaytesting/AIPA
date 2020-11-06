import json

class Manifest:
    def __init__(self):
        self.game_app = ""
        self.root_directory = ""
        self.resource_directory = "Resources"
    
    @classmethod
    def load_from_file(cls,file_path):
        file = open(file_path, "r")
        json_str = file.read()
        json_dict = json.loads(json_str)    
        manifest = Manifest()
        manifest.game_app = json_dict["game_app"]
        manifest.root_directory = json_dict["root_directory"]
        manifest.resource_directory = json_dict["resource_directory"]
        return manifest