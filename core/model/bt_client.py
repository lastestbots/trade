from core.model.enums import OrderSide, OrderType
from core.utils.colour import ColourTxtUtil


class ConsoleOrderParam:
    """
    从控制台获取订单参数
    """
    ratio: float
    price: float
    symbol: str
    side: OrderSide
    type: OrderType

    def __init__(self, log):
        self.log = log

    def is_limit(self) -> bool:
        return self.type == 'L'

    def is_market(self) -> bool:
        return self.type == 'M'

    def fetch_side(self):
        while True:
            self.log("{}:做多 {}：做空".format(ColourTxtUtil.red(OrderSide.Buy.value),
                                              ColourTxtUtil.red(OrderSide.Sell.value)))
            order_side = input("{}：".format(ColourTxtUtil.orange("订单方向："))).replace(' ', '').upper()

            if order_side == OrderSide.Sell.value:
                self.side = OrderSide.Sell
                break
            elif order_side == OrderSide.Buy.value:
                self.side = OrderSide.Buy
                break

    def fetch_type(self):
        while True:
            self.log("{}:市价 {}：限价".format(ColourTxtUtil.red(OrderType.Market.value),
                                              ColourTxtUtil.red(OrderType.Limit.value)))
            order_type = input("{}：".format(ColourTxtUtil.orange("订单类型："))).replace(' ', '').upper()

            if order_type == OrderType.Market.value:
                self.type = OrderType.Market
                break
            elif order_type == OrderType.Limit.value:
                self.type = OrderType.Limit
                break

    def fetch_symbol(self, symbols):
        while True:
            self.log("{}: {}".format(ColourTxtUtil.red("Symbols:"),
                                     symbols))
            symbol = input("{}：".format(ColourTxtUtil.orange("Symbol："))).replace(' ', '').upper()
            if symbol in symbols:
                self.symbol = symbol
                break
            else:
                self.log(ColourTxtUtil.red("{} not in  support symbols ".format(symbol)))

    def fetch_price(self):
        while True:
            price = input("{}：".format(ColourTxtUtil.orange("Price："))).replace(' ', '').lower()
            try:

                price = float(price)
            except ValueError:
                self.log(ColourTxtUtil.red('price must be float'))

            if 0 < price:
                self.price = price
                break
            else:
                self.log(ColourTxtUtil.red("price should be > 0"))

    def fetch_ratio(self):
        while True:
            self.log("{}: (0,100] %".format(ColourTxtUtil.red("开仓比列")))
            size_ratio = input("{}：".format(ColourTxtUtil.orange("Ratio："))).replace(' ',
                                                                                     '').lower()
            try:
                size_ratio = float(size_ratio)
            except ValueError:
                self.log(ColourTxtUtil.red('ratio must be float'))
                continue
            if 0 < size_ratio <= 100:
                self.ratio = size_ratio
                break
            else:
                self.log(ColourTxtUtil.red("ratio should be in (0,100]"))

    def fetch_params_by_console(self, symbols):
        self.fetch_side()
        self.fetch_type()
        self.fetch_symbol(symbols)
        self.fetch_ratio()

        if self.type.is_limit():
            self.fetch_price()


class ConsoleOrderParamsFactory:

    @staticmethod
    def create_test_order_model(log, symbol: str) -> ConsoleOrderParam:
        param = ConsoleOrderParam(log=log)
        param.side = OrderSide.Sell
        param.type = OrderType.Market

        param.ratio = 100
        param.symbol = symbol.upper()
        return param

    @staticmethod
    def fetch_buy_by_console(log, symbols: list) -> ConsoleOrderParam:
        params = ConsoleOrderParam(log=log)
        params.side = OrderSide.Buy
        params.fetch_type()
        if len(symbols) == 1:
            params.symbol = symbols[0]
        else:
            params.fetch_symbol(symbols)
        params.fetch_ratio()

        if params.type.is_limit():
            params.fetch_price()
        return params

    @staticmethod
    def fetch_sell_by_console(log, symbols: list) -> ConsoleOrderParam:
        params = ConsoleOrderParam(log=log)
        params.side = OrderSide.Sell
        params.fetch_type()
        if len(symbols) == 1:
            params.symbol = symbols[0]
        else:
            params.fetch_symbol(symbols)
        params.fetch_ratio()

        if params.type.is_limit():
            params.fetch_price()
        return params
