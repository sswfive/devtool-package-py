"""
@Time    : 2022/3/13
@Author  : ssw
@File    : mysql.py
@Desc    : 执行.sql文件生成表和数据
"""


import pymysql
from pathlib import Path


class ConnectMsql:

    def __init__(self, host='10.10.10.10', port=3307, user='root', password='123456',
                 database="sonic4", filename: str = "lms_v3-v1.sql"):
        """
        :param host:        域名
        :param port:        端口
        :param user:        用户名
        :param password:    密码
        :param database:    数据库名
        :param filename:    文件名称
        """

        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._database: str = database
        self._file_path = Path(__file__).parent.joinpath(filename)

    def _show_databases_and_create(self):
        """
        查询数据库是否存在，不存在则进行新建操作
        :return:
        """
        connection = pymysql.connect(host=self._host, port=self._port, user=self._user, password=self._password,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('show databases;')
                result = cursor.fetchall()
                results = self._database not in tuple(x["Database"] for x in result)

        if results:
            with connection.cursor() as cursor:
                cursor.execute(f'create database {self._database};')
            with connection.cursor() as cursor:
                cursor.execute('show databases;')
                result = cursor.fetchall()
                results = self._database in tuple(x["Database"] for x in result)
            return results if results else result
        else:
            return True

    def _export_databases_data(self):
        """
        读取.sql文件，解析处理后，执行sql语句
        :return:
        """
        if self._show_databases_and_create() is True:
            connection = pymysql.connect(host=self._host, port=self._port, user=self._user, password=self._password,
                                         database=self._database, charset='utf8')
            # 读取sql文件，并提取出sql语句
            results, results_list = "", []
            with open(self._file_path, mode="r+", encoding="utf-8") as r:
                for sql in r.readlines():
                    # 去除数据中的“\n”和“\r”字符
                    sql = sql.replace("\n", "").replace("\r", "")
                    # 获取不是“--”开头且不是“--”结束的数据
                    if not sql.startswith("--") and not sql.endswith("--"):
                        # 获取不是“--”的数据
                        if not sql.startswith("--"):
                            results = results + sql

                # 根据“;”分割数据，处理后插入列表中
                for i in results.split(";"):
                    if i.startswith("/*"):
                        results_list.append(i.split("*/")[1] + ";")
                    else:
                        results_list.append(i + ";")

            # 执行sql语句
            with connection:
                with connection.cursor() as cursor:
                    # 循环获取sql语句
                    for x in results_list[:-1]:
                        # 执行sql语句
                        cursor.execute(x)
                        # 提交事务
                        connection.commit()
                    else:
                        return "sql全部语句执行成功 ！"

    @property
    def sql_run(self):
        """
        执行方法
        :return:
        """
        return self._export_databases_data()


if __name__ == '__main__':
    res = ConnectMsql().sql_run
    print(res)