import json
import os
from datetime import datetime

import numpy as np
from loguru import logger


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return super(NpEncoder, self).default(obj)


class JsonUtil:
    @staticmethod
    def read(filepath, ):
        """
        读取json 数据
        """
        try:

            return json.load(open(filepath, 'r', encoding="utf-8"))
        except Exception as e:
            logger.info("读取json 数据失败由于{}".format(e))
            return None

    @staticmethod
    def write(filepath: str, data, init_data=None):
        """
        文件写入json
        """
        data = json.dumps(data, cls=NpEncoder, indent=4, )

        if init_data is None:
            init_data = []
        if os.path.exists(filepath) is False:
            with open(filepath, 'w') as f:
                f.write(json.dumps(init_data, indent=4, ensure_ascii=False))

        with open(filepath, 'w') as f:
            f.write(data)
