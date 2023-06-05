import backtrader as bt

from core.backtrade.utils.calculator import CalculatorUtil
from core.backtrade.utils.symbol import SymbolUtil
from core.utils.colour import ColourTxtUtil


class ConsoleFormatUtil:
    """
    控制台格式化工具
    格式化 账户 订单 仓位 行情
    """

    @staticmethod
    def order_str(order):
        symbol = SymbolUtil.order_symbol(order)
        order_ref = order.ref,
        size = order.size,
        price = order.executed.price,
        value = order.executed.price * order.size,
        sell_type = order.info.sell_type,
        return "{} {} {}: {} {}: {} {}: {} {}: {} {}: {} ".format(
            ColourTxtUtil.cyan("订单"),
            symbol,
            ColourTxtUtil.blue("Ref"),
            order_ref,
            ColourTxtUtil.blue("Price"),
            price,
            ColourTxtUtil.blue("Size"),
            size,
            ColourTxtUtil.blue("Value"),
            value,
            ColourTxtUtil.blue("Type"),
            sell_type,
        )

    @staticmethod
    def klines_srt(klines, index=0):
        symbol = SymbolUtil.klines_symbol(klines)
        date_str = bt.num2date(klines.lines[6][0])
        return "{} {} {}: {} {}: {} {}: {} {}: {} {}: {} {}:{} {}：{} %".format(
            ColourTxtUtil.cyan("行情"),
            symbol,

            ColourTxtUtil.blue("Time"),
            date_str,
            ColourTxtUtil.blue("Open"),
            klines.open[index],
            ColourTxtUtil.blue("High"),
            klines.high[0],
            ColourTxtUtil.blue("Low"),
            klines.low[0],
            ColourTxtUtil.blue(
                "Close"),
            klines.close[0],
            ColourTxtUtil.blue(
                "Volume"),
            klines.volume[0],
            ColourTxtUtil.blue(
                "Change"),
            round((klines.close[0] - klines.open[0]) / klines.open[0] * 100, 2)
        )

    @staticmethod
    def position_str(position, klines):
        symbol = SymbolUtil.klines_symbol(klines)
        price = klines.close[0]
        profit = CalculatorUtil.position_profit(position, price)

        return "{} {} {}: {} {}:{} {}：{} {}：{} %".format(ColourTxtUtil.green("资产"),
                                                         ColourTxtUtil.cyan(symbol),
                                                         ColourTxtUtil.blue("Size"),
                                                         position.size,
                                                         ColourTxtUtil.blue("Price"),
                                                         position.price,
                                                         ColourTxtUtil.blue("Assert"),
                                                         position.size * position.price,
                                                         ColourTxtUtil.blue("Profit"),
                                                         round(profit), 2)



    @staticmethod
    def command_str():
        return "{} {}:Buy  {}:Sell {}: Next".format(
            ColourTxtUtil.cyan('Command'),
            ColourTxtUtil.red("B"),
            ColourTxtUtil.red("S"),
            ColourTxtUtil.red("N"),

        )

    @staticmethod
    def account_str(account):
        return "{} {}: {} {}:{}".format(ColourTxtUtil.green("账户"),
                                        ColourTxtUtil.cyan("Assert"),
                                        account.getvalue(),
                                        ColourTxtUtil.cyan("Clash"),
                                        account.get_cash(),
                                        )
