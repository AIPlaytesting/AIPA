import tensorflow as tf
import numpy as np

class AI_Tester:
    def __init__(self, model_path):
        self.model_path = model_path

    def LoadModel(self):
        self.q_model = tf.keras.model.load_model(self.model_path)

    
    def PredictAction(self, state):
        actions = self.q_model.__call__(np.array([state]), dtype=float)
        action_vec = actions[0]

        return action_vec, False
