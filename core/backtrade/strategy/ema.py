import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class EMAStrategy(TemplateStrategy):

    def __init__(self):
        super().__init__()
        self.indexs = {}
        self.stop_loss = -5
        self.take_profit = 15
        self.position_ratio = 0.01
        self.ema_period = 200
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.indexs[symbol] = {}
            self.indexs[symbol]['ema'] = bt.indicators.EMA(klines, period=self.ema_period)
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
            # 指标
            ema = self.indexs[symbol]['ema']
            macd = self.indexs[symbol]['macd']
            sign = 0
            if p_close[0] > ema[0] and macd.lines.macd[0] > macd.lines.signal[0] > 0:
                sign = 1
            elif p_close[0] < ema[0] and macd.lines.macd[0] < macd.lines.signal[0] < 0:
                sign = -1
            # if p_close[0] > ema[0]:
            #     sign = 1
            # elif p_close[0] < ema[0]:
            #     sign = -1

            if pos.size == 0:
                size = enable_cash / klines.high[0] * 0.95 * self.position_ratio
                if sign == 1:
                    self.buy(data=klines, size=size)
                elif sign == -1:
                    self.sell(data=klines, size=size)
            else:
                order_value = abs(pos.size) * pos.price
                if profit < -50:
                    self.log(ColourTxtUtil.red("{} 强制止损 ".format(symbol)))
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


class EMAV2Strategy(TemplateStrategy):

    def __init__(self):
        super().__init__()
        self.indexs = {}
        self.stop_loss = -10
        #
        self.take_profit_value = self.broker.cash * 0.1
        self.position_ratio = 1
        self.ema_period = 100
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.indexs[symbol] = {}
            self.indexs[symbol]['ema'] = bt.indicators.EMA(klines, period=self.ema_period)
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
            # 指标
            ema = self.indexs[symbol]['ema']
            macd = self.indexs[symbol]['macd']
            sign = 0
            if p_close[0] > ema[0] and macd.lines.macd[0] > macd.lines.signal[0] > 0:
                sign = 1
            elif p_close[0] < ema[0] and macd.lines.macd[0] < macd.lines.signal[0] < 0:
                sign = -1
            # if p_close[0] > ema[0]:
            #     sign = 1
            # elif p_close[0] < ema[0]:
            #     sign = -1

            if pos.size == 0:
                size = enable_cash / klines.high[0] * 0.95 * self.position_ratio
                if sign == 1:
                    self.buy(data=klines, size=size)
                elif sign == -1:
                    self.sell(data=klines, size=size)
            else:
                profit_value = profit * pos.price * abs(pos.size)

                order_value = abs(pos.size) * pos.price
                if profit < -50:
                    self.log(ColourTxtUtil.red("{} 强制止损 ".format(symbol)))
                    self.close(data=klines)
                elif profit_value > self.take_profit_value:
                    self.close(data=klines)

                elif profit < self.stop_loss:
                    if order_value > enable_cash:
                        continue
                    elif pos.size > 0 and sign > 0:
                        self.buy(data=klines, size=order_value)
                    elif pos.size < 0 and sign < 0:
                        self.sell(data=klines, size=order_value)


class SimpleEmaStrategy(TemplateStrategy):

    def __init__(self):
        super().__init__()
        self.indexs = {}
        self.stop_loss = -5
        self.take_profit = 15
        self.position_ratio = 0.1
        self.ema_period = 200
        self.breaker_change = 5
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.indexs[symbol] = {}
            self.indexs[symbol]['ema'] = bt.indicators.EMA(klines, period=self.ema_period)

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
            # 指标
            ema = self.indexs[symbol]['ema']
            price_change = (p_close[0] - p_open[0]) / p_open[0] * 100
            sign = 0
            if p_close[0] > ema[0] and price_change > self.breaker_change:
                sign = 1
            elif p_close[0] < ema[0] and price_change < -self.breaker_change:
                sign = -1
            if pos.size == 0:
                size = enable_cash / klines.high[0] * 0.95 * self.position_ratio
                if sign == 1:
                    self.buy(data=klines, size=size)
                elif sign == -1:
                    self.sell(data=klines, size=size)
            else:
                order_value = abs(pos.size) * pos.price
                if profit < -50:
                    self.log(ColourTxtUtil.red("{} 强制止损 ".format(symbol)))
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
