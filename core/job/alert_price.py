import time

from ccxt import NetworkError
from requests.exceptions import SSLError

from core.model.enums import PriceDirection
from core.utils.ccxt_util import OhlvUtil
from core.utils.colour import ColourTxtUtil
from core.utils.message_util import DingTalkUtil


class AlertPriceTask:

    def __init__(self):
        self.name = ''
        self.symbols = []
        self.direction = PriceDirection.Up
        self.target_prices = []
        self.log = print

    def run(self):
        while True:
            try:

                for i in range(len(self.symbols)):
                    time.sleep(1)
                    symbol = self.symbols[i]
                    price = OhlvUtil.fetch_last_price(symbol)
                    target_price = self.target_prices[i]
                    self.log('{} {}'.format(ColourTxtUtil.blue(symbol), round(price, 3)))

                    if self.direction == PriceDirection.Up and price > target_price:
                        self.send_message(symbol, price, target_price)
                    elif self.direction == PriceDirection.Down or price > target_price:
                        self.send_message(symbol, price, target_price)

                time.sleep(5)
            except SSLError as e:
                self.log('{} {}'.format('认证异常', e))
            except NetworkError as e:
                self.log('{} {}'.format('网络异常', e))
            except Exception as e:
                self.log('{} {}'.format('未知异常', e))

    def send_message(self, symbol, price, target_price):
        title = symbol
        txt = '{} \n{}   {} to target price  {}'.format(symbol, price, self.direction.value, target_price)

        self.log('{} {}'.format(ColourTxtUtil.red(title), txt)
                 )
        DingTalkUtil.send_text(txt)


class AlertPriceTaskFactory:

    @staticmethod
    def load_task_by_config():
        pass
