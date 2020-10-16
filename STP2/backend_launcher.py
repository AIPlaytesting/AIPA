from backend.gameplay_kernel import GameplayKernel
from backend.db_accessor import DBAccessor
from backend.connection import Connection
from backend.backend_mainloop import BackendMainloop

from rlbot import RLBot

from db.game_database import GameDatabase, calculate_root_dir
from gameplay.game_manager import GameManager

# connect to frontend
connection = Connection()
connection.connect()

# load database
db_root = calculate_root_dir()
game_db = GameDatabase(db_root)

# create game_manager
game_manager = GameManager(game_db.game_app_data)

# create compontents for BackendMainLoop
db_accessor = DBAccessor(game_db)
gameplay_kernel = GameplayKernel(game_manager)

# creat and load RLBot
rlbot = RLBot(game_manager)

# create backendmainloop and run 
backend_mainloop = BackendMainloop(connection,gameplay_kernel,db_accessor,rlbot)
backend_mainloop.run()