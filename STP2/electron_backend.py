from backend.protocol import ResponseMessage
from backend.connection import Connection

ELECTRON_LISTEN_PORT = 10000
# electron method code 
ELECTRON_DETECT_ENV = 10
ELECTRON_TRAIN = 11
ELECTRON_SIMULATE = 12

# connect to frontend
connection = Connection(ELECTRON_LISTEN_PORT)
connection.connect()

def detect_env_mainloop():
    def detectEnv():
        version = {}
        import sys
        pyver = sys.version_info
        version['py'] = str(pyver.major) +'.'+str(pyver.minor)+'.'+str(pyver.micro)
        try:
            import tensorflow
            version['tf'] = tensorflow.__version__
        except:
            version['tf'] = 'none'

        return version
    ver = detectEnv()
    connection.send_response(ResponseMessage("electron",ver))
    print("detect env mainloop done: ",ver)

def train_mainloop():
    import time
    import ai_train_controller
    import sys, os

    #disable printing
    sys.stdout = open(os.devnull, 'w')

    ai_trainer = ai_train_controller.AI_Trainer(app_id="", deck_id="")
    train_time_list = []
    num_games = 14000

    for i in range(num_games):
        train_time = ai_trainer.TrainOneIteration(i)
        if train_time > 1:
            train_time_list.append(train_time)

        avg_train_time = sum(train_time_list) / len(train_time_list) if len(train_time_list) > 0 else 4

        remaining_time = avg_train_time * (num_games - i + 1)
        rem_hrs = remaining_time // 3600
        rem_min = int((remaining_time - rem_hrs * 3600 ) % 60)

        train_info ={}
        train_info['curprogress'] = i
        train_info['maxprogress'] = num_games
        train_info['remaining_hours'] = rem_hrs
        train_info['remaining_minutes'] = rem_min
        connection.send_response(ResponseMessage("electron",train_info))

    #enable print again
    sys.stdout = sys.__stdout__

def simulate_mainloop():
    import time
    import ai_test_controller
    import sys, os

    ai_tester = ai_test_controller.AI_Tester(app_id='', deck_id='')

    if ai_tester.main_folder_path == "":
        return

    #disable printing
    sys.stdout = open(os.devnull, 'w')
    

    for i in range(2000):
        ai_tester.TestOneIteration(i)
        simulate_progress ={}
        simulate_progress['curprogress'] = i+1
        simulate_progress['maxprogress'] = 2000
        connection.send_response(ResponseMessage("electron",simulate_progress))
    
    #enable print again
    sys.stdout = sys.__stdout__

    ai_tester.ProcessDataAndWriteFiles()


# wait method
request = connection.wait_one_request()
if request.method == ELECTRON_DETECT_ENV:
    detect_env_mainloop()
elif request.method == ELECTRON_TRAIN:
    train_mainloop()
elif request.method == ELECTRON_SIMULATE:
    simulate_mainloop()
else:
    print("undefined method: ",request.method)