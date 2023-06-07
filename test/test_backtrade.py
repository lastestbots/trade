# 多周期
# 买入条件：日MACD金叉、周RSI小于50
# 卖出条件：价格较最高收盘价回撤5%卖出
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import backtrader as bt
import backtrader.indicators as btind
import pandas as pd

from core.backtrade.feeds.cctx import CCxtPdData
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.ccxt_util import OhlvUtil


class RSIMACDMultiTF(bt.Strategy):
    params = (
        ('trailamount', 0.0),
        ('trailpercent', 0.05),
    )

    def __init__(self):
        # 存储不同数据的技术指标
        self.inds = dict()
        # 存储特定股票的订单，key为股票的代码
        self.orders = dict()
        # 遍历所有数据
        for i, d in enumerate(self.datas):
            self.orders[d._name] = None
            # 为每个数据定义字典，存储技术指标
            self.inds[d] = dict()
            # 判断d是否为日线数据
            if 0 == i % 2:
                self.inds[d]['crossup'] = btind.CrossUp(btind.MACD(d).macd, btind.MACD(d).signal)
            # d为周线数据
            else:
                self.inds[d]['rsi'] = btind.RSI_Safe(d)

    def next(self):
        # print(self.datetime.date())
        print("")
        for i, d in enumerate(self.datas):
            # 如果处理周线数据则跳过买卖条件，因为已在日线数
            # 据判断处理过
            klines_str = ConsoleFormatUtil.klines_str(d)
            symbol = SymbolUtil.klines_symbol(d)
            print(d._name, klines_str)

            if 1 == i % 2:
                continue
            pos = self.getposition(d)
            # 不在场内，则可以买入
            if not len(pos):
                # 达到买入条件
                if self.inds[d]['crossup'][0] and self.inds[self.datas[i + 1]]['rsi'][0] < 50:
                    # 买入手数，如果是多只股票回测，这里需要修改
                    stake = int(self.broker.cash // (d.close[0] * 100)) * 100
                    # 买买买
                    self.buy(data=d, size=stake)
            elif not self.orders[d._name]:
                # 下保护点卖单
                self.orders[d._name] = self.close(data=d, exectype=bt.Order.StopTrail,
                                                  trailamount=self.p.trailamount,
                                                  trailpercent=self.p.trailpercent)

    def notify_order(self, order):

        if order.status in [order.Completed]:
            if order.isbuy():
                print('{} BUY {} EXECUTED, Price: {:.2f}'.format(self.datetime.date(), order.data._name,
                                                                 order.executed.price))
            else:  # Sell
                self.orders[order.data._name] = None
                print('{} SELL {} EXECUTED, Price: {:.2f}'.format(self.datetime.date(), order.data._name,
                                                                  order.executed.price))


# 加载数据
def load_data(symbol, timeframe):
    fromdate = datetime.datetime(2022, 1, 1)
    todate = datetime.datetime(2023, 6, 1)

    klines = OhlvUtil.load_ohlv_as_pd(symbol=symbol, timeframe=timeframe, start=fromdate,
                                      end=todate)
    klines['Time'] = pd.to_datetime(klines['Time'])
    klines.set_index('Time', inplace=True)

    return CCxtPdData(dataname=klines)


def runstrat():
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000.0)
    cerebro.addstrategy(RSIMACDMultiTF)
    for symbol in ['ETHUSDT', 'OPUSDT']:
        for timeframe in ['1h', '1d']:
            data = load_data(symbol, timeframe)
            cerebro.adddata(data, name=symbol)
    cerebro.addwriter(bt.WriterFile, out='log.csv', csv=True)
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Plot the result绘制结果
    # cerebro.plot(start=datetime.date(2018, 1, 1), end=datetime.date(2019, 12, 31),
    #              volume=False, style='candle',
    #              barup='red', bardown='green')


if __name__ == '__main__':
    runstrat()
