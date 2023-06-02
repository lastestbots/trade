import backtrader as bt

from core.model.bt_console import ConsoleOrderFactory
# Command 抽象类
from core.utils.colour import ColourTxtUtil


class BuyCommand:
    command = 'B'

    @staticmethod
    def execute(command, strategy):
        if BuyCommand.command != command:
            return

        cash = strategy.fetch_cash()
        symbols = strategy.fetch_symbols()
        order = ConsoleOrderFactory.create_feature_order(cash, symbols)
        klines = strategy.fetch_klines(order.symbol)
        if cash < order.value:
            strategy.log(ColourTxtUtil.red('余额不足'))
        if order.price <= 0:
            size = order.value / klines.high[0]

        else:
            size = order.value / order.price

        strategy.log("{}: {}".format(ColourTxtUtil.orange("下单数量"), size))
        if order.type.is_market():

            if order.side.is_buy():
                strategy.buy(data=klines, size=size)
            elif order.side.is_sell():
                strategy.sell(data=klines, size=size)
        elif order.type.is_limit():
            if order.side.is_buy():
                strategy.buy(data=klines, size=size, price=order.price, exectype=bt.Order.Limit)
            elif order.side.is_sell():
                strategy.sell(data=klines, size=size, price=order.price, exectype=bt.Order.Limit)

        return order.value


class SellCommand:
    command = 'S'

    @staticmethod
    def execute(command, strategy):
        if SellCommand.command != command:
            return

        symbols = strategy.fetch_symbols()
        positions = strategy.fetch_positions()
        order = ConsoleOrderFactory.create_sell_position_order(positions, symbols)
        if order.value is None or order.symbol is None:
            return
        klines = strategy.fetch_klines(order.symbol)
        strategy.close(data=klines, size=order.value)
