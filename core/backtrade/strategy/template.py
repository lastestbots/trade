import backtrader as bt
from loguru import logger


class TemplateStrategy(bt.Strategy):

    def __init__(self):
        # 记录用
        self.buy_bond_record = {}  # 记录购买的订单
        self.sell_bond_record = {}  # 记录卖出的订单

    def next(self):
        """最核心的触发策略"""
        raise

    def notify_order(self, order):
        """通知订单状态,当订单状态变化时触发"""
        today_time_string = self.datetime.datetime().strftime('%Y-%m-%d')
        if order.status in [order.Submitted, order.Accepted]:  # 接受订单交易，正常情况
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_bond_record.setdefault(today_time_string, {})
                self.buy_bond_record[today_time_string].setdefault(order.data._name.replace(".", "_"), [])
                self.buy_bond_record[today_time_string][order.data._name.replace(".", "_")].append({
                    "order_ref": order.ref,
                    "bond_name": order.data._name,
                    "size": order.size,
                    "price": order.executed.price,
                    "value": order.executed.value,
                    "trade_date": self.datetime.datetime(0),
                })
                logger.debug('{} 订单{} 已购入 {} , 购入单价 {:.2f}, 数量 {}, 费用 {:.2f}, 手续费 {:.2f}'.
                             format(self.datetime.date(), order.ref, order.data._name, order.executed.price, order.size,
                                    order.executed.value, order.executed.comm))
            elif order.issell():
                self.sell_bond_record.setdefault(today_time_string, {})
                self.sell_bond_record[today_time_string].setdefault(order.data._name.replace(".", "_"), [])
                self.sell_bond_record[today_time_string][order.data._name.replace(".", "_")].append({
                    "order_ref": order.ref,
                    "bond_name": order.data._name,
                    "size": order.size,
                    "price": order.executed.price,
                    "value": - order.executed.price * order.size,
                    "sell_type": order.info.sell_type,
                    "trade_date": self.datetime.datetime(0),
                })
                logger.debug('{} 订单{} 已卖出 {}, 卖出金额 {:.2f}, 数量 {}, 费用 {:.2f}, 手续费 {:.2f}'.
                             format(self.datetime.date(), order.ref, order.data._name, order.executed.price, order.size,
                                    -order.executed.price * order.size, order.executed.comm))
        elif order.status in [order.Margin, order.Rejected]:
            logger.warning('{} 订单{} 现金不足、金额不足拒绝交易', self.datetime.date(), order.ref)
        elif order.status in [order.Canceled]:
            logger.debug("{} 订单{} 已取消", self.datetime.date(), order.ref)
        elif order.status in [order.Expired]:
            logger.warning('{} 订单{} 超过有效期已取消, 订单开价 {}, 当天最高价{}, 最低价{}', self.datetime.date(),
                           order.ref, order.price,
                           order.data.high[0], order.data.low[0])

# self.buy(
#     data=self.getdatabyname(stock_name), # 针对哪一个股票代码
#     size=100, # 数量
#     price=self.getdatabyname(stock_name).close[0], # 以当天的收盘价购买
#     exectype=bt.Order.Limit, # 限价单
#     valid=self.getdatabyname(stock_name).datetime.date(1),  # 有效期1天
# )
