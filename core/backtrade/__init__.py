from core.bt.analysis.console import ConsoleAnalyzer

BT_GLOBAL_CONFIG = {
    'analyzer': {
        'ConsoleAnalyzer': ConsoleAnalyzer
    }
}


def fetch_strategy_analyzer(name):
    try:
        analyzer = BT_GLOBAL_CONFIG['analyzer'][name]
        return analyzer
    except KeyError:
        raise KeyError("BT_GLOBAL_CONFIG 找不到分析器{}".format(name))


class BackTradeConfig:
    @staticmethod
    def fetch_strategy_analyzer(name):
        try:
            analyzer = BT_GLOBAL_CONFIG['analyzer'][name]
            return analyzer
        except KeyError:
            raise KeyError("BT_GLOBAL_CONFIG 找不到分析器{}".format(name))
