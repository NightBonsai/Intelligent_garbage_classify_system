# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : MySql.py
# Author : hhs
# DATE : 2023/8/15 20:14

import MySQLdb


class MySql:
    """
    数据库单例
    """
    # 数据库是否连接标志位
    _is_connect = False

    def __new__(cls, *args, **kwargs):
        """
        外部接口：获取唯一数据库单例
        :param args:
        :param kwargs:
        :return: 数据库单例，返回后执行__init__构造函数
        """
        if not hasattr(cls, "_instance"):
            # _instance 数据库实例
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_name, pwd, user_name="root", host="192.168.229.200", port="3306"):
        """
        数据库单例构造函数
        :param db_name: 数据库名
        :param pwd: 数据库密码
        :param user_name: 数据库用户名
        :param host: 远程数据库主机ip
        :param port: 远程数据库主体端口号
        """
        if MySql._is_connect is False:
            try:
                # 异常处理
                # __db   私有 数据库实例
                self.__db = MySQLdb.connect(host, user_name, pwd, db_name)   # 远程连接数据库
                print("connect database success")

                MySql._is_connect = True                                     # 连接标志位True

                # __cursor 私有 游标 ≈ 数据库指针
                self.__cursor = self.__db.cursor()                           # 获取游标
            except:
                print("connect database error")

    def execute(self, sql_code):
        """
        执行sql语句
        :param sql_code: sql语句
        :return:执行成功or失败，True or False
        """
        print("执行sql语句---------------------------------------------------------------------------------------------")
        print("sql语句：{}".format(sql_code))
        try:
            # 异常处理
            self.__cursor.execute(sql_code)     # 执行sql语句
            self.__db.commit()                  # 提交到数据库执行
            print("execute sql_code success")
            return True
        except:
            print("execute sql_code error")
            self.__db.rollback()                # 发生错误时回滚
            return False

    def select_op(self, sql_code):
        """
        数据库查询操作
        :param sql_code: 执行sql语句
        :return: 查询的数据，若未查询到返回False
        """
        print("执行sql查询语句------------------------------------------------------------------------------------------")
        print("sql语句：{}".format(sql_code))
        try:
            # 异常处理
            self.__cursor.execute(sql_code)     # 执行sql语句
            self.__db.commit()                  # 提交到数据库执行
            print("execute select_sql_code success")

            data = self.__cursor.fetchall()     # 使用fetchall方法获取一条数据
            return data
        except:
            print("execute select_sql_code error")
            self.__db.rollback()                # 发生错误时回滚
            return False

    def insert_op(self, sql_code):
        """
        数据插入操作
        :param sql_code: sql语句
        :return: 改变的记录列表数，若失败返回False
        """
        print("执行sql插入语句------------------------------------------------------------------------------------------")
        print("sql语句：{}".format(sql_code))
        try:
            # 异常处理
            self.__cursor.execute(sql_code)     # 执行sql语句
            self.__db.commit()                  # 提交到数据库执行
            print("execute insert_sql_code success")

            return self.__cursor.rowcount      # 获取改变的记录列表数
        except:
            print("execute insert_sql_code error")
            self.__db.rollback()                # 发生错误时回滚
            return False

    def __del__(self):
        self.__db.close()                       # 关闭数据库


if __name__ == "__main__":
    # 数据库单例
    db = MySql("IGCS_DB", "123456")

    # 数据插入操作
    # user_id = db.insert_op("insert into tbl_user(user_name,user_pwd,user_icon) values('cq','123456','null');")
    # print("user_id = {}".format(user_id))

    # 数据检索操作
    data = db.select_op("select * from tbl_userInfo where userPwd='123456';")
    print("data = {}".format(data))
