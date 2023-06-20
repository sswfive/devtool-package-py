"""
@Time    : 2022/3/1 10:44
@Author  : ssw
@File    : helper_pwd.py
@Desc    : 密码加密和校验工具
"""

"""
pip install passlib
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password):
    """
    明文密码加密函数
    :param plain_password  明文密码:
    :return:
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    """
    密码验证函数
    :param  plain_password  明文密码:
    :param  hashed_password  hash加密后的密码:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)
