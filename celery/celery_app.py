"""
@Time    : 2022/3/1 14:33
@Author  : ssw
@File    : celery_app.py
@Desc    :
"""


"""
pip install celery==5.2.3
"""

from celery import Celery

from .config import CeleryConfig


# app = Celery('tasks')

# app.config_from_object(CeleryConfig)