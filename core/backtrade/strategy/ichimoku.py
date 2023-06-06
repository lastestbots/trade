# K线图中的一目均衡指标是一种基于移动平均线的技术指标，由日本的书籍作者森永卓郎提出，也叫做Ichimoku Cloud（云图）。它的计算公式如下：
#
# 1. 转换线（Tenkan-Sen）= （9日高点的总和 / 9）和（9日低点的总和 / 9）的平均值
# 2. 基准线（Kijun-Sen）= （26日高点的总和 / 26）和（26日低点的总和 / 26）的平均值
# 3. 前推26天的基准线
# 4. 主极限线（Chikou Span）= 当前收盘价与前推26天的收盘价连接形成的线
# 5. 前期高点（上周期内的最高价）与前期低点（上周期内的最低价）。前期高点为当天前22日中的最高价，前期低点为当天前22天中的最低价。
# 6. 密集云（Kumo）：由两个移动平均线形成，将前期高点与前期低点关于纵坐标对称，然后连接两线。其中，红色的是先行偏差线（Senkou Span A），蓝色的是滞后线（Senkou Span B）。
#

import tushare

print(tushare.__version__)
import tushare as ts

ts.get_hist_data('600848') #一次性获取全部日k线数据
class IchimokuIndicator:
    # 转换线周期
    tenkan_period = 9
    # 基准周期
    kijun_period = 26
    # 转换线
    tenkan_sen = None
    # 基准线
    kijun_sen = None
    # 主极限线
    chikou_span = None
    # 密集云
    kumo = None

    def calculate(self, klines):
        tenkan_period = self.tenkan_period
        if len(klines.high.get(size=tenkan_period)) < tenkan_period:
            return
        # 最高价

        tenkan_ = sorted(klines.high.get(size=tenkan_period), reverse=True)

        # 最低价
        tenkan_l = klines.low.get(size=tenkan_period)

        # # 前一日收盘价
        # pc = klines.close.get(size=2)[0]
        #
        # pivot = (pc + pl + ph) / 3
        #
        # # 第一组 突破买入价 全场最高
        # self.b_break = ph + 2 * (pivot - pl)
        # # 第二组 观察卖出价 多单叛变条件1
        # self.s_setup = pivot + (ph - pl)
        # # 第二组 反转卖出价 多单叛变条件2
        # self.s_enter = 2 * pivot - pl
        # # 第三组 反转买入价 空单叛变条件2
        # self.b_enter = 2 * pivot - ph
        # # 第三组 观察买入价 空单叛变条件1
        # self.b_setup = pivot - (ph - pl)
        # # 第一组 突破卖出价 全场最低
        # self.s_break = pl - 2 * (ph - pivot)
