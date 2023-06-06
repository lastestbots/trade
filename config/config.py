import os
import warnings
from configparser import ConfigParser
from datetime import datetime

from core.model.enums import AnalyzerType
from core.utils.date_util import DateUtil
from init import fetch_app_path, fetch_default_config_path, fetch_pyfolio_template_path

warnings.filterwarnings('ignore')
# 读取配置文件
CONFIG_FILENAME = './config.ini'

config = ConfigParser()
if os.path.exists(CONFIG_FILENAME):
    config.read(CONFIG_FILENAME, encoding='utf-8')
elif os.path.exists(fetch_default_config_path()):
    CONFIG_FILENAME = fetch_default_config_path()
    config.read(CONFIG_FILENAME, encoding='utf-8')
else:
    raise FileExistsError(f"配置文件 {CONFIG_FILENAME}  不存在")

APP_PATH = fetch_app_path()
RESOURCE_PATH = APP_PATH + '/static'
CCXT_API_KEY = config.get('ccxt', 'api_key')
if CCXT_API_KEY == 'None':
    CCXT_API_KEY = None
CCXT_SECRET = config.get('ccxt', 'secret')
if CCXT_SECRET == 'None':
    CCXT_SECRET = None

TRADE_BALANCE = float(config.get('trade', 'balance'))
TRADE_FEE = float(config.get('trade', 'fee'))
TRADE_SYMBOLS = config.get('trade', 'symbols').split(',')
TRADE_TIMEFRAME = config.get('trade', 'timeframe')
TRADE_FROM_TIME = config.get('trade', 'from_time')
TRADE_TO_TIME = config.get('trade', 'to_time')
if TRADE_TO_TIME == 'None':
    TRADE_TO_TIME = None
else:
    TRADE_TO_TIME = DateUtil.format_to_end_datetime(TRADE_TO_TIME)

if TRADE_FROM_TIME == 'None':
    TRADE_FROM_TIME = None
else:
    TRADE_FROM_TIME = DateUtil.format_to_begin_datetime(TRADE_FROM_TIME)

TRADE_ENABLE_SHORT = config.get('trade', 'enable_shore').lower() == 'true'

TRADE_ENABLE_COC = config.get('trade', 'enable_coc').lower() == 'true'
TRADE_IS_SHOW_LOG = config.get('trade', 'is_show_trade_log').lower() == 'true'
TRADE_SHIPPING_FIXED = config.get('trade', 'slippage_fixed')
TRADE_SHIPPING_FIXED = float(TRADE_SHIPPING_FIXED)

CONFIG_TRADE_ANALYZERS = config.get('trade', 'analyzers').split(",")
TRADE_ANALYZERS = []
for TRADE_ANALYZER in CONFIG_TRADE_ANALYZERS:
    TRADE_ANALYZERS.append(AnalyzerType.value_of(TRADE_ANALYZER))

PYFOLIO_TEMPLATE_PATH = fetch_pyfolio_template_path()

FUNDUASAGE = int(config.get('trade', 'fundusage'))


class CcxtConfig:
    """
    cctx配置
    """
    # 交易所的密钥
    api_key = CCXT_API_KEY
    # 交易所的密钥
    secret = CCXT_SECRET


class SystemConfig:
    """
    系统配置
    """
    # 资源位置
    resource_path = RESOURCE_PATH


class TradeConfig:
    """
    模拟交易配置
    """
    # 账户余额
    account_balance = TRADE_BALANCE
    # 设置以收盘价成交，作弊模式
    trade_enable_coc = TRADE_ENABLE_COC
    # 手续费
    account_fee = TRADE_FEE
    # 交易股票
    trade_symbols = TRADE_SYMBOLS
    # 时间级别
    trade_timeframe: str = TRADE_TIMEFRAME
    # 交易开始
    trade_from_time: datetime = TRADE_FROM_TIME
    # 交易结束
    trade_to_time: datetime = TRADE_TO_TIME
    # 是否做空
    enable_shore: bool = TRADE_ENABLE_SHORT
    # 滑点
    trade_shipping_fixed: float = TRADE_SHIPPING_FIXED
    # 运行策略
    strategy = None
    # 分析器
    analyzers = TRADE_ANALYZERS
    is_show_trade_log = TRADE_IS_SHOW_LOG
    # 资源位置
    resource_path = RESOURCE_PATH
    pyfolio_template_path = PYFOLIO_TEMPLATE_PATH
    # 使用的杠杆
    fundusage = FUNDUASAGE
