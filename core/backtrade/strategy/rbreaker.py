import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class RBreakerIndicator:

    def __init__(self, params=None):
        self.b_break = 0
        self.s_setup = 0
        self.s_enter = 0
        self.b_enter = 0
        self.b_setup = 0
        self.s_break = 0

    def calculate(self, klines):
        if len(klines.high.get(size=2)) < 2:
            return
        # 前一日最高价
        ph = klines.high.get(size=2)[0]
        # 前一日最低价
        pl = klines.low.get(size=2)[0]
        # 前一日收盘价
        pc = klines.close.get(size=2)[0]

        pivot = (pc + pl + ph) / 3

        # 第一组 突破买入价 全场最高
        self.b_break = ph + 2 * (pivot - pl)
        # 第二组 观察卖出价 多单叛变条件1
        self.s_setup = pivot + (ph - pl)
        # 第二组 反转卖出价 多单叛变条件2
        self.s_enter = 2 * pivot - pl
        # 第三组 反转买入价 空单叛变条件2
        self.b_enter = 2 * pivot - ph
        # 第三组 观察买入价 空单叛变条件1
        self.b_setup = pivot - (ph - pl)
        # 第一组 突破卖出价 全场最低
        self.s_break = pl - 2 * (ph - pivot)


class RBreakerStrategy(TemplateStrategy):
    params = (

        ('profit_target', 0.06),
        ('stop_loss', 0.02),
    )

    def __init__(self):
        super().__init__()
        self.log(ColourTxtUtil.red("RBreaker 策略"))

        self.take_profit = None
        self.stop_loss = None

    def next(self):
        self.order_value = 0
        for klines in self.datas:
            self.trade(klines)

    def trade(self, klines):
        indicator = RBreakerIndicator()
        indicator.calculate(klines)
        if indicator.b_enter == 0:
            return

        high = klines.high[0]
        low = klines.low[0]
        average = (klines.high[0] + klines.open[0] * 2 + klines.low[0]) / 4
        cash = self.fetch_cash()
        symbol = SymbolUtil.klines_symbol(klines)
        order_size = (cash / klines.close[0]) * (1.0 / len(self.symbols)) * 0.97
        position = self.getposition(klines)
        if position.size != 0:

            profit = CalculatorUtil.position_profit(position, klines.close[0])
            if profit > self.p.profit_target or profit > self.p.profit_target:
                self.close(data=klines)
                return
            if position.size > 0:
                if high > indicator.s_setup and average < indicator.s_enter:
                    # 多头持仓,当日内最高价超过观察卖出价后，
                    # 盘中价格出现回落，且进一步跌破反转卖出价构成的支撑线时，
                    # 采取反转策略，即在该点位反手做空
                    self.log("{} 多头持仓,当日内最高价超过观察卖出价后跌破反转卖出价: 反手做空".format(symbol))
                    self.close(data=klines)
                    self.sell(exectype=bt.Order.Market, size=order_size, data=klines)
            elif position.size < 0:

                if low < indicator.b_setup and average > indicator.b_enter:
                    # 空头持仓，当日内最低价低于观察买入价后，
                    # 盘中价格出现反弹，且进一步超过反转买入价构成的阻力线时，
                    # 采取反转策略，即在该点位反手做多
                    self.log("{} 空头持仓,当日最低价低于观察买入价后超过反转买入价: 反手做多".format(symbol))
                    self.close(data=klines)
                    self.buy(exectype=bt.Order.Market, size=order_size, data=klines)

        else:
            # 空仓条件

            if average > indicator.b_break:
                self.log("{} 空仓,盘中价格超过突破买入价: 开仓做多".format(symbol))
                self.buy(size=order_size, exectype=bt.Order.Market, data=klines)
            elif average < indicator.s_break:
                # 在空仓的情况下，如果盘中价格跌破突破卖出价，
                # 则采取趋势策略，即在该点位开仓做空
                self.log("{}空仓,盘中价格跌破突破卖出价: 开仓做空".format(symbol))
                self.buy(size=order_size, exectype=bt.Order.Market, data=klines)
