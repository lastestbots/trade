class SymbolUtil:
    @staticmethod
    def order_symbol(order):
        return order.data._name

    @staticmethod
    def klines_symbol(klines):
        symbol = klines._name
        return symbol

    @staticmethod
    def trade_symbol(trade):
        return trade.data._name
