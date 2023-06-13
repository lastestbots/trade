from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class BreakerIndicator:
    def __init__(self, average_period=5, breaker=3):
        self.sign = 0
        self.average_change = 0
        self.price_change = 0
        self.period = average_period
        self.breaker = breaker

    def compute(self, klines):

        if len(klines.high.get(
                size=self.breaker * 2)) < self.breaker * 2:
            self.sign = 0
            return

        open_price = klines.open
        close_price = klines.close
        average_change = 0
        for i in range(self.period - 1):
            average_change += (close_price[-i - 1] - open_price[-i - 1]) / open_price[-i - 1] * 100

        self.average_change /= self.period
        self.price_change = (close_price[0] - open_price[0]) / open_price[0] * 100
        if abs(average_change) < 0.01 or abs(self.price_change) > 1:
            self.sign = 0
        if abs(self.price_change) > self.breaker * abs(average_change):
            if self.price_change > 0:
                self.sign = 1
            elif self.price_change < 0:
                self.sign = -1

        else:
            self.sign = 0


class BreakerStrategy(TemplateStrategy):
    def __init__(self):
        self.strategy_name = 'Breaker '
        super().__init__()
        # 持仓时间
        self.hold_pos_day = {}
        self.stop_loss = -20
        self.take_profit = 10
        self.position_ratio = 1
        self.ema_period = 200
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.hold_pos_day[symbol] = 0

    def next(self):
        max_hold_day = 30
        breaker = 5
        for klines in self.datas:
            pos = self.getposition(klines)

            symbol = SymbolUtil.klines_symbol(klines)
            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * 0.97

            # k线数据
            p_high = klines.high
            p_low = klines.low
            p_open = klines.open
            p_close = klines.close
            size = enable_cash / p_high[0]

            profit = CalculatorUtil.position_profit(pos, p_close)
            if pos.size != 0:
                self.hold_pos_day[symbol] += 1
            if pos.size == 0:
                price_change = (p_close[0] - p_open[0]) / p_open[0] * 100
                if price_change > breaker:
                    self.buy(data=klines, size=size)
                elif price_change < -breaker:
                    self.sell(data=klines, size=size)
            elif self.hold_pos_day[symbol] >= max_hold_day - 1:
                self.close(data=klines)
                self.hold_pos_day[symbol] = 0
            # elif profit > self.take_profit:
            #     self.close(data=klines)
            #     self.hold_pos_day[symbol] = 0
            elif profit < self.stop_loss:
                self.close(data=klines)
                self.hold_pos_day[symbol] = 0


class AverageBreakerStrategy(TemplateStrategy):
    def __init__(self):
        self.strategy_name = 'Breaker '
        super().__init__()
        # 持仓时间
        self.hold_pos_day = {}
        self.stop_loss = -20
        self.take_profit = 10
        self.position_ratio = 0.05
        self.ema_period = 200
        self.pos = {}
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.pos[symbol] = {}
            self.pos[symbol]['hold_day'] = 0
        self.average_period = 5
        self.breaker = 3

    def trade(self):

        self.order_value = 0
        for klines in self.datas:
            index = BreakerIndicator()
            index.compute(klines)
            sign = index.sign

            high_price = klines.high
            close_price = klines.close
            pos = self.getposition(klines)

            symbol = SymbolUtil.klines_symbol(klines)
            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * 0.97

            if pos.size != 0:
                self.pos[symbol]['hold_day'] += 1

            if pos.size == 0:

                size = enable_cash / high_price[0] * self.position_ratio
                if sign > 0:
                    self.buy(data=klines, size=size)

                    self.order_value += enable_cash
                # if sign < 0:
                #     self.sell(data=klines, size=size)
                #
                #     self.order_value += enable_cash
            else:
                profit = CalculatorUtil.position_profit(pos, close_price)

                order_value = abs(pos.size) * pos.price
                size = order_value / high_price[0]

                if profit > abs(index.breaker):
                    self.close(data=klines)

                elif profit > self.take_profit:
                    self.log(ColourTxtUtil.red("强迫止盈"))
                    self.close(data=klines)
                elif profit < self.stop_loss:
                    if profit < -60:
                        self.close(data=klines)
                        self.log(ColourTxtUtil.red("强迫止损"))
                        continue
                    if order_value > enable_cash:
                        # self.show_trade_info()
                        # self.log(ColourTxtUtil.red("现金不足、金额不足"))
                        continue
                    elif pos.size > 0 and sign > 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('加仓做多'),
                                                 ConsoleFormatUtil.position_str(pos, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))

                        self.buy(data=klines, size=size)
                    elif pos.size <= 0 and sign < 0:
                        self.log(
                            "{} \n{}\n{}".format(ColourTxtUtil.red('加仓做空'),
                                                 ConsoleFormatUtil.position_str(pos, klines),
                                                 ConsoleFormatUtil.klines_str(klines)))
                        self.sell(data=klines, size=size)

    def show_price_change(self):
        period = 5
        breaker = 3
        for klines in self.datas:

            if len(klines.high.get(
                    size=period * 2)) < period * 2:
                return
            open_price = klines.open.get(size=period * 2, )
            close_price = klines.close.get(size=period * 2, )
            average_change = 0
            for i in range(period):
                average_change += (close_price[i] - open_price[i]) / open_price[i] * 100

            average_change /= period
            price_change = (close_price[period] - open_price[period]) / open_price[period] * 100

            if abs(price_change) > breaker * abs(average_change):
                symbol = SymbolUtil.klines_symbol(klines)
                self.log("{} {} {}".format(symbol, round(average_change, 2), round(price_change, 2)))
                log_info = ''
                for i in range(period):
                    pc = (close_price[i + period - 1] - open_price[i + period - 1]) / open_price[
                        i + period - 1] * 100
                    log_info += ' {} '.format(round(pc, 2))
                self.log("{} {}\n".format(symbol, log_info))

    def next(self):
        # self.show_price_change()
        self.trade()


class AddPositionTrade:

    def trade(self, strategy):
        pass
