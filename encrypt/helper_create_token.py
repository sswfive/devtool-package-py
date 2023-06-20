"""
@Time    : 2022/3/1 10:38
@Author  : ssw
@File    : helper_create_token.py
@Desc    : jwt  生成token
"""
from datetime import timedelta, datetime
from typing import Optional
from jose import jwt
from fastapi import HTTPException, Header

# jwt加密key
SECRET_KEY = "eac77e4e9a9a767b792779132e84ea37b1f4c31bec56714607f617a3fbdfbd53"
# 加密算法
ALGORITHM = "HS256"

# token过期时间(分钟)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# token过期时间(小时)
ACCESS_TOKEN_EXPIRE_HOURS = 2


def create_token(data:dict, expires_delta: Optional[timedelta] = None):
    """
       生成token函数
       :param data: 需要进行JWT令牌加密的数据（解密的时候会用到）
       :param expires_delta: 令牌有效期
       :return: token
       """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # expire = datetime.utcnow() + timedelta(hours=2)
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    # 添加失效时间
    to_encode.update({"exp": expire})
    # SECRET_KEY：密钥
    # ALGORITHM：JWT令牌签名算法
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_token(authorization: Optional[str] = Header(None)):
    """
    解析token
    :param authorization: token字符串
    :return: username
    """
    token = authorization
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("sub")
        # 通过解析得到的username并返回
        if username:
            return username
        # raise HTTPException(status_code=401, detail='token错误')
        raise TokenException(code=401, msg='token错误', data=None)
    except jwt.ExpiredSignatureError:
        # raise HTTPException(status_code=401, detail='token已过期')
        raise TokenException(code=401, msg='token已过期', data=None)
    except jwt.JWTError:
        # raise HTTPException(status_code=401, detail='token验证失败')
        raise TokenException(code=401, msg='token验证失败', data=None)




class MyBaseException(Exception):
    """ 自定义异常基类 """

    def __init__(self, status_code: int, code: int, msg: str, data: None):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.data = data


class TokenException(MyBaseException):
    """ 自定义token异常类 """
    pass