import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil


class BollStrategy(TemplateStrategy):

    def __init__(self):
        super().__init__()
        # boll 周期
        boll_period = 20
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.index = {}
        # 开仓比列
        self.pos_ratio = 0.1
        for data in self.datas:
            self.index[data] = {}
            boll = bt.indicators.BollingerBands(data, period=boll_period)
            self.index[data]['boll_top'] = boll.top
            self.index[data]['boll_bot'] = boll.bot

    def next(self):
        for data in self.datas:
            index = self.index[data]
            top = index['boll_top']
            bot = index['boll_bot']
            # 可用资金
            enable_cash = self.fetch_cash() * (1.0 / len(self.symbols)) * self.pos_ratio
            pos = self.getposition(data)
            # k线数据
            p_high = data.high
            p_low = data.low
            p_open = data.open
            p_close = data.close
            price_change = (p_close[0] - p_open[0]) / p_close[0] * 100
            if price_change > 5 and pos.size == 0:
                # 执行买入
                size = enable_cash / p_high[0]
                self.buy(data=data, size=size)
                self.index[data]['price_change'] = price_change
            elif pos.size != 0:
                # 利润
                profit = CalculatorUtil.position_profit(pos, p_close)
                # 加仓大小
                order_value = abs(pos.size) * pos.price
                if profit > 20 or profit < -10 or profit > self.index[data]['price_change']:
                    self.close(data=data)
                    self.index[data]['price_change'] = 0
                elif order_value > enable_cash:
                    continue
                elif price_change > 5:
                    size = order_value / p_high[0] * 0.98
                    self.buy(data=data, size=size)
