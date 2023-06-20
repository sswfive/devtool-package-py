"""
# @Time     : 2022/2/20 8:54 下午
# @Author   : ssw
# @File     : hepler_time.py
# @Desc      : 时间转换工具
"""
import calendar
import time
import datetime


class TimeManager:
    """
    时间转换工具
    """
    @staticmethod
    def now(is_str=False, digit=13, fmt='%Y-%m-%d %H:%M:%S'):
        """获取当前时间"""
        now_time = datetime.datetime.now()
        time_str = now_time.strftime(fmt)
        timestamp = (
            int(round(time.mktime(now_time.timetuple()) * 1000))
            if digit == 13
            else int(round(time.mktime(now_time.timetuple())))
        )
        return time_str if is_str else timestamp

    # @staticmethod
    # def get_current_timestamp():
    #     """获取当前时间戳"""
    #     return int(round(time.time() * 1000))
    #
    # @staticmethod
    # def get_current_time_string():
    #     """获取当前时间（字符串）"""
    #     return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_current_date_string():
        """获取当前日期（字符串）"""
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def timestamp_to_str(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
        """时间戳（13位）转换字符串"""
        if isinstance(timestamp, int) or isinstance(timestamp, float):
            if len(str(int(timestamp))) >= 12:
                timestamp = float(timestamp / 1000)
            fmt_time = time.strftime(fmt, time.localtime(timestamp))
            return fmt_time
        else:
            return TimeManager.now(is_str=True)

    @staticmethod
    def str_to_timestamp(time_str, digit=13):
        """字符串转时间戳"""
        timestamp = (
            int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))) * 1000
            if digit == 13
            else int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S")))
        )
        return timestamp

    @staticmethod
    def timestamp_to_datetime(timestamp):
        """时间戳转datetime"""
        return datetime.datetime.fromtimestamp(timestamp / 1000)

    @staticmethod
    def convert_str(time_str, fmt_raw="%Y-%m-%d %H:%M:%S", fmt_goal="%Y-%m-%d %H_%M_%S"):
        """转换时间格式"""
        return datetime.datetime.strptime(time_str, fmt_raw).strftime(fmt_goal)

    @staticmethod
    def utcstr_to_str(utcstr, fmt="%Y-%m-%dT%H:%M:%S.%f+0800"):
        """处理utc类型的时间字符串"""
        utc_time = datetime.datetime.strptime(utcstr, fmt)
        return utc_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def split_time(time_str):
        year = month = day = hour = minute = second = 0
        if "-" in time_str:
            year, month, day = time_str.split(" ")[0].split("-")
            hour, minute, second = time_str.split(" ")[1].split(":")
        else:
            if time_str.count(":") == 2:
                hour, minute, second = time_str.split(":")
            else:
                hour, minute = time_str.split(":")
        return int(year), int(month), int(day), int(hour), int(minute), int(second)

    @staticmethod
    def month_first_day(next_month=False):
        """当前月的第一天（日期）"""
        now_date = datetime.date.today()
        first_day = datetime.date(now_date.year, now_date.month, 1)
        if next_month:
            days_num = calendar.monthrange(first_day.year, first_day.month)[1]
            return first_day + datetime.timedelta(days=days_num)
        else:
            return first_day

    @staticmethod
    def month_last_day(next_month=False):
        """当前月的最后一天（日期）"""
        month_first_day = TimeManager.month_first_day(next_month)
        month_days = calendar.monthrange(month_first_day.year, month_first_day.month)[1]
        month_last_day = month_first_day + datetime.timedelta(days=month_days - 1)
        return month_last_day

    @staticmethod
    def datetime_plus_datetime(time_obj, day):
        datetime_obj = (time_obj + datetime.timedelta(days=day))
        return datetime_obj


if __name__ == '__main__':
    print(TimeManager.now())
    print(TimeManager.now(is_str=True))
    print(TimeManager.get_current_date_string())
    print(TimeManager.split_time("2022-03-01 07:10:37"))
    print(TimeManager.month_first_day())
    print(TimeManager.datetime_plus_datetime(datetime.datetime.now(), 2))


