import backtrader as bt
import pandas as pd

from core.backtrade.feeds.cctx import CCxtPdData
from core.backtrade.strategy.mock import MockSpotStrategy
from core.utils.ccxt_util import OhlvUtil


class SMACrossOver(bt.Strategy):
    params = (('pfast', 10), ('pslow', 30), ('printlog', True))

    def log(self, txt, dt=None, do_print=True):
        if self.params.printlog or do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        self.dataclose = self.datas[0].close
        self.sma_fast = bt.indicators.SMA(self.datas[0], period=self.params.pfast)
        self.sma_slow = bt.indicators.SMA(self.datas[0], period=self.params.pslow)
        self.rsi = bt.indicators.RSI(self.datas[0], period=14)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status == order.Completed:
            self.log('%s %s' % ('BUY' if order.isbuy() else 'SELL', order.executed.price), do_print=True)
        elif order.status == order.Canceled:
            self.log('Order Canceled', do_print=True)
        elif order.status == order.Margin:
            self.log('Order Margin Call', do_print=True)
        elif order.status == order.Rejected:
            self.log('Order Rejected', do_print=True)

    def next(self):
        if self.position:
            if self.dataclose < self.sma_fast:
                self.sell()
        else:
            if self.dataclose > self.sma_slow and self.rsi < 30:
                self.buy()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.001)
    klines = OhlvUtil.load_ohlv_as_pd('ETHUSDT', '1d')
    klines['Time'] = pd.to_datetime(klines['Time'])
    klines.set_index('Time', inplace=True)
    data = CCxtPdData(dataname=klines)
    cerebro.adddata(data)
    cerebro.addstrategy(MockSpotStrategy)
    cerebro.run()
