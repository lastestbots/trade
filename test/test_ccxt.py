import unittest

from core.rpc.ccxt_adapter import CCtxAdapter
from core.utils.ccxt_util import OhlvUtil


class TestCctxUtil(unittest.TestCase):

    def test_load_data(self):
        """
        测试加载数据
        :return:
        """
        OhlvUtil.load_ohlv_as_pd(symbol='IOTA/USDT', timeframe='1d')

    def test_load_symbols(self):
        """
        测试加载股票
        :return:
        """
        symbols = CCtxAdapter.query_symbols('USDT')
        print(symbols)
