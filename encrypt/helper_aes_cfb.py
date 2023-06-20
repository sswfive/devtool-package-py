"""
# @Time     : 2022/3/1 7:48 上午
# @Author   : ssw
# @File     : helper_aes_cfb.py
# @Desc      : 
"""


from Crypto.Cipher import AES
import base64
import os

BLOCK_SIZE = 16
PADDING = '\0'
pad_it = lambda s: s+(16 - len(s)%16)*PADDING
# key = b'B31F2A75FBF94099'


#使用aes算法，进行加密解密操作
#为跟java实现同样的编码，注意PADDING符号自定义
def encrypt_aes(sourceStr):
    generator = AES.new(key, AES.MODE_CFB, iv)
    crypt = generator.encrypt(pad_it(sourceStr).encode('utf-8'))
    cryptedStr = base64.b64encode(crypt)
    return cryptedStr


def decrypt_aes(cryptedStr):
    generator = AES.new(key, AES.MODE_CFB, iv)
    cryptedStr = base64.b64decode(cryptedStr)
    recovery = generator.decrypt(cryptedStr)
    decryptedStr = recovery.rstrip(PADDING.encode('utf-8'))
    return decryptedStr


# sourceStr = '{"abc":"dfr","agh":"fdfd"}'
if __name__ == '__main__':

    sourceStr = "{'accessId':'1000000002','accessOrderid':'un12jasdmas2123','accountno':'18674866463','productId':'100001','callBackUrl':'http://xxx.com','productAmount':1}"
    key = b'pfJG5kZzUQHIes8k'
    iv = b'16-Bytes--String'

    print('明文:',sourceStr)
    print('加密串:',encrypt_aes(sourceStr))
    print('解密串:',decrypt_aes(encrypt_aes(sourceStr)).decode('utf-8'))