import unittest

from core.backtrade.client.runner import StrategyRunner
from core.backtrade.strategy.breaker import BreakerStrategy
from core.backtrade.strategy.channel import ChannelStrategy
from core.backtrade.strategy.ema import EMAStrategy, EMAV2Strategy, SimpleEmaStrategy
from core.backtrade.strategy.feature import FeatureTradeStrategy
from core.backtrade.strategy.frequency import HighFrequencyStrategy
from core.backtrade.strategy.ichimoku import IchimokuStrategy
from core.backtrade.strategy.macd import MacdStrategy
from core.backtrade.strategy.rbreaker import RBreakerStrategy
from core.backtrade.strategy.rsi import RsiStrategy
from core.backtrade.strategy.sma import SmaStrategy
from core.backtrade.strategy.spot import SpotStrategy
from core.backtrade.strategy.turtle import TurtleStrategy


class TestStrategyRunner(unittest.TestCase):

    def test_sma_strategy(self):
        """
        测试sma策略
        :return:
        """
        runner = StrategyRunner()
        runner.config.strategy = SmaStrategy
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

    def test_high_frequency_strategy(self):
        """
        测试基于一目均衡的策略
        :return:
        """
        runner = StrategyRunner()
        runner.config.strategy = IchimokuStrategy
        runner.run()

    def test_ris_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = RsiStrategy
        runner.run()

    def test_channel_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = ChannelStrategy
        runner.run()

    def test_macd_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = MacdStrategy
        runner.run()

    def test_ema_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = EMAStrategy
        runner.run()

    def test_ema_v2_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = EMAV2Strategy
        runner.run()

    def test_simple_ema_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = SimpleEmaStrategy
        runner.run()

    def test_breaker_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = BreakerStrategy
        runner.run()
