from .connection import Connection
from game_manager import GameManager

class DBQueryLoop:
    def __init__(self,connection:Connection,game_manager:GameManager):
        self.connection = connection
        self.game_manager = game_manager
        
    def run(self):
        pass