"""
# @Time     : 2022/3/1 7:26 上午
# @Author   : ssw
# @File     : helper_nip.py
# @Desc      : 获取本地IP
"""
import os
import socket
from starlette.requests import Request

def get_local_ip():
    """
    copy and paste from
    https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    """
    if os.environ.get('CHAT_HOST_IP', False):
        return os.environ['CHAT_HOST_IP']
    try:
        ip = [l for l in (
            [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if
             not ip.startswith("127.")][:1], [
                [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s
                 in
                 [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][
            0][
            0]
    except OSError as e:
        print(e)
        return '127.0.0.1'

    return ip


def get_client_ip(request: Request):
    """
    获取客户端真实ip
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host


if __name__ == '__main__':
    print(get_local_ip())