"""
# @Time     : 2022/3/1 7:58 上午
# @Author   : ssw
# @File     : helper_time2.py
# @Desc      : 时间字符串转换
"""

import calendar
import time
import datetime

import math


def datetime2str(t=None, format='%Y-%m-%d %H:%M:%S'):
    '''
    将数据转换为字符串形式
    :param t:  datetime 格式时间； int 长度10 秒时间戳格式， int 长度13 毫秒时间戳
    :param format:
    :return:
    '''
    if t is None:
        return datetime.datetime.now().strftime(format)

    if isinstance(t, datetime.datetime):
        return t.strftime(format)
    elif isinstance(t, int):
        if len(str(t)) == 10:
            return datetime.datetime.fromtimestamp(t).strftime(format)
        elif len(str(t)) == 13:
            return datetime.datetime.fromtimestamp(t // 1000).strftime(format)
        else:
            return None


def str2datetime(tstr, format='%Y-%m-%d %H:%M:%S'):
    '''
    字符串为datetime格式
    :param tstr:  时间的字符串
    :param format:
    :return:
    '''
    if tstr is None:
        return datetime.datetime.strptime("1970-01-01 00:00:00", format)
    elif isinstance(tstr, str):
        return datetime.datetime.strptime(tstr, format)


def str2datet(tstr, format='%Y-%m-%d %H:%M:%S'):
    '''
    字符串为datetime格式
    :param tstr:  时间的字符串
    :param format:
    :return:
    '''
    if tstr is None:
        return datetime.datetime.strptime("1970-01-01 00:00:00", format)
    elif isinstance(tstr, str):
        return datetime.datetime.strptime(tstr, format)


'''
-------------------------------------------------------------------------------------------------------
时间字符串---间隔转换
-------------------------------------------------------------------------------------------------------
'''


def humanread_date(timestr):
    if timestr == None:
        return u"Null"
    d = datetime.datetime.strptime(timestr, "%Y-%m-%d")
    now = datetime.datetime.now()
    dist = now - d

    if dist.days == 0:
        return u'今天'
    elif dist.days == 1:
        return u'昨天'
    elif dist.days == 2:
        return u'前天'
    else:
        return u'{0}天前'.format(dist.days)


def humanread_time(t):
    if t is None:
        return u"Null"
    if isinstance(t, datetime.datetime):
        d = t
    elif isinstance(t, int):
        d = datetime.datetime.fromtimestamp(t / 1000)
    else:
        raise Exception(u"unknown time type:%s" % (type(t)))

    now = datetime.datetime.now()
    dist = now - d
    # 当天
    if dist.days == 0:
        if dist.seconds <= 60:
            return u'1分钟内'
        elif dist.seconds <= 60 * 60:
            return u'{0}分钟前'.format(int(math.ceil(dist.seconds / 60)))
        else:
            return u'{0}小时前'.format(int(math.ceil(dist.seconds / 3600)))
    elif dist.days < 0:
        return u'刚才'
    else:
        return d.strftime(u"%Y-%m-%d %H:%M")


def humanread_timelong(sec):
    ds = int(sec)
    print('time long diff', sec)
    if ds < 60:
        return u'%d秒前'.format(ds)
    elif ds < 3600:
        return u'{0}分{1}秒前'.format(int(math.floor(ds / 60)), int(ds % 60))
    else:
        return u'{0}小时{1}分{2}秒前'.format(int(math.floor(ds / 3600)), int(math.floor(ds % 3600 / 60)), int(ds % 60))


def get_date(*args):
    '''
    获取日期
    根据参数个数调判断实现多态
    :param args:
    :return:
    '''
    # 1个参数或者没有参数默认get_date_for_datetime
    if len(args) == 1 or len(args) == 0:
        return get_date_for_datetime(*args)
    # 3个参数时默认为年月日
    elif len(args) == 3:
        return get_date_for_args(*args)


def get_date_for_datetime(dt=None):
    '''
    根据datetime获取date
    :param dt:
    :return:
    '''
    if dt == None:
        dt = datetime.datetime.now()
    return datetime.datetime.date(dt)


def get_date_for_args(year, month, day):
    '''
    根据年月日获取date
    :param year: 年
    :param month: 月
    :param day: 日
    :return:
    '''
    return get_date_for_datetime(datetime.datetime(year, month, day))


def get_date_short_str(dt=None):
    '''
    获取日期格式短文本
    :param dt:
    :return:
    '''
    if dt == None:
        dt = datetime.datetime.now()
    return dt.strftime('%Y%m%d')


def get_date_long_str(dt=None):
    '''
    获取日期格式长文本
    :param dt:
    :return:
    '''
    if dt == None:
        dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d")


def get_datetime():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def get_datetime_heng():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_datetime_ymd():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().strftime('%Y%m%d')


def get_datetime_now():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now()


def get_datetime_now_year():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().year


def get_datetime_now_month():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().month


def get_datetime_now_day():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().day


# 获取当前时间下有多少天
def get_curr_monthrange():
    import calendar
    return calendar.monthrange(get_datetime_now_year(), get_datetime_now_month())[1]


# 获取当前时间下有多少天
def get_monthrange(year, month):
    import calendar
    return calendar.monthrange(year, month)[1]


def get_timedelta(minutes=20):
    """ 分钟"""
    return datetime.timedelta(minutes=minutes)


# 2.把字符串转成datetime
def string_toDatetime2222222222(st):
    return datetime.datetime.strptime(st, "%Y-%m-%d")
    # print("2.把字符串转成datetime: ",)


# 2.把字符串转成datetime
def string_toDatetime(st):
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
    # print("2.把字符串转成datetime: ",)


# 2.把字符串转成datetime
def string_toDatetime_times(st, format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(st, format)
    # print("2.把字符串转成datetime: ",)


def string_toDatetime_times2(st):
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")


# 2.把字符串转成datetime
def string_toDatetime_times_two(st):
    return datetime_toString(string_toDatetime_times2(st))


def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d 00:00:00")


def get_datetime_2():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")


def get_datetime_3():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_datetime_4():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().strftime("%Y%m%d%H%M")


# 2.把字符串转成datetime
# def string_toDatetime(st):
#     return datetime.strptime(st, "%Y-%m-%d %H:%M:%S")

# 2.把字符串转成datetime
def string_toDatetime_2(st):
    return datetime.datetime.strptime(st, "%Y%m%d%H%M%S")
    # print("2.把字符串转成datetime: ",)


def add_datetime(strtime, timedelta):
    # 有效期开始时间
    validity_starttime = string_toDatetime(st=strtime) + timedelta(timedelta)
    # 有效期结束时间

    return validity_starttime + timedelta(days=365 + (365 / 2))


def get_datetime_strftime():
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime.now().strftime('%Y%m%d')


def get_datetime_ymr(shijian):
    """获取年月日时分秒毫秒共10位数的字符串"""
    return datetime.datetime(shijian.year, shijian.month, shijian.day)


def timestamp_to_datatime(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def timestampto_back_time(timestamp):
    return time.localtime(timestamp)


def timestamp_to_datatime_statrt(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d 00:00:00", timeArray)


def timestamp_to_datatime_end(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d 23:59:59", timeArray)


def timestamp_to_datatime2(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d 00:00:00", timeArray)


def to_date(dt):
    """将时间格式化为日期字符串（%Y-%m-%d）"""
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d')
    elif isinstance(dt, datetime.date):
        return dt.strftime('%Y-%m-%d')


def to_datetime(dt):
    """将时间格式化为日期字符串（2017-01-12 10:00:00）"""
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ''


def get_timestamp10():
    """获取当前时间长度为10位长度的时间戳"""
    return int(time.time())


def get_timestamp10_add(num):
    """当前时间长度为10位长度的时间戳+ 多少秒"""
    return int(time.time() + num)


def get_timestamp13():
    """获取当前时间长度为13位长度的时间戳"""
    return int(time.time() * 1000)


def diff(sign, start_time, end_time):
    """
    比较两个时间相差几秒、几分、几小时、几日、几周、几月、几季或几年
    sign: y = 年, q = 季, m =月, w = 周, d = 日, h = 时, n = 分钟, s = 秒
    start_time: 开始时间
    end_time： 结束时间
    return: 返回两个时间差值（整形数值）
    """
    result = end_time - start_time
    if sign == 'y':
        return result.days // 365
    elif sign == 'q':
        return result.days // 30 // 3
    elif sign == 'm':
        return result.days // 30
    elif sign == 'w':
        return result.days // 7
    elif sign == 'd':
        return result.days
    elif sign == 'h':
        return result.seconds // 60 // 60
    elif sign == 'n':
        return result.seconds // 60
    elif sign == 's':
        return result.seconds


def timedelta(sign, dt, value):
    """
    对指定时间进行加减运算，几秒、几分、几小时、几日、几周、几月、几年
    sign: y = 年, m = 月, w = 周, d = 日, h = 时, n = 分钟, s = 秒
    dt: 日期，只能是datetime或datetime.date类型
    value: 加减的数值
    return: 返回运算后的datetime类型值
    """
    if sign == 'y':
        year = dt.year + value
        if isinstance(dt, datetime.date):
            return datetime.datetime(year, dt.month, dt.day)
        elif isinstance(dt, datetime.datetime):
            return datetime.datetime(year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        else:
            return None
    elif sign == 'm':
        year = dt.year
        month = dt.month + value
        ### 如果月份加减后超出范围，则需要计算一下，对年份进行处理 ###
        # 如果月份加减后等于0时，需要特殊处理一下
        if month == 0:
            year = year - 1
            month = 12
        else:
            # 对年月进行处理
            year = year + month // 12
            month = month % 12
        if isinstance(dt, datetime.date):
            # 如果日大于月的最大日数，则改成该月最后一天
            if int(dt.day) > int(calendar.monthrange(year, month)[1]):
                return datetime.datetime(year, month, int(calendar.monthrange(year, month)[1]))
            else:
                return datetime.datetime(year, month, dt.day)
        elif isinstance(dt, datetime.datetime):
            # 如果日大于月的最大日数，则改成该月最后一天
            if int(dt.day) > int(calendar.monthrange(year, month)[1]):
                return datetime.datetime(year, month, int(calendar.monthrange(year, month)[1]), dt.hour, dt.minute,
                                         dt.second, dt.microsecond)
            else:
                return datetime.datetime(year, month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        else:
            return None
    elif sign == 'w':
        delta = datetime.timedelta(weeks=value)
    elif sign == 'd':
        delta = datetime.timedelta(days=value)
    elif sign == 'h':
        delta = datetime.timedelta(hours=value)
    elif sign == 'n':
        delta = datetime.timedelta(minutes=value)
    elif sign == 's':
        delta = datetime.timedelta(seconds=value)
    else:
        return None

    return dt + delta


def get_date_first_formonth(year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    # 获取月份的第一天日期
    return datetime.datetime(year, month, 1)


def get_date_last_formonth(year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    # 获取月份的最后一天日期
    return datetime.datetime(year, month + 1, 1) - datetime.timedelta(1)


def get_current_date():
    """获取今日日期
    格式: '20171213'
    """
    return time.strftime("%Y%m%d")


def get_current_timestamp():
    """获取当前时间戳
    格式: 1524032735404
    """
    return int(round(time.time() * 1000))


def get_current_time():
    """获取当前时间
    :return: 时间类型
    """
    return datetime.datetime.now()


def weekofmonth(date):
    """当前天是当月中的第几周
    :param date:
    :return:第几周
    """
    end = int(date.strftime('%W'))
    start = int(datetime.datetime(date.year, date.month, 1).strftime('%W'))
    return end - start


def formatTime(timestamp, format="%Y-%m-%d %H:%M:%S"):
    """格式化时间戳
    格式: 2017-12-13 16:32:30
    """
    time_local = time.localtime(timestamp / 1000)
    return time.strftime(format, time_local)


def get_time():
    """获取当前时间
    => 格式: '2017-12-13 16:32:30'
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_time_before(days=0, hours=0, minutes=0, seconds=0, microseconds=0):
    """获取时间偏移数据
    :param days:
    :param hours:
    :param minutes:
    :param seconds:
    :param microseconds:
    :return: 获取当前时间戳=> 格式: '2017-12-13 16:32:30'
    """
    res = datetime.datetime.now() - datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds,
                                                       microseconds=microseconds)
    return res


# 获取当前系统得时间得月份开始 和 月尾得时间
def get_curr_sys_day_begin_day_end():
    import calendar
    import time
    day_now = time.localtime()
    day_begin = '%d-%02d-01 00:00:00' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d 23:59:59' % (day_now.tm_year, day_now.tm_mon, monthRange)
    # print('月初日期为：',day_begin, '月末日期为：',day_end)
    return day_begin, day_end


def get_curr_in_day_begin_day_end(stime):
    day_begin = string_toDatetime(st=stime)
    month_num = int(stime.split('-')[1])
    # print(month_num)
    import calendar
    day_end = day_begin + datetime.timedelta(days=calendar.mdays[month_num])
    return day_begin, day_end


if __name__ == '__main__':
    pass
    # print('2020-05-21 15:29:50')
    # print(datetime.datetime.strptime('2020-05-21 15:29:50', "%Y-%m-%d %H"))
    print(get_datetime_ymd())
    print(float(str(4 / 6)))
