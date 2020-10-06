import AI_Module.AI_Brain_Q_Basic
import AI_Module.AI_Brain_Q_Multiple
import AI_Module.AI_Brain_Q_Simple
import AI_Module.AI_Brain_Q_Basic_Condensed
import AI_Module.ReplayBuffer
import AI_Module.GameBuffer
import Environment
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
import winsound


#initialize the environment
env = Environment.Environment()
game_buffer = AI_Module.GameBuffer.GameBuffer()
state_space_len = env.state_space_dim
action_space_len = env.action_space_dim

number_of_games = 50000

start_time = time.time()

#Q-Learning Basic
#ai_agent = AI_Module.AI_Brain_Q_Basic.AI_Brain(gamma=0.9, state_space_dim=98, action_space_dim=13,
#                   hidden_layer_dims=[256, 256, 256, 256], epsilon=0.8, epsilon_dec=0.00, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#ai_agent = AI_Module.AI_Brain_Q_Simple.AI_Brain(gamma=0.9, action_space_dim=12,
#                   epsilon=0.8, epsilon_dec=0.00, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#Q-Learning Multiple Models
#ai_agent = AI_Module.AI_Brain_Q_Multiple.AI_Brain(action_space_dim=12, batch_size = 64, gamma = 0.9, eps=0.8, eps_min = 0.03, eps_dec = 0.003)

#Q-Learning Condensed State
ai_agent = AI_Module.AI_Brain_Q_Basic_Condensed.AI_Brain(gamma=0, state_space_dim=state_space_len, action_space_dim=action_space_len,
                   hidden_layer_dims=[128, 128, 1024, 1024], epsilon=0.8, epsilon_dec=0.0003, epsilon_min = 0.01, mem_size = 10000, batch_size = 128)

total_episode_rewards = []
eps_history = []
episode_length_history = []

#turn_buffer = AI_Module.ReplayBuffer.ReplayBuffer(98, 1000)

for i in range(number_of_games):
    done = False
    total_episode_reward = 0
    state = env.Reset()
    episode_len = 0

    while not done:
        action_space_vec, isRandom = ai_agent.PredictAction(state)
        print(action_space_vec)
        new_state, action, reward, done, pac_state, isTurnEnd = env.Step(action_space_vec, isRandom)
        
        total_episode_reward += reward
        episode_len += 1
        
        if(action != -1):
            game_buffer.StoreByTurns(state, new_state, action, reward, done, isTurnEnd)
        else:
            game_buffer.TurnEnd()
            
        state = new_state
    
    game_buffer.TurnEnd()
    game_buffer.RewardCalculations()
    game_buffer.TransferToReplayBuffer(ai_agent)
    game_buffer.ResetBuffer()

    eps_history.append(ai_agent.epsilon)
    total_episode_rewards.append(total_episode_reward)
    episode_length_history.append(episode_len)


    print("================================================")
    print("Total reward from episode " + str(i) + " : " + str(total_episode_reward))
    print("================================================")

    rows = zip(total_episode_rewards, eps_history, episode_length_history)

    if (i != 0 and i % 1000 == 0):
        with open('zero gamma with game buffer.csv', 'w+', newline='') as f:
            filewriter = csv.writer(f)
            for row in rows:
                filewriter.writerow(row)

            for key in env.action_cards_played:
                filewriter.writerow([key])
                filewriter.writerow([env.action_cards_played[key]])

            filewriter.writerow([(env.win_count/i)*100])




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

