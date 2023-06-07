from core.backtrade.strategy.template import TemplateStrategy


class SmaStrategy(TemplateStrategy):
    # 定义参数

    def __init__(self):
        super().__init__()

    def next(self):
        for klines in self.datas:
            pass
