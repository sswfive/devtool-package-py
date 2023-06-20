"""
# @Time     : 2022/3/1 8:00 上午
# @Author   : ssw
# @File     : helper_encrypt.py
# @Desc      : 加密工具
"""
import hashlib
import hmac
import binascii
import base64
from Crypto.Cipher import AES  # PyCrypto 库安装  安装 PyCrypto3.6问题比较多 ，直接安装pycryptodome
from binascii import b2a_hex, a2b_hex


def md5(text):
    """md5加密函数"""
    md5 = hashlib.md5()
    if not isinstance(text, bytes):
        text = str(text).encode('utf-8')
    md5.update(text)
    return md5.hexdigest()


def base64_encode(text):
    """进行base64编码处理"""
    return base64.b64encode(bytes(text, encoding="utf-8"))


def base64_decode(text):
    """进行base64解码处理"""
    return base64.b64decode(text)


def hmac_sha1(key, text):
    """进行hmac加密"""
    h = hmac.new(bytes(key, encoding="utf-8"))
    h.update(bytes(text, encoding="utf-8"))
    return h.hexdigest()


def hmac_sha1_forpphp2(key, text):
    """进行hmac加密"""
    # h = base64.b64encode(hmac.new(bytes(key, encoding="utf-8"), msg=bytes(text, encoding="utf-8"), digestmod=hashlib.sha1).digest())
    # h = base64.b64encode(hmac.new(bytes(key, encoding="utf-8"), msg=bytes(text, encoding="utf-8"), digestmod=hashlib.sha1).digest())

    return md5(
        hmac.new(bytes(key, encoding="utf-8"), msg=bytes(text, encoding="utf-8"), digestmod=hashlib.sha1).digest())


def hmac_sha1_3(key, text):
    """进行hmac加密"""
    dk = hashlib.pbkdf2_hmac(hash_name='sha1',
                             password=bytes(key, encoding='utf-8'),
                             salt=bytes(text, encoding='utf-8'),
                             iterations=100000)
    return binascii.hexlify(dk)


def hmac_sha1_4(key, text):
    """进行hmac加密"""
    h = hmac.new(bytes(key, encoding='utf-8'), bytes(text, encoding='utf-8'), digestmod=hashlib.sha1)
    return h.hexdigest()


def hmac_sha1_5(key, text):
    return binascii.hexlify(
        hmac.new(bytes(key, encoding='utf-8'), bytes(text, encoding='utf-8'), digestmod=hashlib.sha1).digest())


def aes_encode(key, text):
    """进行AES加密"""
    pad_it = lambda s: s + (16 - len(s) % 16) * '\0'
    generator = AES.new(key, AES.MODE_CBC, b'0000000000000000')
    crypt = generator.encrypt(pad_it(text))
    cryptedStr = base64.b64encode(crypt)
    return bytes.decode(cryptedStr)


def aes_decode(key, text):
    """AES解密，解密后，去掉补足的空格用strip() 去掉"""
    generator = AES.new(key, AES.MODE_CBC, b'0000000000000000')
    cryptedStr = base64.b64decode(text)
    recovery = bytes.decode(generator.decrypt(cryptedStr))
    decryptedStr = recovery.rstrip('\0')
    return decryptedStr


if __name__ == '__main__':
    print(aes_decode('wssronin', aes_encode('wssronin', 'aaa')))
