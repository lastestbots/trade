import backtrader as bt
import pyfolio as pf

from core.model.bt_analysis import ConsoleAnalyzedResult


class ConsoleAnalyzer:
    @staticmethod
    def execute(cerebro: bt.Cerebro):
        result = ConsoleAnalyzedResult()
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        result.start_cash = cerebro.broker.getvalue()
        result.final_asset = cerebro.broker.getvalue()

        for klines in cerebro.datas:
            result.symbols.add(klines._name)

        strat = cerebro.run()
        pyfoliozer = strat.analyzers.getbyname('pyfolio')
        returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
        pf.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions,
            gross_lev=gross_lev,
            live_start_date='2005-05-01',  # This date is sample specific
            round_trips=True)
