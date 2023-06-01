from config.config import TradeConfig
from core.backtrade.client.runner import StrategyRunner
from core.backtrade.strategy.spot import SpotStrategy


class SpotTradeClient(StrategyRunner):
    """
    现货实盘模拟交易客户端
    """
    # 加载数据
    klines = None
    config: TradeConfig = None
    cerebro = None

    def __init__(self):
        super().__init__()
        self.config.strategy = SpotStrategy
