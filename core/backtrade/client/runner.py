import backtrader as bt
import pandas as pd
from loguru import logger

from config.config import TradeConfig
from core.backtrade.feeds.cctx import CCxtPdData
from core.utils.ccxt_util import OhlvUtil


class RiskSizer(bt.Sizer):
    def __init__(self):
        self.params.override = True

    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            risk = 0.02
            risk_factor = data.close[0] - data.low[0]
        else:
            risk = 0.01
            risk_factor = data.high[0] - data.close[0]
        return int((cash * risk / risk_factor) // 100 * 100)


class StrategyRunner:
    """

    """

    klines = None
    config = None
    cerebro = None

    def __init__(self):
        self.config = TradeConfig()

    def set_strategy(self, strategy):
        self.config.strategy = strategy

    def run(self):
        logger.debug("运行策略：{}".format(self.config.strategy))
        config = self.config
        if config.analyzers is None:
            raise ValueError("未配置分析器")
        # 加载backtrader引擎
        cerebro = self.load_cerebro(config)
        for analyzer in config.analyzers:
            analyzer.target_class.execute(cerebro, self.config)

    def load_data(self):
        config = self.config
        self.klines = {}
        for symbol in config.trade_symbols:
            self.klines[symbol] = []

            for timeframe in config.trade_timeframes:
                klines = OhlvUtil.load_ohlv_as_pd(symbol=symbol, timeframe=timeframe, start=config.trade_from_time,
                                                  end=config.trade_to_time)
                klines['Time'] = pd.to_datetime(klines['Time'])
                klines.set_index('Time', inplace=True)

                self.klines[symbol].append(klines)

                self.cerebro.adddata(data=CCxtPdData(dataname=klines),
                                     name=symbol)

        #

    def load_cerebro(self, config, is_reload=False):
        if self.cerebro is not None and not is_reload:
            return self.cerebro
        if config.strategy is None:
            return ValueError("策略为空")

        cerebro = bt.Cerebro()
        # 是否可以做空
        cerebro.broker.set_shortcash(config.enable_shore)
        # 策略加进来
        # todo 不同风险策略
        # cerebro.addsizer(bt.sizers.FixedSize, stake=1)
        # 设置以收盘价成交，作弊模式
        cerebro.broker.set_coc(config.trade_enable_coc)
        # 设置初始资金
        cerebro.broker.set_cash(config.account_balance)
        cerebro.broker.set_slippage_fixed(config.trade_shipping_fixed)
        # 设置手续费
        cerebro.broker.setcommission(commission=config.account_fee)
        # 设置运行策略
        cerebro.addstrategy(strategy=config.strategy)
        # 设置最大使用的杠杆比例

        # for symbol in config.trade_symbols:
        #     cerebro.broker.setcommission(
        #         commission=0.00017 * 1000.0 * config.fundusage / 2,
        #         # 必须为1，原因不说了
        #         margin=1,
        #         # 不同货币的保证金可以使用公式计算得出
        #         automargin=1000,
        #         # 100是杠杆的倍数，1000固定
        #         mult=1000.0 * config.fundusage,
        #         name=symbol)  # 设定此方案分配给那个货币对使用

        self.cerebro = cerebro
        # 加载数据
        self.load_data()

        return cerebro
