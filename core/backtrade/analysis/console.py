import backtrader as bt

from core.backtrade.base.kline import fetch_klines_name
from core.model.bt_analysis import ConsoleAnalyzedResult


class ConsoleAnalyzer:
    @staticmethod
    def execute(cerebro: bt.Cerebro, config) -> ConsoleAnalyzedResult:
        start_cash = cerebro.broker.getvalue()
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        symbols = []
        for klines in cerebro.datas:
            symbols.append(fetch_klines_name(klines))
        for strat in cerebro.run():
            final_asset = cerebro.broker.getvalue()
            pyfoliozer = strat.analyzers.getbyname('pyfolio')
            trades_analysis = strat.analyzers.trades.get_analysis()
            max_gain = trades_analysis.streak.won.longest
            max_loss = trades_analysis.streak.lost.longest
            cum_trades = trades_analysis.total.total
            total_wins = trades_analysis.won.total
            if cum_trades > 0:

                gain_ratio = total_wins / cum_trades
            else:
                gain_ratio = 0
            returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
            result = ConsoleAnalyzedResult(returns, symbols, start_cash, final_asset)
            result.max_gain = max_gain
            result.max_loss = max_loss
            result.gain_ratio = gain_ratio
            result.cum_trades = cum_trades
            result.show_result_empyrical()
            return result
