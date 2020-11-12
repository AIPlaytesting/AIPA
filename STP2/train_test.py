
import time
import ai_test_controller
import sys, os


config = {'game_id':'TestApp','deck_id':'deck1','game_nums':'200'}

ai_tester = ai_test_controller.AI_Tester(app_id=config['game_id'], deck_id=config['deck_id'])

# if ai_tester.main_folder_path == "":
#     return

#disable printing
sys.stdout = open(os.devnull, 'w')

game_nums = int(config['game_nums'])
for i in range(game_nums):
    ai_tester.TestOneIteration(i)
    # simulate_progress ={}
    # simulate_progress['curprogress'] = i+1
    # simulate_progress['maxprogress'] = game_nums
    # connection.send_response(ResponseMessage("electron",simulate_progress))

#enable print again
sys.stdout = sys.__stdout__

ai_tester.ProcessDataAndWriteFiles()
