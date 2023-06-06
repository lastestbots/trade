from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class IchimokuIndicator:
    """
    转换线 = （9天内的最高价 + 9天内的最低价）/ 2

    计算基准线（Kijun-sen）的公式为：

    基准线 = （26天内的最高价 + 26天内的最低价）/ 2

    计算云图（Senkou Span A 和 Senkou Span B）的公式为：

    Senkou Span A = （转换线 + 基准线）/ 2，向右平移26个交易日

    Senkou Span B = （52天内的最高价 + 52天内的最低价）/ 2，向右平移26个交易日

    计算滞后线（Lagging Span）的公式为：

    滞后线 = 当前收盘价，向左平移26个交易日

    计算前期高低点的平均线（Chikou Span）的公式为：

    前期高低点的平均线 = 当前收盘价，向左平移26个交易日
    """
    # 转换线周期
    tenkan_period = 9
    # 基准周期
    kijun_period = 26
    senkou_span_a_period = 26
    senkou_span_b_period = 52
    # 基准线
    tenkan_sen = None

    # 转换线
    kijun_sen = None
    # 云图 a
    senkou_span_a = None
    # 云图 b
    senkou_span_b = None

    def calculate(self, klines):
        tenkan_period = self.tenkan_period
        kijun_period = self.kijun_period
        senkou_span_a_period = self.senkou_span_a_period
        senkou_span_b_period = self.senkou_span_b_period
        if len(klines.high.get(
                size=senkou_span_b_period + senkou_span_a_period)) < senkou_span_b_period + senkou_span_a_period:
            return
        # 最高价
        tenkan_arr = sorted(klines.high.get(size=tenkan_period), reverse=True)
        self.tenkan_sen = (tenkan_arr[0] + tenkan_arr[-1]) / 2
        kijun_arr = sorted(klines.high.get(size=kijun_period), reverse=True)
        self.kijun_sen = (kijun_arr[0] + kijun_arr[-1]) / 2
        self.senkou_span_a = []
        self.senkou_span_b = []
        for i in range(senkou_span_a_period):
            ago = -senkou_span_a_period + i
            tenkan_arr = sorted(klines.high.get(ago=ago, size=tenkan_period), reverse=True)
            kijun_arr = sorted(klines.high.get(ago=ago, size=kijun_period), reverse=True)
            senkou_span_a = (tenkan_arr[0] + tenkan_arr[-1] + kijun_arr[0] + kijun_arr[-1]) / 4
            self.senkou_span_a.append(senkou_span_a)
            senkou_span_b = sorted(klines.high.get(ago=ago, size=senkou_span_b_period), reverse=True)
            self.senkou_span_b.append((senkou_span_b[0] + senkou_span_b[-1]) / 2)


class IchimokuStrategy(TemplateStrategy):

    def __init__(self):
        self.strategy_name = '一目均衡图策略'
        super().__init__()
        self.stop_loss = -2
        self.take_profit = 5

    def next(self):
        self.order_value = 0

        for klines in self.datas:
            # 交易信号

            # 仓位
            position = self.getposition(klines)
            # 股票
            symbol = SymbolUtil.klines_symbol(klines)
            # 订单大小
            order_size = (self.fetch_cash() / klines.high[0]) * (1.0 / len(self.symbols)) * 0.97
            # 指标
            indicator = IchimokuIndicator()
            indicator.calculate(klines)
            if indicator.senkou_span_b is None:
                continue
                # k线数据
            p_high = klines.high
            p_low = klines.low
            p_open = klines.open
            p_close = klines.close
            average = (p_open[0] + p_low[0] + p_high[0]) / 3
            # 做多信号
            buy_sign = False
            if average > indicator.kijun_period:
                buy_sign = True
            # 做空信号
            sell_sign = False
            if average < indicator.kijun_period:
                sell_sign = False

            # 交易规则
            if position.size == 0:
                if buy_sign:
                    self.buy(data=klines, size=order_size)
                elif sell_sign:
                    self.sell(data=klines, size=order_size)
            else:
                profit = CalculatorUtil.position_profit(position, p_close)
                if profit > self.take_profit:
                    self.log(
                        "{} \n{}\n{}".format(ColourTxtUtil.red('触发止盈'),
                                             ConsoleFormatUtil.position_str(position, klines),
                                             ConsoleFormatUtil.klines_srt(klines)))
                    self.close(data=klines)
                elif profit < self.stop_loss:
                    self.log(
                        "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损'),
                                             ConsoleFormatUtil.position_str(position, klines),
                                             ConsoleFormatUtil.klines_srt(klines)))

                    self.close(data=klines)
                elif position.size > 0 and sell_sign:
                    self.close(data=klines)
                    self.sell(data=klines, size=order_size)
                    self.log("{} 触发卖信号,反手做空".format(symbol))
                elif position.size < 0 and buy_sign:
                    self.close(data=klines)
                    self.buy(data=klines, size=order_size)
                    self.log("{} 触发买信号,反手做多".format(symbol))
