import base64
import hashlib
import hmac
import json
import time
from urllib.parse import quote_plus

import requests

from config.config import DingdingConfig


class DingTalkAdapter:
    def __init__(self):
        self.timestamp = str(round(time.time() * 1000))
        # 钉钉机器人Webhook地址
        self.webhook_url = 'https://oapi.dingtalk.com/robot/send'

        self.headers = {'Content-Type': 'application/json'}
        secret = DingdingConfig.secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': DingdingConfig.token, "sign": self.sign}

    def send_text(self, content):
        """
        发送文本
        @param content: str, 文本内容
        """
        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.webhook_url,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

    def send_markdown_msg(self,title, text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        r = requests.post(self.webhook_url, headers=headers, data=json.dumps(data))
        return r.json()



