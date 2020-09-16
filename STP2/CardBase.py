import json

class Card:
    
    def __init__(self, cardname):
        self.ReadDataFromFile(cardname)
        self.DecodeJson()
    
    def ReadDataFromFile(self, filename):
        with open("Cards/" + filename + ".json", "r") as file:
            raw_json_data = file.read()
            self.card_data = json.loads(raw_json_data)    
    
    def DecodeJson(self):
        self.name = self.card_data["name"]
        self.energy_cost = self.card_data["energy_cost"]
        
        #damage and block information information
        self.damage_block = self.card_data["damage_block_info"]
        self.card_life_cycle = self.card_data["card_life_cycle_info"]
        self.buffs = self.card_data["buffs_info"]
        self.special_mod = self.card_data["special_modifiers_info"]
    
    
    
        
        
        
         
        
