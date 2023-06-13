import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class RsiStrategy(TemplateStrategy):

    def __init__(self):
        self.strategy_name = 'RSI策略'
        super().__init__()
        self.stop_loss = -2
        self.take_profit = 5

        self.rsi_symbols = {}
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.rsi_symbols[symbol] = bt.indicators.RSI(klines, period=31)
        # 加仓比列
        self.position_ratio = 0.01

    def next(self):
        self.order_value = 0

        for klines in self.datas:
            # 交易信号
            # 仓位
            position = self.getposition(klines)
            # 股票
            symbol = SymbolUtil.klines_symbol(klines)
            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * 0.97
            # k线数据
            p_high = klines.high
            p_low = klines.low
            p_open = klines.open
            p_close = klines.close
            average = (p_open[0] + p_low[0] + p_high[0]) / 3
            # 信号
            sign = 0
            if self.rsi_symbols[symbol][0] < 10:
                sign = 1
            sell_sign = False
            if self.rsi_symbols[symbol][0] > 90:
                sign = -1

            if position.size == 0:
                size = enable_cash * self.position_ratio / p_high[0]
                if sign > 0:
                    self.buy(data=klines, size=size)
                elif sign <= 0:
                    self.sell(data=klines, size=size)

            else:
                profit = CalculatorUtil.position_profit(position, p_close)
                order_value = abs(position.size) * position.price * 2
                size = order_value / p_high[0]
                if profit > self.take_profit:
                    if order_value >= enable_cash:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止盈'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.close(data=klines)

                elif profit < self.stop_loss:
                    if order_value >= enable_cash:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.close(data=klines)
                    elif position.size > 0 and sign < 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损 加仓做多'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))

                        self.buy(data=klines, size=size)
                    elif position.size <= 0 and sign > 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损 加仓做空'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.sell(data=klines, size=size)



class RsiStrategy(TemplateStrategy):

    def __init__(self):
        self.strategy_name = 'RSI策略'
        super().__init__()
        self.stop_loss = -2
        self.take_profit = 5

        self.rsi_symbols = {}
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.rsi_symbols[symbol] = bt.indicators.RSI(klines, period=31)
        # 加仓比列
        self.position_ratio = 0.01

    def next(self):
        self.order_value = 0

        for klines in self.datas:
            # 交易信号
            # 仓位
            position = self.getposition(klines)
            # 股票
            symbol = SymbolUtil.klines_symbol(klines)
            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * 0.97
            # k线数据
            p_high = klines.high
            p_low = klines.low
            p_open = klines.open
            p_close = klines.close
            average = (p_open[0] + p_low[0] + p_high[0]) / 3
            # 信号
            sign = 0
            if self.rsi_symbols[symbol][0] < 10:
                sign = 1
            sell_sign = False
            if self.rsi_symbols[symbol][0] > 90:
                sign = -1

            if position.size == 0:
                size = enable_cash * self.position_ratio / p_high[0]
                if sign > 0:
                    self.buy(data=klines, size=size)
                elif sign <= 0:
                    self.sell(data=klines, size=size)

            else:
                profit = CalculatorUtil.position_profit(position, p_close)
                order_value = abs(position.size) * position.price * 2
                size = order_value / p_high[0]
                if profit > self.take_profit:
                    if order_value >= enable_cash:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止盈'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.close(data=klines)

                elif profit < self.stop_loss:
                    if order_value >= enable_cash:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.close(data=klines)
                    elif position.size > 0 and sign < 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损 加仓做多'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))

                        self.buy(data=klines, size=size)
                    elif position.size <= 0 and sign > 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损 加仓做空'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.sell(data=klines, size=size)