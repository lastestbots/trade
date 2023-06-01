import empyrical
import numpy as np
import pandas as pd
import pyfolio as pf
from empyrical import max_drawdown, alpha_beta

returns = np.array([.01, .02, .03, -.4, -.06, -.02])
benchmark_returns = np.array([.02, .02, .03, -.35, -.05, -.01])
max_drawdown(returns)  # 计算最大回撤
alpha, beta = alpha_beta(returns, benchmark_returns)  # 计算alpha和beta
returns = pd.Series([.01, .02, .03, -.4, -.06, -.02])  # 支持pd.Series()
DRAWDOWN = max_drawdown(returns)
print(dir(empyrical))

