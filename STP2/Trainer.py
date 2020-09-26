import AI_Module.AI_Brain_Q_Basic
import AI_Module.AI_Brain_Q_Multiple
import AI_Module.AI_Brain_Q_Simple
import Environment
import matplotlib.pyplot as plt
import csv


#initialize the environment
env = Environment.Environment()

number_of_games = 1000

#Q-Learning Basic
#ai_agent = AI_Module.AI_Brain_Q_Basic.AI_Brain(gamma=0.9, state_space_dim=98, action_space_dim=12,
#                   hidden_layer_dims=[512, 512, 512, 512], epsilon=0.8, epsilon_dec=0.00, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#ai_agent = AI_Module.AI_Brain_Q_Simple.AI_Brain(gamma=0.9, action_space_dim=12,
#                   epsilon=0.8, epsilon_dec=0.00, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#Q-Learning Multiple Models
ai_agent = AI_Module.AI_Brain_Q_Multiple.AI_Brain(action_space_dim=12, batch_size = 64, gamma = 0.9, eps=0.8, eps_min = 0.03, eps_dec = 0)

total_episode_rewards = []
eps_history = []

for i in range(number_of_games):
    done = False
    total_episode_reward = 0
    state = env.Reset()

    while not done:
        action_space_vec = ai_agent.PredictAction(state)
        new_state, action, reward, done = env.Step(action_space_vec)
        total_episode_reward += reward
        if(action != -1):
            ai_agent.StoreTransition(state, new_state, action, reward, done)
            state = new_state
            ai_agent.Learn()

    eps_history.append(ai_agent.epsilon)
    total_episode_rewards.append(total_episode_reward)


    print("================================================")
    print("Total reward from episode " + str(i) + " : " + str(total_episode_reward))
    print("================================================")

rows = zip(total_episode_rewards, eps_history)

with open('training_4.csv', 'w+', newline='') as f:
    filewriter = csv.writer(f)
    for row in rows:
        filewriter.writerow(row)

    for key in env.action_cards_played:
        filewriter.writerow([key])
        filewriter.writerow([env.action_cards_played[key]])    
    

x = [i for i in range(number_of_games)]

plt.figure(1)
plt.plot(x, total_episode_rewards, label="Reward per episode")
plt.xlabel("Game Number")
plt.ylabel("Reward per episode")

#ai_agent.SaveModel("training_1.hd5")

