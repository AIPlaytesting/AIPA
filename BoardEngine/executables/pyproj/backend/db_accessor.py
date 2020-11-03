from .protocol import DBQuery
from db.game_database import GameDatabase
import json

class DBAccessor:
    def __init__(self,db:GameDatabase):
        self.db = db

    def process_dbquery(self,dbquery:DBQuery)->str:
        result = {}
        if dbquery.query_sentence == 'registeredCardnames':
            cardnames =[cardname for cardname in self.db.game_app_data.cards_dict.keys()] 
            result = {"cardnames":cardnames}
        elif dbquery.query_sentence == 'registeredBuffnames':
            buffnames =[buffname for buffname in self.db.game_app_data.registered_buffnames] 
            result = {"buffnames":buffnames}
        return json.dumps(result)