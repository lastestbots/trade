import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class TurtleStrategy(TemplateStrategy):
    """
    海龟策略
    """
    params = dict(
        N1=40,  # 唐奇安通道上轨的t
        N2=30,  # 唐奇安通道下轨的t
        ATR_T=40,  # ATR的周期T
        printlog=False,
        risk=0.03,

    )

    def __init__(self):
        self.strategy_name = '唐奇安通道策略'
        super().__init__()
        self.indicators = {}


        for klines in self.datas:
            # 第一个标的沪深300主力合约的close、high、low 行情数据
            close = klines.close
            high = klines.high
            low = klines.low
            # 计算唐奇安通道上轨：过去最高价
            donchian_h = bt.ind.Highest(high(-1), period=self.p.N1)
            # 计算唐奇安通道下轨：过去最低价
            donchian_l = bt.ind.Lowest(low(-1), period=self.p.N2)

            # ATR
            atr = bt.ind.AverageTrueRange(klines, period=self.p.ATR_T)

            symbol = SymbolUtil.klines_symbol(klines)
            indicator = {'atr': atr,
                         'donchian_h': donchian_h,
                         'donchian_l': donchian_l,

                         }

            self.indicators[symbol] = indicator

    def next(self):
        self.order_value = 0

        for klines in self.datas:
            self.trade(klines)

    def trade(self, klines):
        symbol = SymbolUtil.klines_symbol(klines)
        # indicator
        donchian_h = self.indicators[symbol]['donchian_h']
        donchian_l = self.indicators[symbol]['donchian_l']
        atr = self.indicators[symbol]['atr']
        # klines
        pc = klines.close
        po = klines.open
        pl = klines.low
        ph = klines.high

        cash = self.fetch_cash() / len(self.symbols)
        position = self.getposition(klines)

        p_size = cash / ph[0]
        risk = self.p.risk

        if position.size == 0:
            if po[0] < donchian_l[-1]:
                price = pc[0] + 2 * atr[0]
                self.sell(data=klines, size=p_size, price=price, exectype=bt.Order.Limit)
            elif po[0] > donchian_h[-1]:
                price = pc[0] - 2 * atr[0]
                self.sell(data=klines, size=p_size, price=price, exectype=bt.Order.Limit)

        else:
            profit = CalculatorUtil.position_profit(position, pc[0])
            if profit > risk * 3 or profit < -risk * 1.5:
                self.close(data=klines)
            if position.size > 0:
                if po[0] < donchian_l[-1]:
                    self.close(data=klines)
            elif position.size < 0:

                if po[0] > donchian_h[-1]:
                    self.close(data=klines)
