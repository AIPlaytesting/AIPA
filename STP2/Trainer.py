import AI_Module.AI_Brain_Q_Basic
import AI_Module.AI_Brain_Q_Multiple
import AI_Module.AI_Brain_Q_Simple
import AI_Module.ReplayBuffer
import Environment
import numpy as np
import matplotlib.pyplot as plt
import csv



def RewardModification(pac_state):
    #pac_state = (old_player_info, new_player_info, old_boss_info, new_boss_info)
    #old_player_info = (old_player_hp, old_player_block, old_player_buffs, old_player_energy)

    old_player_block = pac_state[0][1]
    new_player_block = pac_state[1][1]
    block_used = old_player_block - new_player_block

    old_player_hp = pac_state[0][0]
    new_player_hp = pac_state[0][1]
    boss_damage = (old_player_hp - new_player_hp) + block_used

    #Check if flex was used during the turn and give it a reward for 25% of damage dealth after flex being used
    flex_used = 8 in turn_buffer.action_memory

    if(flex_used):
        flex_index = np.where(turn_buffer.action_memory == 8)[0][0]
        ctr = flex_index
        flex_additional_reward = 0
        while(ctr < len(turn_buffer.action_memory)):
            flex_additional_reward += turn_buffer.reward_memory[ctr] * 0.25
            ctr += 1
        turn_buffer.reward_memory[flex_index] += flex_additional_reward
            
    #Check if double tap was used and give it a reward of 50% of damage dealt after it was used
    doubletap_used = 9 in turn_buffer.action_memory

    if(doubletap_used):
        doubletap_index = np.where(turn_buffer.action_memory == 9)[0][0]
        ctr = doubletap_index
        doubletap_additional_reward = 0
        while(ctr < len(turn_buffer.action_memory)):
            doubletap_additional_reward += turn_buffer.reward_memory[ctr] * 0.3
            ctr += 1
        turn_buffer.reward_memory[doubletap_index] += doubletap_additional_reward

    #Calculate the block that was used up during the boss turn
    if block_used > 0:
        defend_used = 1 in turn_buffer.action_memory
        shrug_used = 2 in turn_buffer.action_memory

        defend_index = np.where(turn_buffer.action_memory == 1)
        shrug_index = np.where(turn_buffer.action_memory == 2)

        if(defend_used and shrug_used):
            defend_additional_reward = (6/14) * (block_used) * 0.01
            shrug_additional_reward = (8/14) * (block_used) * 0.01

            turn_buffer.reward_memory[defend_index[0][0]] += defend_additional_reward
            turn_buffer.reward_memory[shrug_index[0][0]] += shrug_additional_reward

        elif(defend_used):
            defend_additional_reward = block_used * 0.01
            turn_buffer.reward_memory[defend_index[0][0]] += defend_additional_reward
        
        elif(shrug_used):
            shrug_additional_reward = block_used * 0.01
            turn_buffer.reward_memory[shrug_index[0][0]] += shrug_additional_reward

    #If boss dealt damage and was weakened, give reward to clothesline for damage blocked
    if(boss_damage > 0):
        boss_weakened_count = pac_state[2][2]['Weakened']

        if(boss_weakened_count > 0):
            #was clothesline used?
            clothesline_used = 11 in turn_buffer.action_memory

            if(clothesline_used):
                clothesline_index = np.where(turn_buffer.action_memory == 11)[0][0]
                clothesline_additional_reward = boss_damage / 3

                turn_buffer.reward_memory[clothesline_index] += clothesline_additional_reward



#initialize the environment
env = Environment.Environment()

number_of_games = 5000

#Q-Learning Basic
ai_agent = AI_Module.AI_Brain_Q_Basic.AI_Brain(gamma=0.9, state_space_dim=98, action_space_dim=12,
                   hidden_layer_dims=[256, 256, 256, 256], epsilon=1.0, epsilon_dec=0.0000, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#ai_agent = AI_Module.AI_Brain_Q_Simple.AI_Brain(gamma=0.9, action_space_dim=12,
#                   epsilon=0.8, epsilon_dec=0.00, epsilon_min = 0.03, mem_size = 100000, batch_size = 64)


#Q-Learning Multiple Models
#ai_agent = AI_Module.AI_Brain_Q_Multiple.AI_Brain(action_space_dim=12, batch_size = 64, gamma = 0.9, eps=0.8, eps_min = 0.03, eps_dec = 0.003)

total_episode_rewards = []
eps_history = []

turn_buffer = AI_Module.ReplayBuffer.ReplayBuffer(98, 1000)

for i in range(number_of_games):
    done = False
    total_episode_reward = 0
    state = env.Reset()

    while not done:
        action_space_vec = ai_agent.PredictAction(state)
        new_state, action, reward, done, pac_state, isTurnEnd = env.Step(action_space_vec)

        total_episode_reward += reward
        state = new_state

        if(action != -1):
            turn_buffer.StoreTransition(state, new_state, action, reward, done)
            
        if(isTurnEnd):
            RewardModification(pac_state)
            indexes_to_get = np.arange(turn_buffer.mem_ctr)
            t_states, t_new_states, t_actions, t_rewards, t_dones = turn_buffer.GetFromBuffer(indexes_to_get)

            for i in range(turn_buffer.mem_ctr):
                ai_agent.StoreTransition(t_states[i], t_new_states[i], t_actions[i], t_rewards[i], t_dones[i])
                ai_agent.Learn()

            turn_buffer.ResetBuffer()


    eps_history.append(ai_agent.epsilon)
    total_episode_rewards.append(total_episode_reward)


    print("================================================")
    print("Total reward from episode " + str(i) + " : " + str(total_episode_reward))
    print("================================================")

rows = zip(total_episode_rewards, eps_history)

with open('training_5.csv', 'w+', newline='') as f:
    filewriter = csv.writer(f)
    for row in rows:
        filewriter.writerow(row)

    for key in env.action_cards_played:
        filewriter.writerow([key])
        filewriter.writerow([env.action_cards_played[key]])

    filewriter.writerow([(env.win_count/number_of_games)*100])
    


x = [i for i in range(number_of_games)]

plt.figure(1)
plt.plot(x, total_episode_rewards, label="Reward per episode")
plt.xlabel("Game Number")
plt.ylabel("Reward per episode")

#ai_agent.SaveModel("training_1.hd5")

