import pong as pong
import matplotlib.pyplot as plt
from neural_network import NeuralNetworkAgent

pong.init_pong()

import pickle

with open("agent.pkl", "rb") as f:
    pong.agent = pickle.load(f)
with open("state_to_id.pkl", "rb") as f:
    pong.state_to_id = pickle.load(f)

agent = NeuralNetworkAgent(state_dim=6, action_dim=3)

rewards, epsilon_history = pong.play_episodes(
    n_episodes=10,
    max_epsilon=0,
    min_epsilon=0,
    decay_rate=0,
    gamma=0,
    learn=True,
    viz=True,
    log=True,
    agent=agent
)

plt.plot(epsilon_history)
plt.show()
plt.plot(rewards)
plt.show()

pong.pygame.quit()