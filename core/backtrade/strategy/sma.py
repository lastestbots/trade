import backtrader as bt

from core.backtrade.strategy.ichimoku import IchimokuIndicator
from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class SmaStrategy(TemplateStrategy):
    # 定义参数
    params = (
        ('trailamount', 0.0),
        ('trailpercent', 0.05),
    )

    def __init__(self):
        self.strategy_name = 'SMA策略'
        super().__init__()
        # 存储不同数据的技术指标
        self.inds = dict()
        # 存储特定股票的订单，key为股票的代码
        self.orders = dict()
        # 遍历所有数据
        for i, klines in enumerate(self.datas):
            symbol = SymbolUtil.klines_symbol(klines)

            # 为每个数据定义字典，存储技术指标
            self.inds[symbol] = dict()
            # 判断d是否为小周期
            if 0 == i % 2:
                self.inds[symbol]['rsi'] = bt.indicators.ExponentialMovingAverage(klines, period=30)
            # d为大周期
            else:
                ema = bt.indicators.ExponentialMovingAverage(klines, period=30)
                # 趋势
                self.inds[symbol]['trend'] = bt.indicators.CrossOver(klines.close, ema)
        self.stop_loss = -2
        self.take_profit = 2
        # 加仓比列
        self.position_ratio = 0.01

    def next(self):
        for i, klines in enumerate(self.datas):
            # 如果处理周线数据则跳过买卖条件，因为已在日线数
            # 据判断处理过
            if 1 == i % 2:
                continue
            # k线数据
            p_high = klines.high
            p_low = klines.low
            p_open = klines.open
            p_close = klines.close
            # 股票
            symbol = SymbolUtil.klines_symbol(klines)
            # 仓位
            position = self.getposition(klines)
            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * 0.97
            #  一目均衡=
            indicator = IchimokuIndicator()
            indicator.calculate(klines)
            # 交易信息
            sign = 0
            # 趋势
            trend = self.inds[symbol]['trend'][0]
            if trend > 0 and indicator.tenkan_period > indicator.kijun_sen:
                sign = 1
            elif trend < 0 and indicator.tenkan_period < indicator.kijun_sen:
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
                    self.close(data=klines)
                elif profit < self.take_profit:
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
                    elif position.size > 0 and trend < 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('趋势看空 平多'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.close(data=klines)
                    elif position.size < 0 and trend > 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('趋势看多 平空'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.close(data=klines)
