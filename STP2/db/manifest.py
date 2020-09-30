RULES_FILENAME = "rules.json"
DECK_CONFIG_FILENAME = "deckConfig.json"

class Manifest:
    def __init__(self,root_directory:str):
        self.game_app = ""
        self.root_directory = root_directory
        self.resource_directory = "Resources"
        self.game_app_cards_directory = "Cards"
    