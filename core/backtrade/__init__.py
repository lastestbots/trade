from core.backtrade.analysis.console import ConsoleAnalyzer
from core.backtrade.analysis.pyfolio import PyfolioReportAnalyzer

BT_GLOBAL_CONFIG = {
    'analyzer': {
        'ConsoleAnalyzer': ConsoleAnalyzer,
        'PyfolioReportAnalyzer': PyfolioReportAnalyzer
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
