import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy


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
        for data in self.datas:
            self.index[data] = {}
            boll = bt.indicators.BollingerBands(data, period=boll_period)
            self.index[data]['boll_top'] = boll.top
            self.index[data]['boll_bot'] = boll.bot

    def next(self):
        pass
