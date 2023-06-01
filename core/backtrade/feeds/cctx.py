from datetime import datetime

import backtrader as bt
from backtrader.feeds import PandasData


class CCxtPdData(PandasData):
    lines = ('de',)  # 要添加的线
    params = (
        ('de', -1),

    )

