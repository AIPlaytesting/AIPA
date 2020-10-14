from backend.dbqueryloop import DBQueryLoop
from backend.gameplayloop import GameplayLoop
from backend.connection import Connection
from db.game_database import GameDatabase, calculate_root_dir
from game_manager import GameManager

# connect to frontend
connection = Connection()
connection.connect()

# load database
db_root = calculate_root_dir()
game_db = GameDatabase(db_root)

# create game manager
game_manager = GameManager(game_db.game_app_data)

