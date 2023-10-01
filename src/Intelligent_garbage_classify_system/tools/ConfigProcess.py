# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : ConfigProcess.py
# Author : hhs
# DATE : 2023/8/16 16:07

import configparser
import os


class ConfigProcess(object):
    """
    配置文件操作类
    """
    def __init__(self, file_path):
        self.config_path = ""

        if os.path.isfile(file_path):
            # 若路径存在
            self.config_path = file_path
            print("找到配置文件")
        else:
            # 若路径不存在
            print("配置文件路径不存在")

    def get_config_info(self):
        """
        获取配置文件信息并返回
        :return: 配置文件信息字典
        """
        print("获取连接数据库&模型信息----------------------------------------------------------------------------------------")
        # 解析配置文件
        self.cf = configparser.ConfigParser()
        self.cf.read(self.config_path)

        secs = self.cf.sections()
        print("配置文件数据")
        print("secs: {}, {}".format(secs, type(secs)))

        host = self.cf.get(secs[0], "host")
        user = self.cf.get(secs[0], "user")
        pwd = self.cf.get(secs[0], "pwd")
        db = self.cf.get(secs[0], "db")
        port = self.cf.get(secs[0], "port")
        charset = self.cf.get(secs[0], "charset")
        model = self.cf.get(secs[1], "model")
        print("host: ", host, " user:", user, " pwd:", pwd, " db:", db,
              " port:", port, " charset:", charset, " model:", model)

        return {"host": host, "user": user, "pwd": pwd, "db": db,
                "port": port, "charset": charset, "model": model}

    def save_config_info(self, config_info):
        """
        保存配置文件信息
        :param config_info: 配置文件信息字典
        :return:
        """
        print("保存数据库&模型信息----------------------------------------------------------------------------------------")
        self.cf.set("database", "host", config_info["host"])
        self.cf.set("database", "user", config_info["user"])
        self.cf.set("database", "pwd", config_info["pwd"])
        self.cf.set("database", "db", config_info["db"])
        self.cf.set("database", "port", config_info["port"])
        self.cf.set("model", "model", config_info["model"])
        self.cf.write(open(self.config_path, "w"))


if __name__ == "__main__":
    read_config = ConfigProcess("../resources/config.ini")
    db_info = read_config.get_config_info()
