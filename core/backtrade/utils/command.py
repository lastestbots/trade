from core.model.enums import OrderSide, OrderType
from core.utils.colour import ColourTxtUtil

log_func = print


class OrderCommandConsoleUtil:
    """
    负责从控制台获取命令
    """

    @staticmethod
    def fetch_side():
        while True:
            log_func("{}:做多 {}：做空".format(ColourTxtUtil.red(OrderSide.Buy.command),
                                              ColourTxtUtil.red(OrderSide.Sell.command)))
            input_command = input("{}：".format(ColourTxtUtil.orange("订单方向："))).replace(' ', '').upper()

            if input_command == OrderSide.Sell.value:
                return OrderSide.Sell

            elif input_command == OrderSide.Buy.value or input_command == '':
                return OrderSide.Buy

    @staticmethod
    def fetch_type() -> OrderType:
        while True:
            log_func("{}:市价 {}：限价".format(ColourTxtUtil.red(OrderType.Market.command),
                                              ColourTxtUtil.red(OrderType.Limit.command)))
            input_command = input("{}：".format(ColourTxtUtil.orange("订单类型："))).replace(' ', '').upper()

            if input_command == OrderType.Market.value or input_command == '':
                return OrderType.Market

            elif input_command == OrderType.Limit.value:
                return OrderType.Limit

    @staticmethod
    def fetch_symbol(symbols):
        while True:
            log_func("{}: {}".format(ColourTxtUtil.red("Symbols:"),
                                     symbols))
            symbol = input("{}：".format(ColourTxtUtil.orange("购买股票："))).replace(' ', '').upper()

            if symbol == '' and len(symbols) > 0:

                return symbols[0]
            elif symbol in symbols:

                return symbol
            else:
                log_func(ColourTxtUtil.red("{} not in  support symbols ".format(symbol)))

    @staticmethod
    def fetch_position_symbol(positions, symbols):
        while True:
            log_func("{}: {}".format(ColourTxtUtil.red("Symbols:"),
                                     symbols))
            symbol = input("{}：".format(ColourTxtUtil.orange("购买股票："))).replace(' ', '').upper()
            if symbol.lower() == 'back':
                return
            if symbol == '' and len(symbols) > 0:
                symbol = symbols[0]
                if positions[symbol].size == 0:
                    log_func(ColourTxtUtil.red("仓位为空 ".format(symbol)))
                    continue
                return symbol
            elif symbol in symbols:
                if positions[symbol].size == 0:
                    log_func(ColourTxtUtil.red("仓位为空 ".format(symbol)))
                    continue
                return symbol
            else:
                log_func(ColourTxtUtil.red("{} not in  support symbols ".format(symbol)))

    @staticmethod
    def fetch_price():
        while True:
            input_command = input("{}：".format(ColourTxtUtil.orange("订单价格："))).replace(' ', '').lower()
            try:
                if input_command == '':
                    return 99
                input_command = float(input_command)

            except ValueError:
                log_func(ColourTxtUtil.red('input_command must be float'))
                continue
            if 0 < input_command:
                return input_command

            else:
                log_func(ColourTxtUtil.red("input_command should be > 0"))

    @staticmethod
    def fetch_order_value(clash):
        while True:
            log_func("{}: {}".format(ColourTxtUtil.red("可用资金："), clash))
            o_value = input("{}：".format(ColourTxtUtil.orange("购买金额："))).replace(' ',
                                                                                     '').lower()
            try:
                if o_value == '':
                    continue
                elif o_value.endswith('%'):
                    o_value = float(o_value.replace('%', ''))
                    if o_value <= 0 or o_value > 100:
                        log_func(ColourTxtUtil.red('clash not enough'))
                    else:
                        return clash * o_value * 0.01
                else:
                    o_value = float(o_value)
                    if o_value >= clash or o_value < 0:
                        log_func(ColourTxtUtil.red('clash not enough'))
                        continue
                    else:
                        return o_value

            except ValueError:
                log_func(ColourTxtUtil.red('clash must be float'))
                continue

    @staticmethod
    def fetch_position_value(position_size):
        while True:
            log_func("{}: {}".format(ColourTxtUtil.red("持有仓位："), position_size))
            position_value = input("{}：".format(ColourTxtUtil.orange("平仓数量："))).replace(' ',
                                                                                            '').lower()
            try:
                if position_value == 'back':
                    return

                if position_value == '':
                    continue
                elif position_value.endswith('%'):
                    position_value = float(position_value.replace('%', ''))
                    if position_value <= 0 or position_value > 100:
                        log_func(ColourTxtUtil.red('format error'))
                    else:
                        return position_size * position_value * 0.01
                else:
                    position_value = float(position_value)
                    if position_value >= position_size or position_value < 0:
                        log_func(ColourTxtUtil.red('position not enough'))
                        continue
                    else:
                        return position_value

            except ValueError:
                log_func(ColourTxtUtil.red('position must be float'))
                continue
