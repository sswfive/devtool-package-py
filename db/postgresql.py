"""
# @Time     : 2022/3/1 8:08 上午
# @Author   : ssw
# @File     : helper_pg_db.py
# @Desc      : 
"""
import os
import psycopg2
import time
from io import StringIO
from .file_helper import save_file
from loguru import logger



# 当前程序所在服务器路径
PROGRAM_PATH = os.path.split(os.path.realpath(__file__))[0].rstrip('\\config')
# 日志存储路径
log_path = ''.join((os.path.join(PROGRAM_PATH, 'logutils'), '/sql_timeout.logutils'))

# 是否输出Sql语句到日志里
is_output_sql = False


class PgHelper(object):
    """操作postgresql数据库的类"""

    def __init__(self, db):
        self.connect = None
        self.cursor = None
        # 初始化数据库参数
        self.db_name = db.get('db_name', '')
        self.db_user = db.get('db_user', '')
        self.db_pass = db.get('db_pass', '')
        self.db_host = db.get('db_host', '')
        self.db_port = db.get('db_port', '')

    def __enter__(self):
        """初始化数据库链接"""
        self.open_conn()
        return self

    def __exit__(self, type, value, trace):
        """关闭postgresql数据库链接"""
        self.close_conn()

    def open_conn(self):
        """连接数据库，并建立游标"""
        try:
            if not self.connect:
                self.connect = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_pass,
                                                host=self.db_host, port=self.db_port)
            return self.connect
        except Exception as e:
            logger.error('连接数据库失败：' + str(e.args))
            # print('连接数据库失败：' + str(e.args))
            return False

    def close_conn(self):
        """关闭postgresql数据库链接"""
        # 关闭游标
        try:
            if self.cursor:
                self.cursor.close()
        except Exception:
            pass
        # 关闭数据库链接
        try:
            if self.connect:
                self.connect.close()
        except Exception:
            pass

    def rollback(self):
        """回滚操作"""
        try:
            # 操作异常时，操作回滚
            if self.connect:
                self.connect.rollback()
                self.close_conn()
        except Exception as e:
            logger.error('回滚操作失败：' + str(e.args))

    def commit(self):
        """提交事务"""
        try:
            if self.connect:
                self.connect.commit()
                self.close_conn()
        except Exception as e:
            logger.error('提交事务失败：' + str(e.args))

    def get_sql(self, query, vars=None):
        """获取编译后的sql语句"""
        start_time = time.clock()
        try:
            # 建立游标该程序创建一个光标将用于整个数据库使用Python编程
            self.cursor = self.connect.cursor()
            # 执行SQL
            self.data = self.cursor.mogrify(query, vars)
            if is_output_sql:
                self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' sql:' + str(query))
        except Exception as e:
            self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' error sql:' + str(query))
            logger.error('sql生成失败:' + str(e.args) + ' query:' + str(query))
            self.data = '获取编译sql失败'
        finally:
            # 关闭游标
            self.cursor.close()

        end_time = time.clock()
        self.write_log(start_time, end_time, query)

        return self.data

    def copy(self, values, table_name, columns):
        """
        百万级数据更新函数
        :param values: 更新内容，字段之间用\t分隔，记录之间用\n分隔 "1\taaa\tabc\n2\bbb\abc\n"
        :param table_name: 要更新的表名称
        :param columns: 需要更新的字段名称：例：('id','userame','passwd')
        :return:
        """
        try:
            # 建立游标
            self.cursor = self.connect.cursor()
            self.cursor.copy_from(StringIO(values), table_name, columns=columns)
            self.connect.commit()
            return True
        except Exception as e:
            self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' 批量更新%s失败' % (table_name,))
            logger.error('批量更新失败:' + str(e.args) + ' table:' + table_name)
        finally:
            # 关闭游标
            self.cursor.close()

    def execute(self, query, vars=None):
        """执行sql语句查询，返回结果集或影响行数"""
        if not query:
            return None

        # if not self.connect:
        #     return None

        start_time = time.clock()
        try:
            # 建立游标
            self.cursor = self.connect.cursor()
            # 执行SQL
            self.cursor.execute(query, vars)
            if is_output_sql:
                self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' sql:' + str(query))
        except Exception as e:
            self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' error sql:' + str(query))
            args = str(e.args)
            if not 'unique' in args:
                logger.error('sql执行失败:' + args + ' query:' + str(query))
            self.data = None
        else:
            # 获取数据
            try:
                self.data = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row))
                             for row in self.cursor.fetchall()]
            except Exception as e:
                self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' error sql:' + str(query))
                # log_helper.info('数据获取失败:' + str(e.args) + ' query:' + str(query))
                self.data = None
        finally:
            # 关闭游标
            self.cursor.close()

        end_time = time.clock()
        self.write_log(start_time, end_time, query)

        # 如果写入数据后，有返回数据，则把该数据返回给调用者
        if self.data and self.data != -1:
            return self.data

        # 返回操作成功的记录条数
        rowcount = self.cursor.rowcount
        if rowcount > 0:
            return rowcount
        elif self.data != None:
            return self.data
        else:
            return None

    def execute_transaction(self, query, vars=None):
        """执行sql语句查询，返回结果集或影响行数"""
        start_time = time.clock()
        try:
            # 建立游标
            self.cursor = self.connect.cursor()
            # 执行SQL
            self.cursor.execute(query, vars)
            if is_output_sql:
                self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' sql:' + str(query))
        except Exception as e:
            # 操作异常时，操作回滚
            if self.connect:
                self.connect.rollback()
                # 关闭游标
                self.cursor.close()
            self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' error sql:' + str(query))
            logger.error('sql事务执行失败:' + str(e.args) + ' query:' + str(query))
            return False
        else:
            # 获取数据
            try:
                self.data = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row))
                             for row in self.cursor.fetchall()]
            except Exception as e:
                self.__save_log(time.strftime('%Y-%m-%d %H:%M:%S') + ' sql:' + str(query))
                # log_helper.info('数据获取失败:' + str(e.args) + ' query:' + str(query))
                self.data = None
        finally:
            # 关闭游标
            self.cursor.close()

        end_time = time.clock()
        self.write_log(start_time, end_time, query)

        # 如果写入数据后，有返回数据，则把该数据返回给调用者
        if self.data and self.data != -1:
            return self.data

        # 返回操作成功的记录条数
        rowcount = self.cursor.rowcount
        if rowcount > 0:
            return rowcount
        elif self.data != None:
            return self.data
        else:
            return None

    def write_log(self, start_time, end_time, sql):
        """记录Sql执行超时日志"""
        t = end_time - start_time
        if (t) > 0.1:
            content = ' '.join((time.strftime('%Y-%m-%d %H:%M:%S'), ' main time:', str(t), 's sql:', sql))
            self.__save_log(content)

    def __save_log(self, text):
        """存储日志"""
        save_file(log_path, text + '\n')