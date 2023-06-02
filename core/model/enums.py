from enum import Enum

from core.backtrade import BackTradeConfig


class OrderSide(Enum):
    """
    订单方向
    """

    Buy = 'B'
    Sell = 'S'

    @property
    def command(self):
        return self.value

    def is_buy(self) -> bool:
        return self.value == OrderSide.Buy.value

    def is_sell(self) -> bool:
        return self.value == OrderSide.Sell.value


class OrderType(Enum):
    """
    订单类型
    """
    Market = 'M'
    Limit = 'L'
    @property
    def command(self):
        return self.value
    def is_market(self) -> bool:
        return self.value == OrderType.Market.value

    def is_limit(self) -> bool:
        return self.value == OrderType.Limit.value


class AnalyzerType(Enum):
    ConsoleAnalyzer = 'ConsoleAnalyzer'
    PyfolioReportAnalyzer = 'PyfolioReportAnalyzer'

    @property
    def target_class(self):
        return BackTradeConfig.fetch_strategy_analyzer(self.value)

    @staticmethod
    def value_of(analyzer):
        return AnalyzerType[analyzer]
