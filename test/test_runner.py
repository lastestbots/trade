import unittest

from core.backtrade.client.runner import StrategyRunner
from core.backtrade.strategy.sma import SmaCross


class TestStrategyRunner(unittest.TestCase):

    def test_run_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = SmaCross
        runner.run()

    def test_sma_strategy(self):
        runner = StrategyRunner()
        runner.config.strategy = SmaCross
        runner.run()
