import unittest

from core.utils.ccxt_util import OhlvUtil


class TestCctxUtil(unittest.TestCase):

    def test_load_data(self):
        OhlvUtil.load_ohlv_as_pd(symbol='ETHUSDT', timeframe='1d')
