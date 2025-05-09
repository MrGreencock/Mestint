import pong
from neural_network import NeuralNetworkAgent

pong.init_pong()
pong.screen

#Fontos változás!: mivel a num_states esetén jó kis errorokat dobott ki, így egy statikus 6-tal próbálkoztam. :)
pong.agent = NeuralNetworkAgent(state_dim=6, action_dim=3, learning_rate=1.0)
# A játék fő köre
clock = pong.pygame.time.Clock()

rewards, epsilon_history = pong.play_episodes(
    n_episodes=100,
    max_epsilon=1.0,
    min_epsilon=0.05,
    decay_rate=0.0001,
    gamma=0.95,
    learn=True,
    viz=False,
    human=False,
    log=False,
    agent=pong.agent
)

import matplotlib.pyplot as plt

# Ellenőrizhetjük az ügynök teljesítményének történetét
plt.plot(epsilon_history)
plt.show()

plt.plot(rewards)
plt.show()

