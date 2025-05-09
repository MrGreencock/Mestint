import tensorflow as tf
from keras import layers
import numpy as np

"""
Neurális Háló Ágens osztály létrehozása
Nagyjából: a QLearnignAgent helyett egy neurális hálót építek ki.

"""


class NeuralNetworkAgent:
    def __init__(self, state_dim, action_dim, learning_rate=0.001):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()
        self.optimizer = tf.keras.optimizers.Adam(learning_rate)
        self.loss_fn = tf.keras.losses.MeanSquaredError()

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())


    """
    Neurális háló kiépítése
    2 db 128 neuronos Dense réteg ReLU aktivációval
    """
    def build_model(self):
        return tf.keras.Sequential([
            layers.Input(shape=(self.state_dim, )),
            layers.Dense(128, activation="relu"),
            layers.Dense(128, activation="relu"),
            #layers.Dense(128, activation="relu"),
            layers.Dense(self.action_dim)])

    def act(self, state, epsilon):
        if np.random.rand() < epsilon:
            return np.random.choice(self.action_dim)

        """A q-értékeket a neurális háló alapján kapjuk meg"""
        q_values = self.model(np.array([state], dtype=np.float32))
        return np.argmax(q_values[0].numpy())


    def learn(self, state, action, reward, next_state, gamma):
        state = np.array([state], dtype=np.float32)
        next_state = np.array([next_state], dtype=np.float32)
        """A q-értékeket a neurális háló alapján kapjuk meg"""
        q_values = self.model(state)
        next_q_values = self.target_model(next_state)

        target_q = q_values.numpy()
        target_q[0][action] = reward + gamma * np.max(next_q_values.numpy())

        with tf.GradientTape() as tape:
            q_pred = self.model(state) #Háló előrejelzése
            """Mivel neurális háló, kell loss függvény"""
            loss = self.loss_fn(target_q, q_pred) # Mean Squared Error a cél és az előrejelzés között
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))


