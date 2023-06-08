import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.symbol import SymbolUtil


class PriceBreakerStrategy(TemplateStrategy):

    def __init__(self):
        super().__init__()
        self.indexs = {}
        self.stop_loss = -5
        self.take_profit = 10
        self.position_ratio = 0.01
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.indexs[symbol] = {}
            self.indexs[symbol]['ema'] = bt.indicators.EMA(klines, period=200)
            self.indexs[symbol]['macd'] = bt.indicators.MACD(klines)

    def next(self):
        # 判断 MACD 线是否高于慢速线
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)

            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * 0.97
            pos = self.getposition(klines)
            # k线数据
            p_high = klines.high
            p_low = klines.low
            p_open = klines.open
            p_close = klines.close
            profit = CalculatorUtil.position_profit(pos, p_close)


