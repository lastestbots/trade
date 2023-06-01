import tushare as ts

from config.config import TushareConfig

ts.set_token(TushareConfig.api_key)
pro = ts.pro_api()

df = pro.index_daily(ts_code='000300.SH', start_date='20220101', end_date='20220201')
print(df)