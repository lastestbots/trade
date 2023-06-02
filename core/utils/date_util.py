import time
from datetime import datetime


class DateFormat:
    YMDHMS = '%Y-%m-%d %H:%M:%S'
    YMD = '%Y-%m-%d'


class DateUtil:

    @staticmethod
    def timestamp_to_format(timestamp, fmt=DateFormat.YMDHMS) -> str:
        time_array = time.localtime(timestamp)
        return time.strftime(fmt, time_array)

    @staticmethod
    def format_to_timestamp(date: str, fmt=DateFormat.YMDHMS) -> int:
        """
        时间戳转字符串
        """
        time_array = time.strptime(date, fmt)
        timestamp = int(time.mktime(time_array))
        return timestamp

    @staticmethod
    def format_to_datetime(date_str: str, fmt=DateFormat.YMD) -> datetime:
        """
        时间戳转字符串
        """
        return datetime.strptime(date_str, fmt)

    @staticmethod
    def format_to_end_datetime(date_str: str, fmt=DateFormat.YMD) -> datetime:
        """
        时间戳转字符串
        """
        dt = datetime.strptime(date_str, fmt)
        end_time = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        return end_time

    @staticmethod
    def get_today_end_format():
        today = datetime.today().date()
        end_of_day = datetime.combine(today, datetime.max.time())
        end_of_day_iso = end_of_day.strftime(DateFormat.YMDHMS)
        return end_of_day_iso

    @staticmethod
    def datetime_to_format(date: datetime, fmt=DateFormat.YMDHMS):
        end_of_day_iso = date.strftime(fmt)
        return end_of_day_iso

    @staticmethod
    def format_to_begin_datetime(date_str: str, fmt=DateFormat.YMD) -> datetime:
        """
        时间戳转字符串
        """
        dt = datetime.strptime(date_str, fmt)
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def datetime_to_timestamp(date: datetime) -> int:
        """
        时间戳转字符串
        """

        return int(datetime.timestamp(date))
