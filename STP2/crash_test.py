
import time
import ai_train_controller
import sys, os

config = {'game_id':'TestApp','deck_id':'deck1','iterations':100}
#config = {'game_id':'TestApp','deck_id':'deck1','iterations':100}
#disable printing
sys.stdout = open(os.devnull, 'w')

ai_trainer = ai_train_controller.AI_Trainer(app_id=config['game_id'], deck_id=config['deck_id'])
train_time_list = []
num_games = int(config['iterations'])

for i in range(num_games):
    train_time = ai_trainer.TrainOneIteration(i)
    if train_time > 1:
        train_time_list.append(train_time)

    avg_train_time = sum(train_time_list) / len(train_time_list) if len(train_time_list) > 0 else 4

    remaining_time = avg_train_time * (num_games - i + 1)
    rem_hrs = remaining_time // 3600
    rem_min = int((remaining_time - rem_hrs * 3600 ) % 60)

    #enable print again
    sys.stdout = sys.__stdout__
    print('progress',i)
    #disable printing
    sys.stdout = open(os.devnull, 'w')

#enable print again
sys.stdout = sys.__stdout__

