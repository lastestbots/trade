from core.backtrade.command.trade import BuyCommand, SellCommand
from core.backtrade.strategy.template import TemplateStrategy
from core.backtrade.utils.format import ConsoleFormatUtil
from core.utils.colour import ColourTxtUtil


class FeatureTradeStrategy(TemplateStrategy):
    """
    期货实盘交易策略
    """

    def __init__(self):
        super().__init__()
        self.log("期货实盘交易模拟器")

    def next(self):
        # 显示交易信息
        self.show_trade_info()
        self.order_value = 0
        while True:
            self.log(ConsoleFormatUtil.command_str())
            command = input("{}：".format(ColourTxtUtil.red("指令"))).replace(' ', '').upper()
            if command == '' or command == 'N':
                break
            elif command == 'B':
                self.order_value += BuyCommand.execute(command, strategy=self)
            elif command == 'S':
                SellCommand.execute(command, strategy=self)
