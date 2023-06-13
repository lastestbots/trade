import gym
import numpy as np
from gym import spaces


class RobotMazeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, maze):
        super(RobotMazeEnv, self).__init__()

        self.maze = maze  # 迷宫地图
        self.height, self.width = maze.shape
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.height, self.width), dtype=np.uint8)
        self.reward_range = (-1, 1)

        self.robot_pos = None
        self.goal_pos = None
        self.reset()

    def step(self, action):
        self._take_action(action)

        if self.robot_pos == self.goal_pos:
            return self.robot_pos, 1, True, {}

        done = False
        if self.maze[self.robot_pos] == 1:
            reward = -1  # 撞墙
            done = True
        else:
            reward = 0
        return self.robot_pos, reward, done, {}

    def reset(self):
        self.robot_pos = np.array([0, 0])
        self.goal_pos = np.array([self.height - 1, self.width - 1])
        return self.robot_pos

    def render(self, mode='human'):
        output = ''
        for y in range(self.height):
            for x in range(self.width):
                if np.array_equal(self.robot_pos, [y, x]):
                    output += 'R'
                elif np.array_equal(self.goal_pos, [y, x]):
                    output += 'G'
                elif self.maze[y, x] == 1:
                    output += '#'
                else:
                    output += '.'
            output += '\n'
        print(output)

    def _take_action(self, action):
        if action == 0:  # 上
            next_pos = self.robot_pos + np.array([-1, 0])
        elif action == 1:  # 下
            next_pos = self.robot_pos + np.array([1, 0])
        elif action == 2:  # 左
            next_pos = self.robot_pos + np.array([0, -1])
        elif action == 3:  # 右
            next_pos = self.robot_pos + np.array([0, 1])

        if 0 <= next_pos[0] < self.height and next_pos[1] >= 0 and next_pos[1] < self.width:
            self.robot_pos = next_pos


maze = np.array([[0, 0, 0, 1, 0],
                 [0, 1, 0, 1, 0],
                 [0, 1, 0, 0, 0],
                 [0, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0]])

env = RobotMazeEnv(maze)

done = False
env.render()
while not done:
    action = env.action_space.sample()
    obs, reward, done, _ = env.step(action)
    env.render()
    print('Action:', action, 'Reward:', reward)
