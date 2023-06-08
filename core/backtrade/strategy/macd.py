import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.symbol import SymbolUtil


class MacdStrategy(TemplateStrategy):

    def __init__(self):
        super().__init__()
        self.indexs = {}
        self.stop_loss = -5
        self.take_profit = 10
        self.position_ratio = 0.01
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.indexs[symbol] = {}
            self.indexs[symbol]['macd'] = bt.indicators.MACD(klines)

    def next(self):
        # 判断 MACD 线是否高于慢速线
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            macd = self.indexs[symbol]['macd']
            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * 0.97
            pos = self.getposition(klines)
            # k线数据
            p_high = klines.high
            p_low = klines.low
            p_open = klines.open
            p_close = klines.close
            profit = CalculatorUtil.position_profit(pos, p_close)
            sign = 0
            if macd.lines.macd[0] > macd.lines.signal[0] > 0:
                sign = 1
            elif macd.lines.macd[0] < macd.lines.signal[0] < 0:
                sign = -1

            if pos.size == 0:
                size = enable_cash / klines.high[0] * 0.95 * self.position_ratio
                if sign == 1:
                    self.buy(data=klines, size=size)
                elif sign == -1:
                    self.sell(data=klines, size=size)
            else:
                order_value = abs(pos.size) * pos.price
                if profit < max(self.stop_loss * 2, -60):

                    self.close(data=klines)
                elif profit > self.take_profit:
                    self.close(data=klines)
                elif profit < self.stop_loss:
                    if order_value > enable_cash:
                        continue
                    elif pos.size > 0 and sign > 0:
                        self.buy(data=klines, size=order_value)
                    elif pos.size < 0 and sign < 0:
                        self.sell(data=klines, size=order_value)
