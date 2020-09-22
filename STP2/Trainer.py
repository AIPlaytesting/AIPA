import AI_Module.AI_Brain
import Environment

#initialize the environment
env = Environment.Environment()

number_of_games = 100

ai_agent = AI_Module.AI_Brain.AI_Brain(gamma=0.99, state_space_dim=98, action_space_dim=13,
                    hidden_layer_dims=[512, 512, 512, 512], epsilon=0.5, epsilon_dec=0.03, epsilon_min = 0.01, mem_size = 100000, batch_size = 64)

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
        ai_agent.StoreTransition(state, new_state, action, reward, done)
        state = new_state
        ai_agent.Learn()

    eps_history.append(ai_agent.epsilon)
    total_episode_rewards.append(total_episode_reward)

    print("================================================")
    print("================================================")
    print("================================================")
    print("Total reward from episode " + str(i) + " : " + str(total_episode_reward))
    print("================================================")
    print("================================================")
    print("================================================")

print(total_episode_rewards)
print(eps_history)

ai_agent.SaveModel("training_1.hd5")

