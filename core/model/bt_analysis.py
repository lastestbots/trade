class ConsoleAnalyzedResult:
    # 初始资金
    start_cash = 0
    # 回测结束资产
    final_asset = 0
    # 股票
    symbols = []

    # 收益率
    roi = None
    # 夏普率
    sharpe_ratio = None
    # 最大回撤：最大回撤是衡量策略表现的另一个重要指标，衡量的是策略最大损失能力。最大回撤越小，则策略表现越好。
    max_draw_down = None
    # 胜率
    win_percentage = None
    # 盈亏比
    profit_ratio = None
    # 赢次数
    win_num = None
    # 输次数
    lost_num = None
    # 最大赢次数
    win_longest = None
    # 最大输次数
    lost_longest = None
    # 年化率
    annualized_rates = None
