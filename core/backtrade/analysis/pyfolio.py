import datetime
import os

import quantstats

from core.utils.colour import ColourTxtUtil
from core.utils.date_util import DateUtil


class PyfolioReportAnalyzer:

    @staticmethod
    def execute(cerebro, config) -> str:
        """
        财务数据
        :return:
        """

        template_path = config.pyfolio_template_path
        output = PyfolioReportAnalyzer.fetch_output_path(config)
        stats = cerebro.run()
        portfolio = stats[0].analyzers.getbyname('pyfolio')
        returns, positions, transactions, gross_lev = portfolio.get_pf_items()
        returns.index = returns.index.tz_convert(None)
        quantstats.reports.html(returns, output=output, template_path=template_path,
                                download_filename=output,
                                title="")
        print("{}： {}".format(ColourTxtUtil.blue("Pyfolio分析结果："), output))
        return output

    @staticmethod
    def fetch_output_path(config):
        # 当前时间字符串
        data_str = DateUtil.datetime_to_format(date=datetime.datetime.now(), fmt='%Y_%m_%d_%H_%M_%S')
        output = config.resource_path + "/analysis"
        if not os.path.exists(output):
            os.makedirs(output)
        return output + '/' + data_str + '.html'
