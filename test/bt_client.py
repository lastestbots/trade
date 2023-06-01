import unittest

from core.bt.client.mock import MockSpotTradeClient


class TestMockConfig(unittest.TestCase):

    def test_load_data(self):
        MockSpotTradeClient().load_data()

