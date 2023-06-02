from core.backtrade.utils.command import OrderCommandConsoleUtil
from core.model.enums import OrderSide, OrderType


class ConsoleOrderParam:
    """
    从控制台获取订单参数
    """
    # 订单价值
    value = None
    # 订单价格
    price: float = 0
    # 品种
    symbol = None
    # 订单方向
    side: OrderSide
    # 订单类型
    type: OrderType

    def is_limit(self) -> bool:
        return self.type == 'L'

    def is_market(self) -> bool:
        return self.type == 'M'


class ConsoleOrderFactory:
    @staticmethod
    def create_feature_order(clash, symbols) -> ConsoleOrderParam:
        """
        :param clash: 可用资金
        :param symbols: 可用品种
        :return:
        """
        params = ConsoleOrderParam()
        params.side = OrderCommandConsoleUtil.fetch_side()
        params.type = OrderCommandConsoleUtil.fetch_type()
        params.symbol = OrderCommandConsoleUtil.fetch_symbol(symbols)
        if params.type != OrderType.Market:
            params.price = OrderCommandConsoleUtil.fetch_price()
        params.value = OrderCommandConsoleUtil.fetch_order_value(clash)
        return params

    @staticmethod
    def create_sell_position_order(positions, symbols) -> ConsoleOrderParam:
        """
        :param positions: 可用资金
        :param symbols: 可用品种
        :return:
        """
        params = ConsoleOrderParam()
        params.symbol = OrderCommandConsoleUtil.fetch_position_symbol(positions, symbols)
        if params.symbol is None:
            return params
        position_size = positions[params.symbol].size
        params.value = OrderCommandConsoleUtil.fetch_position_value(position_size)
        return params
