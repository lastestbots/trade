from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class AverageChannelIndicator:

    def __init__(self):
        self.up_channel = 0
        self.down_channel = 0

    def calculate(self, klines, period=40):
        if len(klines.high.get(size=period)) < period:
            return
        up_num = 0
        down_num = 0
        open_price = klines.open.get(size=period)
        close_price = klines.close.get(size=period)
        for i in range(period):
            change = (close_price[i] - open_price[i]) / open_price[i] * 100
            if change > 0:
                self.up_channel += change
                up_num += 1
            elif change < 0:
                self.down_channel += change
                down_num += 1

        self.down_channel /= down_num
        self.up_channel /= up_num


class ChannelStrategy(TemplateStrategy):

    def __init__(self):
        super().__init__()
        self.stop_loss = -20
        self.take_profit = 20
        self.position_ratio = 0.9

        account = ConsoleFormatUtil.account_str(self.broker)
        self.log(account, islog=True)

    def next(self):
        # 调整可用资金
        # if self.wallet <= 2 * self.broker.cash and self.broker.cash > self.init_cash:
        #     self.wallet += self.broker.cash * 0.5
        #     self.broker.cash = self.broker.cash * 0.5
        self.order_value = 0
        channel_period = 20
        stop_loss = self.stop_loss
        take_profit = self.take_profit
        position_ratio = self.position_ratio
        for klines in self.datas:
            # 计算指标
            indicator = AverageChannelIndicator()
            indicator.calculate(klines, period=channel_period)
            sign = 0
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
            change = (p_close[0] - p_open[0]) / p_open[0] * 100
            if change > indicator.up_channel:
                sign = 1
            elif change < indicator.down_channel:
                sign = -1
            if position.size == 0:
                size = enable_cash * position_ratio / p_high[0]
                if sign > 0:
                    self.buy(data=klines, size=size)
                    self.order_value += enable_cash
            else:
                profit = CalculatorUtil.position_profit(position, p_close)

                order_value = abs(position.size) * position.price
                size = order_value / p_high[0]
                if profit > take_profit:
                    self.close(data=klines)
                elif profit < stop_loss:
                    if profit < -60:
                        self.close(data=klines)
                        continue
                    if order_value > enable_cash:
                        self.show_trade_info()
                        self.log(ColourTxtUtil.red("现金不足、金额不足"))
                    elif position.size > 0 and sign < 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损 加仓做多'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))

                        self.buy(data=klines, size=size)
                    elif position.size <= 0 and sign < 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('触发止损 加仓做空'),
                                                 ConsoleFormatUtil.position_str(position, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.sell(data=klines, size=size)


            # 检查账户保证金是否充足
            profit = CalculatorUtil.position_profit(position, p_close)
            if profit <= -100:
                self.show_trade_info()
                # 保证金不足，暂停策略并发出警告消息
                self.notifier.warning(
                    f"保证金不足, cash: {self.broker.get_cash()}, profit: {profit}")
                self.broker.runstop()

    def stop(self):
        self.show_trade_info(islog=True)
