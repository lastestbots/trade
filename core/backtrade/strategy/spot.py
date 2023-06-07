from typing import Dict, List

import backtrader as bt

from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.format import ConsoleFormatUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.model.bt_console import ConsoleOrderFactory
from core.utils.colour import ColourTxtUtil


class SpotStrategy(TemplateStrategy):
    logger = print

    def __init__(self):
        self.threshold = 0  # 设置阈值为 -1000.0，小于此值即控制账户负余额风险

        self.orders: Dict[str, List] = {}

        self.symbols = {}
        for klines in self.datas:
            symbol = SymbolUtil.klines_symbol(klines)
            self.orders[symbol] = []
            self.symbols[symbol] = klines

    def fetch_order_symbol(self, order):
        for symbol, orders in self.orders.items():
            for o in orders[:]:
                if o == order:
                    return symbol
        return None

    def remove_order(self, order):
        for symbol, orders in self.orders.items():
            for o in orders[:]:
                if o == order:
                    orders.remove(o)

    def account_info(self):
        broker = self.broker

        return "{} {}: {} {}:{}".format(ColourTxtUtil.green("账户"),
                                        ColourTxtUtil.cyan("Assert"),
                                        broker.getvalue(),
                                        ColourTxtUtil.cyan("Clash"),
                                        broker.get_cash(),
                                        )

    def fetch_symbol_position(self, symbol):
        return self.getposition(self.symbols[symbol])

    def total_position_assert(self):
        value = 0
        for klines in self.datas:
            value += self.fetch_position_assert(klines)
        return value

    def fetch_position_assert(self, klines):
        position = self.getposition(klines)
        return position.size * position.price

    def show_position_info(self, klines):
        position = self.getposition(klines)
        position_str = ConsoleFormatUtil.position_str(position, klines)
        self.log(position_str)

    def show_order_info(self, klines):
        symbol = SymbolUtil.klines_symbol(klines)
        if symbol in self.orders:
            orders = self.orders[symbol]
            for order in orders:
                order_str = ConsoleFormatUtil.order_str(order)
                self.log(order_str)

    def show_klines_info(self, klines):
        klines_str = ConsoleFormatUtil.klines_str(klines)
        self.log(klines_str)

    def show_account_info(self):
        self.log(self.account_info())

    def notify_trade(self, trade):

        if not trade.isclosed:
            return

        self.log('{}: 净利润{} 净利润率{} %'.format(
            ColourTxtUtil.green("平仓"), round(trade.pnlcomm, 2), round(trade.pnlcomm, 2) / self.cash * 100))

    @property
    def cash(self):
        return self.broker.getvalue() - abs(self.total_position_assert())

    def next(self):
        # 交易信息
        self.log("\n{}".format(ColourTxtUtil.purple('实盘交易模拟器')))
        self.show_account_info()
        self.log("\n")
        for klines in self.datas:
            self.show_position_info(klines)
        self.log("\n")
        for klines in self.datas:
            self.show_order_info(klines)
        self.log("\n")
        for klines in self.datas:
            self.show_klines_info(klines)
        # 从控制台获取指令
        self.log("\n")
        self.input_command()
        pass

    def input_command(self):
        while True:
            self.log(ConsoleFormatUtil.command_str())
            command = input("{}：".format(ColourTxtUtil.red("指令"))).replace(' ', '').upper()
            if command == '' or command == 'N':
                break
            elif command == 'A':
                self.show_account_info()
            elif command == 'B':
                self.execute_buy_command()
            elif command == 'S':
                self.execute_sell_command()

    def execute_sell_command(self):
        order = ConsoleOrderFactory.create_feature_order(self.cash, self.symbols.keys())
        if order.side is None or order.type is None or order.symbol is None:
            return
            # 检查是否有仓位
        position = self.fetch_symbol_position(order.symbol)
        if position.size == 0:
            self.log('{}: {}未持仓'.format(ColourTxtUtil.red('Error'), order.symbol))
            return
        size = position.size * order.ratio * 0.01
        klines = self.symbols[order.symbol]
        self.close(data=klines, size=size)

    def execute_buy_command(self):

        order = ConsoleOrderFactory.create_feature_order(self.log, list(self.symbols.keys()))
        if order.side is None or order.type is None or order.symbol is None:
            return
        klines = self.symbols[order.symbol]
        size = self.broker.get_cash() * 0.01 * order.ratio / klines.high[0]
        self.log("{}: {}".format(ColourTxtUtil.orange("金额"), size * klines.high[0]))
        print(order.ratio)
        self.handle_order(order, size)

    def handle_order(self, order, size):
        klines = self.symbols[order.symbol]
        o = None
        self.log("{}: {}".format(ColourTxtUtil.orange("下单数量"), size))
        if order.type.is_market():

            if order.side.is_buy():
                o = self.buy(data=klines, size=size)
            elif order.side.is_sell():
                o = self.sell(data=klines, size=size)
        elif order.type.is_limit():
            if order.side.is_buy():
                o = self.buy(data=klines, size=size, price=order.price, exectype=bt.Order.Limit)
            elif order.side.is_sell():
                o = self.sell(data=klines, size=size, price=order.price, exectype=bt.Order.Limit)
        if o is not None:
            self.orders[order.symbol].append(o)
