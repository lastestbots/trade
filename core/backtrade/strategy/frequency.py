import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class SupportResistanceIndicator:
    period = 12 * 6
    refer = 3
    """
    支撑位
    """
    support = None

    """
    压力位
    """
    resistence = None

    def __init__(self):
        self.resistence = None
        self.support = None
        self.buy_sign = False
        self.sell_sign = False

    def calc(self, klines):
        if len(klines.high.get(size=self.period)) < 2:
            return
        low = klines.low.get(ago=-1, size=self.period)
        high = klines.high.get(ago=-1, size=self.period)
        # 按降序排列
        sorted_arr = sorted(high, reverse=True)
        self.resistence = sum(sorted_arr[:self.refer]) / self.refer
        sorted_arr = sorted(low, reverse=False)
        self.support = sum(sorted_arr[:self.refer]) / self.refer

        if - 0.002 < (self.resistence - klines.high[0]) / klines.high[0] < 0.002:
            self.sell_sign = True

        elif - 0.002 < (self.support - klines.low[0]) / klines.low[0] < 0.002:
            self.buy_sign = True


class HighFrequencyStrategy(TemplateStrategy):

    def __init__(self):
        self.strategy_name = '高频策略'
        super().__init__()

    def next(self):
        # self.show_trade_info()

        for klines in self.datas:
            indicator = SupportResistanceIndicator()
            indicator.calc(klines)
            if indicator.resistence is None:
                return
            symbol = SymbolUtil.klines_symbol(klines)
            cash = self.fetch_cash() / len(self.symbols)
            position = self.getposition(klines)
            # order = self.fetch_order(symbol)
            # if order is not None:
            #     continue
            if position.size == 0:
                if indicator.buy_sign:
                    self.buy(data=klines, size=cash / klines.close[0] * 0.98, exectype=bt.Order.Market)

                elif indicator.sell_sign:
                    self.sell(data=klines, size=cash / klines.close[0] * 0.98, exectype=bt.Order.Market)

            else:
                profit = CalculatorUtil.position_profit(position, klines.close[0])

                if profit > 10:
                    self.log(
                        "{} {}".format(ColourTxtUtil.red('触发止盈'),
                                       ConsoleFormatUtil.position_str(position, klines)))
                    self.close(data=klines)
                elif profit < -5:
                    self.log(
                        "{} {}".format(ColourTxtUtil.red('触发止损'),
                                       ConsoleFormatUtil.position_str(position, klines)))
                    self.close(data=klines)
                elif indicator.buy_sign and position.price < 0:
                    self.close(data=klines, )
                elif indicator.sell_sign and position.price > 0:
                    self.sell(data=klines)

    def stop(self):
        self.log("{} {}".format(ColourTxtUtil.red('手续费 '), self.trade_free_cost), islog=True)
