import json
import glob
from .const_setting import *

class GameAppData:
    def __init__(self,root_dir:str):
        # self.cards_dict: cardname,Card
        self.cards_dict = {}
        cards_dir = root_dir + "\\" + CARDS_FOLDER_NAME
        cards = GameAppData.load_cards_under_directory(cards_dir)
        for card in cards:
            self.cards_dict[card.name] = card

        # self.rules: rulename,rulevalue
        rules_file_path = root_dir +"\\" + RULES_FILENAME
        self.rules = load_json_from_file(rules_file_path)

        # self.deckConfig: cardname,number
        deck_path = root_dir + "\\" +self.rules['deck'] + ".json"
        deck_config_path = root_dir +"\\" + DECK_CONFIG_FILENAME
        self.deck_config = load_json_from_file(deck_path)

    @classmethod
    def load_cards_under_directory(cls,cards_dir:str):    
        pattern = cards_dir + "\\" + "*json"
        print("search cards with pattern : "+pattern)
        cards = []  
        for file_path in glob.glob(pattern):
            new_card = Card(file_path)
            cards.append(new_card)
            #print("[load card]: "+new_card.name)
        return cards

class Card:
    def __init__(self,file_path):
        card_data = load_json_from_file(file_path)
        self.name = card_data["name"]
        self.type = card_data["type"]
        self.energy_cost = card_data["energy_cost"]
        self.damage_block = card_data["damage_block_info"]
        self.card_life_cycle = card_data["card_life_cycle_info"]
        self.buffs = card_data["buffs_info"]
        self.special_mod = card_data["special_modifiers_info"]

def load_json_from_file(file_path):
    with open(file_path, "r") as file:
        raw_json_data = file.read()
        return json.loads(raw_json_data)  