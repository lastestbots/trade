import backtrader as bt

from core.utils.colour import ColourTxtUtil


def format_order_info(symbol, order):
    return "{} {} {} ".format(ColourTxtUtil.green("订单"),
                              ColourTxtUtil.cyan(symbol),
                              order
                              )


def fetch_klines_name(klines):
    symbol = klines._name
    return symbol


def compute_profit(position, price):
    if position.price > 0 and position.price > 0:
        return (price - position.price) / position.price * 100
    elif position.price > 0 and position.price > 0:
        return 0 - (abs(position.price) - price) / abs(position.price) * 100
    return 0


def format_klines_str(klines, index=0):
    symbol = fetch_klines_name(klines)
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
        (klines.close[0] - klines.open[0]) / klines.open[0] * 100
    )
