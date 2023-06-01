import unittest

from core.backtrade.client.mock import SpotTradeClient

client = SpotTradeClient()
client.run()


class TestSpotTradeClient(unittest.TestCase):

    def test_run_strategy(self):
        """
        测试实盘模拟交易策略
        :return:
        """
        SpotTradeClient().run()
