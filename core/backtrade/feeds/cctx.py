from backtrader.feeds import PandasData


class CCxtDataFeeds(PandasData):
    lines = ('de',)  # 要添加的线
    params = (
        ('de', -1),

    )
