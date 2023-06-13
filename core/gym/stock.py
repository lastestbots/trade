import gym
import numpy as np
from gym import spaces


class StockTradingEnv(gym.Env):
    def __init__(self, data):
        self.data = data
        self.action_space = spaces.Discrete(3)  # 0：卖出，1：不操作，2：买入
        self.observation_space = spaces.Box(low=0, high=1,
                                            shape=(6,))  # 对于每个时间步长，状态空间包含账户余额、持有的股票数量、买卖手续费、当前股票价格、前一日股票价格、累计收益
        self.reward_range = (0, np.inf)
        self.current_step = 0
        self.account_balance = 100000  # 账户初始资金
        self.holdings = 0  # 持有的股票数量
        self.cost_basis = 0  # 持有股票的成本基础
        self.commission_fee = 0  # 累计交易手续费
        self.episode_reward = 0  # 累计收益
        self.prices = self.data['prices']  # 股票价格序列
        self.reset()

    def reset(self):
        self.current_step = 0
        self.account_balance = 100000  # 账户初始资金
        self.holdings = 0  # 持有的股票数量
        self.cost_basis = 0  # 持有股票的成本基础
        self.commission_fee = 0  # 累计交易手续费
        self.episode_reward = 0  # 累计收益
        self.prices = self.data['prices']  # 股票价格序列
        return self._next_observation()

    def step(self, action):
        self._take_action(action)
        self.current_step += 1
        reward = self._get_reward()
        done = self.current_step == len(self.prices) - 1
        obs = self._next_observation()
        return obs, reward, done, {}

    def _next_observation(self):
        obs = np.array([
            self.account_balance / max(self.prices),  # 账户余额
            self.holdings / max(self.prices),  # 持有的股票数量
            self.commission_fee / self.account_balance,  # 本次买卖手续费
            self.prices[self.current_step] / max(self.prices),  # 当前股票价格
            self.prices[self.current_step - 1] / max(self.prices),  # 前一日股票价格
            self.episode_reward / 100000  # 累计收益
        ])
        return obs

    def _take_action(self, action):
        current_price = self.prices[self.current_step]
        action_type = action - 1  # 将动作类型进行转换
        if action_type == 0:  # 卖出操作
            if self.holdings == 0:
                return
            sell_units = self.holdings
            sell_price = current_price * (0.98 - min(0.03, 0.03 * (
                        1 - current_price / self.cost_basis)))  # 假设成交价为当前价格的 98% （因为卖出股票也会产生手续费和税费）
            self.account_balance += sell_units * sell_price
            self.holdings = 0
            self.commission_fee += sell_units * sell_price * 0.003
        elif action_type == 1:  # 不操作
            return
        elif action_type == 2:  # 买入操作
            buy_units = self.account_balance / current_price  # 购买全部可用资金的股票
            self.account_balance -= buy_units * current_price
            self.holdings += buy_units
            self.commission_fee += buy_units * current_price * 0.003
            self.cost_basis = current_price * (1 + min(0.15, 0.15 * (self.cost_basis / current_price - 1)))  # 更新成本基础

    def _get_reward(self):
        current_price = self.e[self.current_step]
        profit = (current_price - self.prices[0]) * self.holdings - self.commission_fee  # 计算累计收益
        self.episode_reward += profit
        return profit
