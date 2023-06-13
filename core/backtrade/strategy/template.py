import backtrader as bt

from config.config import TradeConfig
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil
from core.utils.date_util import DateFormat


class TemplateStrategy(bt.Strategy):
    logger = print
    strategy_name = ''
    trade_free_cost = 0

    def __init__(self):
        # 回测使用的股票
        self.symbols = {}

        self.log(ColourTxtUtil.red(self.strategy_name), islog=True)
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.symbols[symbol] = klines

        self.order_value = 0

    def next(self):
        """最核心的触发策略"""
        raise

    def notify_trade(self, trade):
        """
        交易通知
        :param trade:
        :return:
        """
        if not trade.isclosed:
            return
        symbol = SymbolUtil.trade_symbol(trade)
        data_str = self.datetime.datetime().strftime(DateFormat.YMDHMS)

        log_info = '%s %s %s  净利润 %.2f' % (
            ColourTxtUtil.green('平仓'),
            ColourTxtUtil.blue(symbol),
            data_str, trade.pnl)
        self.log(log_info)

    def log(self, text, islog=False):
        """
        日志
        :param text: 日志内容
        :param islog: 是否打印
        :return:
        """
        if TradeConfig.is_show_trade_log or islog:
            self.logger(text)

    def notify_order(self, order):
        """通知订单状态,当订单状态变化时触发"""

        symbol = SymbolUtil.order_symbol(order)

        if order.status in [order.Submitted, order.Accepted]:  # 接受订单交易，正常情况
            return
        data_str = self.datetime.datetime().strftime(DateFormat.YMDHMS)
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '%s: %s 执行做多, 价格: %.2f, 花费: %.2f, 手续费 %.2f,数量 %.2f' %
                    (ColourTxtUtil.blue(symbol),
                     data_str,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     order.executed.size,))
                self.trade_free_cost += order.executed.comm
            else:
                self.log('%s: %s 执行做空, 价格: %.2f, 花费: %.2f, 手续费 %.2f 数量%.2f' %
                         (ColourTxtUtil.blue(symbol),
                          data_str,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          order.executed.size))
                self.trade_free_cost += order.executed.comm
        elif order.status in [order.Margin, order.Rejected]:
            self.log('{} {} 订单{} 现金不足、金额不足拒绝交易'.format(
                ColourTxtUtil.blue(symbol),
                data_str,
                ColourTxtUtil.blue(order.ref),
            ))
        elif order.status in [order.Canceled]:
            self.log('{} {} 订单{} 已取消'.format(
                ColourTxtUtil.blue(symbol),
                data_str,
                ColourTxtUtil.blue(order.Status[order.ref]),
            ))

        elif order.status in [order.Expired]:
            self.log('{} {} 订单{} 超过有效期已取消, 订单开价 {}, 当天最高价{}, 最低价{}'.format(
                ColourTxtUtil.blue(symbol),
                data_str,
                ColourTxtUtil.blue(order.Status[order.ref]),
                order.price,
                order.data.high[0],
                order.data.low[0]
            ))

    def show_trade_info(self, islog=False):
        """
        交易信息
        :return:
        """
        # 显示账户信息
        account = ConsoleFormatUtil.account_str(self.broker)
        self.log(account, islog=islog)
        # 显示订单信息：

        # 显示资产信息
        for klines in self.datas:
            position = self.getposition(klines)
            position_str = ConsoleFormatUtil.position_str(position, klines)
            self.log(position_str, islog=islog)

        # 显示行情数据
        for klines in self.datas:
            klines_str = ConsoleFormatUtil.klines_str(klines)
            self.log(klines_str, islog=islog)

    def fetch_cash(self):
        """
        获取可用现金
        :return:
        """
        return self.broker.get_cash() - self.order_value

    def fetch_klines(self, symbol):
        """
        获取指标
        :param symbol:
        :return:
        """
        if symbol not in self.symbols:
            return None

        return self.symbols[symbol]

    def fetch_symbols(self):
        """
        目前回测股票
        :return:
        """
        return list(self.symbols.keys())

    def fetch_positions(self):
        """
        获取当前仓位
        :return:
        """
        positions = {}

        for symbol, klines in self.symbols.items():
            positions[symbol] = self.getposition(klines)
        return positions

    def stop(self):
        """
        结束是的的信息
        :return:
        """
        self.log("{} {}".format(ColourTxtUtil.red('总手续费 '), self.trade_free_cost), islog=True)
        for klines in self.datas:
            position = self.getposition(klines)
            position_str = ConsoleFormatUtil.position_str(position, klines)
            self.log(position_str, islog=True)

    def fetch_order(self, symbol):
        """
        获取订单信息
        :param symbol:
        :return:
        """
        for order in self.broker.orders:
            if symbol == SymbolUtil.order_symbol(order) and order.status in [order.Submitted, order.Accepted]:
                return order
        return None
