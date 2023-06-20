"""
# @Time     : 2022/2/28 10:30 下午
# @Author   : ssw
# @File     : helper_json.py
# @Desc      : 
"""
import datetime
import decimal
import json
from json import JSONEncoder


class JsonEncoders:
    json_encoders = {
        datetime: lambda dt: dt.isoformat(' ')  # 解决日期和时间中 "T"字符的格式问题
    }


class JsonObject:
    def __init__(self):
        self.dic = {}

    def put(self, key, value):
        self.dic[key] = value

    def get(self, key):
        return self.dic[key]

    def get_json(self):
        return json.dumps(self.dic, ensure_ascii=False).replace('}"', '}')

    def get_dict(self):
        return self.dic


class CustomJSONEncoder(JSONEncoder):
    """
    自定义 JSON 编码处理
    """
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat().replace("T", ' ')
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat().replace("T", " ")
            elif isinstance(obj, decimal.Decimal):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def dict_to_json(obj, ensure_ascii=False):
    stu = obj.__dict__  # 将对象转成dict字典
    return json.dumps(obj=stu, cls=CustomJSONEncoder, ensure_ascii=ensure_ascii, indent=4)


def json_to_dict(json_msg):
    dict = json.loads(s=json_msg)
    return dict


def dict_to_json_ensure_ascii(dict={}, ensure_ascii=False):
    """不格式化的输出ensure_ascii==false 输出中文的时候，保持中文的输出"""
    return json.dumps(dict, cls=CustomJSONEncoder, ensure_ascii=ensure_ascii)


def dict_to_json_ensure_ascii_indent(dict={}, ensure_ascii=False):
    """格式化排版缩进输出-ensure_ascii==false 输出中文的时候，保持中文的输出"""
    return json.dumps(dict, cls=CustomJSONEncoder, ensure_ascii=ensure_ascii, indent=4)


def class_to_dict(obj):
    if not obj:
        return None
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict.get('__data__')