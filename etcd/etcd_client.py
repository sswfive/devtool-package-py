"""
@Time    : 2022/3/9
@Author  : ssw
@File    : etcd_client.py
@Desc    : python 操作 etcd

# package install:
    pdm add etcd3
    pdm add retry
"""

import time
import etcd3
from retry import retry
import random
from threading import Thread


class Helper:
    __instance = None

    def __init__(self, etcd_cli):
        self.etcd_cli = etcd_cli
        self._poll_dic = dict()  # 轮询  缓存字典
        self._min_connect_dic = dict()  # 最小链接 缓存字典 未实现

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def random(self, service_name):
        _dic = self.etcd_cli.get_prefix("/" + service_name)
        # 没有该服务注册信息
        if not _dic:
            return
        # 只有一个该服务
        if len(_dic) == 1:
            return list(_dic.values())[0]
        # 随机选一个键  返回对应的值
        _key = random.sample(_dic.keys(), 1)[0]
        return _dic[_key]

    def poll(self, service_name):
        _dic = self.etcd_cli.get_prefix("/" + service_name)
        # 没有该服务注册信息
        if not _dic:
            return
        # 只有一个该服务
        if len(_dic) == 1:
            return list(_dic.values())[0]
        # 如果都轮询过了则清空缓存
        if len(self._poll_dic.get(service_name, {})) == len(_dic):
            self._poll_dic[service_name] = dict()
        # 在缓存中写入已经使用过的服务
        for k, v in _dic.items():
            if k not in self._poll_dic.get(service_name, {}):
                self._poll_dic[service_name] = dict()
                self._poll_dic[service_name][k] = v
                return v


class EtcdClient:
    def __init__(self, ip, port):
        self.client = etcd3.client(ip, port)
        self.finder = Helper(self)

    def get(self, key):
        """
        :param key:
        :return:
        """
        res = self.client.get(key)[0]
        if res:
            return str(res)[2:-1]
        return None

    def get_prefix(self, prefix):
        """
        :param prefix:
        :return: dict
        """
        res = self.client.get_prefix(prefix)
        _dic = dict()
        for i in res:
            k, v = i[1].key.decode(), i[0].decode()
            _dic[k] = v
        return _dic

    @retry(tries=3, delay=1)
    def exist_key(self, key):
        """
        判断是否存在指定服务
        :param key: 服务名 eg. /task_service
        :return:
        """
        if self.get(key) is None:
            raise KeyError("不存在该服务")
        return True

    def put(self, key, value, ttl=None, auto_refresh_lease=False):
        """
        注册服务到etcd
        :param key: 服务的键
        :param value: 服务的地址
        :param ttl: 服务与etcd的心跳时间
        :param auto_refresh_lease: 是否自动刷新 默认未False
        :return: 如果设置了ttl则返回lease.id即租约的id  否则返回None
        """
        if ttl is None:
            self.client.put(key, value)

        else:
            lease = self.client.lease(ttl)
            self.client.put(key, value, lease)
            if auto_refresh_lease:
                # 自动定时刷新
                t = Thread(target=self.refresh_lease, args=(lease, ttl))
                t.setDaemon(True)
                t.start()
            return lease.id

    def refresh_lease(self, lease: etcd3.Lease, ttl):
        while True:
            lease.refresh()
            time.sleep(ttl / 2)


etcd_cli = EtcdClient("127.0.0.1", 2379)
if __name__ == '__main__':
    # print(etcd_cli.exist_key("controller/999/999-0"))
    # print(etcd_cli.exist_key("/controller/999"))
    # # print(etcd_cli.exist_key("/controller/999/"))
    # etcd_cli.get_prefix("/controller/999")
    etcd_cli.put("/demo/213", "21321321312", ttl=3, auto_refresh_lease=True)
    while True:
        ...
