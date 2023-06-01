import empyrical

from core.utils.colour import ColourTxtUtil


class ConsoleAnalyzedResult:
    # 初始资金
    start_cash = 0
    # 回测结束资产
    final_asset = 0
    # 股票
    symbols = []
    # 回测结果
    returns = None
    # 累计收益
    cum_returns_final = 0
    # 年华收益率
    annual_return = []
    # 最大回撤
    max_drawdown = 0
    # 夏普比 : Sharpe Ratio 越高，说明获得每一份超额收益的单位风险越少，投资组合的表现越好
    sharpe_ratio = 0
    # 卡玛比 : Calmar比率越高，表明投资组合收益稳定，承受风险能力越强
    calmar_ratio = 0
    # omega: Omega比率越高，意味着风险越低
    omega_ratio = 1
    # 最大连输次数
    max_loss = 0
    # 最大连赢次数
    max_gain = 0
    # 总交易次数
    cum_trades = 0
    #  胜率
    gain_ratio = 0

    def __init__(self, returns, symbols=None, start_cash=0, final_asset=0):
        if symbols is None:
            symbols = []
        self.symbols = symbols
        self.start_cash = start_cash
        self.final_asset = final_asset
        self.cum_returns_final = empyrical.cum_returns_final(returns)
        self.annual_return = empyrical.annual_return(returns)
        self.max_drawdown = empyrical.max_drawdown(returns)
        self.sharpe_ratio = empyrical.sharpe_ratio(returns)
        self.calmar_ratio = empyrical.calmar_ratio(returns)
        self.omega_ratio = empyrical.omega_ratio(returns)
        self.returns = returns

    def show_result_empyrical(self):
        print(f'{ColourTxtUtil.red("分析报告")}')
        print(f'{ColourTxtUtil.orange("股票")}：', self.symbols)
        print(f'{ColourTxtUtil.orange("初始资金")}：', self.start_cash)
        print(f'{ColourTxtUtil.orange("结束资产")}：', self.final_asset)
        print(f'{ColourTxtUtil.orange("累计收益")}：', self.cum_returns_final)
        print(f'{ColourTxtUtil.orange("年化收益")}：', self.annual_return)
        print(f'{ColourTxtUtil.orange("最大回撤")}：', self.max_drawdown)
        print(f'{ColourTxtUtil.orange("夏普比")}：', self.sharpe_ratio)
        print(f'{ColourTxtUtil.orange("卡玛比")}：', self.calmar_ratio)
        print(f'{ColourTxtUtil.orange("omega")}：', self.omega_ratio)
        print(f'{ColourTxtUtil.orange("交易次数")}：', self.cum_trades)
        print(f'{ColourTxtUtil.orange("交易胜率")}：', self.gain_ratio)
        print(f'{ColourTxtUtil.orange("最大连赢次数")}：', self.max_gain)
        print(f'{ColourTxtUtil.orange("最大连输次数")}：', self.max_loss)
