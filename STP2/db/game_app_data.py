import json
import glob
from .const_setting import *

class GameAppData:
    def __init__(self,root_dir:str):
        self.root_dir = root_dir
        # get init info
        init_info = load_json_from_file(root_dir + '\\' + INIT_FILENAME)

        # self.buff_dict: buffname, buffObject
        buff_path = root_dir + "\\" + init_info['buffs_file']
        buff_info = load_json_from_file(buff_path)
        self.registered_buffnames = buff_info['registered_buffnames']
        
        # self.cards_dict: cardname:str,Card:game_app_data.Card
        self.cards_dict = {}
        cards_dir = root_dir + "\\" + init_info['cards_directory']
        cards = GameAppData.load_cards_under_directory(cards_dir, self.registered_buffnames)
        for card in cards:
            self.cards_dict[card.name] = card

        # self.rules: rulename,rulevalue
        rules_file_path = root_dir +"\\" + init_info['rules_file']
        self.rules = load_json_from_file(rules_file_path)

        # self.deckConfig: cardname,number
        deck_path = root_dir + "\\" + init_info['decks_directory'] + '\\' +self.rules['deck'] + ".json"
        self.deck_config = load_json_from_file(deck_path)

    @classmethod
    def load_cards_under_directory(cls,cards_dir:str, registered_buffnames):    
        pattern = cards_dir + "\\" + "*json"
        print("search cards with pattern : "+pattern)
        cards = []  
        for file_path in glob.glob(pattern):
            new_card = Card(file_path, registered_buffnames)
            cards.append(new_card)
            #print("[load card]: "+new_card.name)
        return cards

class Card:
    def __init__(self, file_path, registered_buffnames):
        card_data = load_json_from_file(file_path)
        self.name = card_data["name"]
        self.type = card_data["type"]
        self.energy_cost = card_data["energy_cost"]
        self.damage_block = card_data["damage_block_info"]
        self.card_life_cycle = card_data["card_life_cycle_info"]
        self.buffs = {}
        self.buffs = card_data["buffs_info"] 
        card_buff_dict_from_json = card_data["buffs_info"]
        for buff_name in registered_buffnames:
            if buff_name in card_buff_dict_from_json:
                self.buffs[buff_name] = card_buff_dict_from_json[buff_name] # key: buffname value: buffobject
            else:
                self.buffs[buff_name] = {"value" : 0, "target" : "self"}
        self.special_mod = card_data["special_modifiers_info"]

        # optional fields
        if 'description' in card_data:
            self.description = card_data['description']
        else:
            self.description = self.name

        # img_src is the relative path under resouces dir
        if "img_relative_path" in card_data:
            self.img_relative_path = card_data['img_relative_path']
        else:
            self.img_relative_path = ""

def load_json_from_file(file_path):
    with open(file_path, "r") as file:
        raw_json_data = file.read()
        return json.loads(raw_json_data)  