from db.game_database import init_game_database,check_game_database
import sys

argv = sys.argv
if len(argv) > 1 and argv[1] == 'init':
    init_game_database()
if len(argv) > 1 and argv[1] == 'check':
    check_game_database()