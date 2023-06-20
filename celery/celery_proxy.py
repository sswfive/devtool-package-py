"""
@Time    : 2022/3/1 14:33
@Author  : ssw
@File    : celery_proxy.py
@Desc    :
"""

from celery import Celery


class CeleryProxy:

    def __init__(self, app: Celery) -> None:
        self.app = app

    def send_tasks(self, *args, **kwargs):
        return self.app.send_task(*args, **kwargs)