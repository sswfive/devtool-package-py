"""
# @Time     : 2022/3/1 7:55 上午
# @Author   : ssw
# @File     : helper_check.py
# @Desc      : 参数检查工具
"""

import re


class VerifiedExpression:
    EMAIL_ADDRESS_REG = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*")'
        r'@(?:[A-Z0-9](?:[A-Z0-9-]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))$',
        re.IGNORECASE
    )

    URL_ADDRESS_REG = re.compile(
        r"^(https?|ftp):\/\/"  # http:// or https:// or ftp://
        r"(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?"  # domain
        r"(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|"  # ip
        r"((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|"
        r"(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])"
        r"([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*"
        r"([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+"
        r"(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|"
        r"(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])"
        r"([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*"
        r"([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)"
        r"(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+"
        r"(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?"
        r"(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|"
        r"[!\$&'\(\)\*\+,;=]|:|@)|"
        r"[\uE000-\uF8FF]|\/|\?)*)?"
        r"(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|"
        r"(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$"
    )

    PHONE_REG = re.compile(
        r"^1[3,4,5,7,8]{1}[0-9]{9}$"
    )


class Check:
    @staticmethod
    def is_email(email):
        """
        邮箱验证
        :param email:
        :return:
        """
        return VerifiedExpression.EMAIL_ADDRESS_REG.search(email) is not None

    @staticmethod
    def is_url(url):
        """
        url 验证
        :param url:
        :return:
        """
        return VerifiedExpression.URL_ADDRESS_REG.search(url) is not None

    @staticmethod
    def is_include(param, vals):
        return param in vals

    @staticmethod
    def is_exclude(param, vals):
        return not param in vals

    @staticmethod
    def is_phone(phone):
        """
        手机验证
        :param phone:
        :return:
        """
        return VerifiedExpression.PHONE_REG.search(phone) is not None

    @staticmethod
    def is_valid_datetime(datetime, val, formats):
        import datetime
        try:
            datetime.datetime.strptime(val, formats)
            return True
        except ValueError:
            return False