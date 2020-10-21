import AI_Module.AI_Brain_Q_Basic_Condensed
import AI_Module.AI_Brain_Q_Double

import AI_Module.ReplayBuffer
import AI_Module.GameBuffer
import AI_Module.DataWriter
import Environment #also a part of the AI

import numpy as np
import matplotlib.pyplot as plt
import csv
import time
import winsound


#initialize the environment
env = Environment.Environment()

game_buffer = AI_Module.GameBuffer.GameBuffer(env.ai_transformer.state_space, env.ai_transformer.action_space, env.unplayable_card_pun,isCustomCardRewards = False)
game_buffer.data_collector.StoreDeckConfig(env.ai_transformer.deck_config)

#Replace string with file description is needed
data_writer = AI_Module.DataWriter.DataWriter(game_buffer.data_collector, 'no custom rewards-overnight')

state_space_len = env.state_space_dim
action_space_len = env.action_space_dim

number_of_games = 100000

start_time = time.time()

#Q-Learning Basic
#ai_agent = AI_Module.AI_Brain_Q_Basic.AI_Brain(gamma=0.9, state_space_dim=98, action_space_dim=13,
#                   hidden_layer_dims=[256, 256, 256, 256], epsilon=0.8, epsilon_dec=0.00, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#ai_agent = AI_Module.AI_Brain_Q_Simple.AI_Brain(gamma=0.9, action_space_dim=12,
#                   epsilon=0.8, epsilon_dec=0.00, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#Q-Learning Multiple Models
#ai_agent = AI_Module.AI_Brain_Q_Multiple.AI_Brain(action_space_dim=12, batch_size = 64, gamma = 0.9, eps=0.8, eps_min = 0.03, eps_dec = 0.003)

#Q-Learning Condensed State
#ai_agent = AI_Module.AI_Brain_Q_Basic_Condensed.AI_Brain(gamma=0, state_space_dim=state_space_len, action_space_dim=action_space_len,
#               hidden_layer_dims=[256, 256, 256, 1024], epsilon=0.8, epsilon_dec=0.0003, epsilon_min = 0.01, mem_size = 10000, batch_size = 128)

#Double Q-Learning
ai_agent = AI_Module.AI_Brain_Q_Double.AI_Brain(gamma=0, state_space = env.ai_transformer.state_space, action_space = env.ai_transformer.action_space,
                hidden_layer_dims=[128, 128, 64, 1024], epsilon=1.0, epsilon_dec=0.0003, epsilon_min = 0.01, mem_size = 15000, batch_size = 128, unplayable_pun = env.unplayable_card_pun)


total_episode_rewards = []
eps_history = []
episode_length_history = []

#turn_buffer = AI_Module.ReplayBuffer.ReplayBuffer(98, 1000)

for i in range(number_of_games):
    done = False
    total_episode_reward = 0
    state = env.Reset()
    episode_len = 0

    game_start_time = time.time()
    prediction_time = 0

    while not done:
        start_prediction_time = time.time()
        
        action_space_vec, isRandom = ai_agent.PredictAction(state)
        
        end_prediction_time = time.time()
        prediction_time += end_prediction_time - start_prediction_time

        new_state, action, reward, done, pac_state, isTurnEnd = env.Step(action_space_vec, isRandom)
        
        episode_len += 1
        
        if(action != -1):
            game_buffer.StoreByTurns(state, new_state, action, reward, done, isTurnEnd)
        else:
            game_buffer.TurnEnd()
            
        state = new_state
    
    game_end_time = time.time()
    game_play_time = (game_end_time - game_start_time) - prediction_time
    total_game_play_time = game_end_time - game_start_time



    game_buffer.TurnEnd()
    game_buffer.RewardCalculations()

    start_train_time = time.time()
    
    game_buffer.TransferToReplayBuffer(ai_agent, env.win_int)
    
    end_train_time = time.time()
    train_time = end_train_time - start_train_time

    game_buffer.StoreGameData(ai_agent.epsilon, env.win_int, new_state, prediction_time, game_play_time, train_time)
    game_buffer.ResetBuffer()

    print("================================================")
    print("Episode Ended - " + str(i))
    print("================================================")

    if (i != 0 and (i + 1) % 250 == 0):
        data_writer.WriteFile()
        ai_agent.SaveModel()


# x = [i for i in range(number_of_games)]

# plt.figure(1)
# plt.plot(x, total_episode_rewards, label="Reward per episode")
# plt.xlabel("Game Number")
# plt.ylabel("Reward per episode")
# plt.show()

#ai_agent.SaveModel("training_1.hd5")

time_taken = time.time() - start_time

print("Time taken to run training : %.2f Hours" % (time_taken/3600))



#Code to play a small sound when training is done
freq = 700 #higher is sharper
dur = 1500 #milliseconds
winsound.Beep(freq, dur)

