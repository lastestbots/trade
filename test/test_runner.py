import unittest

from core.backtrade.client.runner import StrategyRunner
from core.backtrade.strategy.feature import FeatureTradeStrategy
from core.backtrade.strategy.frequency import HighFrequencyStrategy
from core.backtrade.strategy.rbreaker import RBreakerStrategy
from core.backtrade.strategy.sma import SmaCross
from core.backtrade.strategy.spot import SpotStrategy
from core.backtrade.strategy.turtle import TurtleStrategy


class TestStrategyRunner(unittest.TestCase):

    def test_sma_strategy(self):
        """
        测试sma策略
        :return:
        """
        runner = StrategyRunner()
        runner.config.strategy = SmaCross
        runner.run()

    def test_spot_strategy(self):
        """
        测试模拟实盘交易策略
        :return:
        """
        runner = StrategyRunner()
        runner.config.strategy = SpotStrategy
        runner.run()

    def test_feature_strategy(self):
        """
        测试模拟期货交易交易策略
        :return:
        """
        runner = StrategyRunner()
        runner.config.strategy = FeatureTradeStrategy
        runner.run()

    def test_rbreaker_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = RBreakerStrategy
        runner.run()

    def test_turtle_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = TurtleStrategy
        runner.run()

    def test_high_frequency_strategy(self):
        """
        测试高频策略
        :return:
        """
        runner = StrategyRunner()
        runner.config.strategy = HighFrequencyStrategy
        runner.run()
