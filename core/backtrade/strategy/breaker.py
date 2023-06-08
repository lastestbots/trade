from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.symbol import SymbolUtil


class BreakerStrategy(TemplateStrategy):
    def __init__(self):
        self.strategy_name = 'Breaker '
        super().__init__()
        # 持仓时间
        self.hold_pos_day = {}
        self.stop_loss = -5
        self.take_profit = 10
        self.position_ratio = 0.01
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
        self.stop_loss = -5
        self.take_profit = 10
        self.position_ratio = 0.01
        self.ema_period = 200
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.hold_pos_day[symbol] = 0

    def next(self):

        breaker = 5
        for klines in self.datas:

