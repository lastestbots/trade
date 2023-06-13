# import random
# from collections import deque
#
# import numpy as np
# from keras.layers import Dense
# from keras.models import Sequential
# from keras.optimizers import Adam
#
#
# class DQNAgent:
#     def __init__(self, state_size, action_size):
#         self.state_size = state_size
#         self.action_size = action_size
#         self.memory = deque(maxlen=2000)
#         self.gamma = 0.95
#         self.eps = 1.0
#         self.eps_decay = 0.995
#         self.eps_min = 0.01
#         self.learning_rate = 0.001
#         self.model = self._build_model()
#
#     def _build_model(self):
#         model = Sequential()
#         model.add(Dense(24, input_dim=self.state_size, activation='relu'))
#         model.add(Dense(24, activation='relu'))
#         model.add(Dense(self.action_size, activation='linear'))
#         model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
#         return model
#
#     def remember(self, state, action, reward, next_state, done):
#         self.memory.append((state, action, reward, next_state, done))
#
#     def act(self, state):
#         if np.random.rand() <= self.eps:
#             return random.randrange(self.action_size)
#         act_values = self.model.predict(state)
#         return np.argmax(act_values[0])
#
#     def replay(self, batch_size):
#         minibatch = random.sample(self.memory, batch_size)
#         for state, action, reward, next_state, done in minibatch:
#             target = reward
#             if not done:
#                 target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
#             target_f = self.model.predict(state)
#             target_f[0][action] = target
#             self.model.fit(state, target_f, epochs=1, verbose=0)
#         if self.eps > self.eps_min:
#             self.eps *= self.eps_decay
#
#     def load(self, name):
#         self.model.load_weights(name)
#
#     def save(self, name):
#         self.model.save_weights(name)
#
#
# state_size = ...  # 根据交易策略确定状态空间的大小
# action_size = 3  # 买、卖、持有三个选项
# num_episodes = 100
# num_steps = 100
# agent = DQNAgent(state_size, action_size)
# for e in range(num_episodes):
#     state = ...  # 获取当前状态
#     for time in range(num_steps):
#         action = agent.act(state)
#         next_state, reward, done = ...  # 执行行动，观察奖励和下一个状态
#         agent.remember(state, action, reward, next_state, done)
#         state = next_state
#         if done:
#             print("episode: {}/{}, score: {}".format(e, num_episodes, time))
#             break
#     if len(agent.memory) > batch_size:
#         agent.replay(batch_size)
#     if e % 10 == 0:
#         agent.save("model.h5")
