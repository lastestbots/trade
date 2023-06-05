import backtrader as bt


class RBreakerIndicator(bt.Indicator):
    lines = ('myline',)

    def __init__(self):
        self.lines.myline = self.data.high - self.data.low

# cerebro = bt.Cerebro()
# data = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2011, 1, 1), todate=datetime(2012, 12, 31))
# cerebro.adddata(data)
#
# indicator = MyIndicator()
# cerebro.addindicator(indicator)
#
# cerebro.run()
# cerebro.plot()
