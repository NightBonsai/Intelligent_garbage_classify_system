# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : SettingWin.py
# Author : hhs
# DATE : 2023/8/15 20:47

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import filedialog
from tkinter import messagebox
import sys

from tools.ConfigProcess import ConfigProcess


class SettingWin(QWidget):
    """
    设置界面
    """
    def __init__(self):
        super().__init__()  # 调用父类构造函数

        # 初始化
        self.config_process = ConfigProcess("resources/config.ini")
        self.init_win()
        self.init_control()
        self.init_connect()
        self.init_config()      # 初始化配置信息

    def init_win(self):
        """
        窗口初始化
        :return:
        """
        self.setFixedSize(1024, 720)

    def init_control(self):
        """
        控件初始化
        """
        self.title = QLabel("当前系统版本 {}".format("智能垃圾分类系统1.0"), self)
        self.title.setFont(QFont("楷体", 16, QFont.Bold))  # 设置字体样式

        self.server_ip = QLabel("服务器系统IP：", self)
        self.server_ip.setFont(QFont("楷体", 12))
        self.server_ip_edit_a = QLineEdit(self)
        self.server_ip_edit_a.setStyleSheet("background:yellow")
        self.server_ip_edit_b = QLineEdit(self)
        self.server_ip_edit_b.setStyleSheet("background:yellow")
        self.server_ip_edit_c = QLineEdit(self)
        self.server_ip_edit_c.setStyleSheet("background:yellow")
        self.server_ip_edit_d = QLineEdit(self)
        self.server_ip_edit_d.setStyleSheet("background:yellow")
        self.server_port = QLabel("服务器系统端口：", self)
        self.server_port.setFont(QFont("楷体", 12))
        self.server_port_edit = QLineEdit(self)
        self.server_port_edit.setStyleSheet("background:yellow")
        self.db_name = QLabel("数据库连接名称：", self)
        self.db_name.setFont(QFont("楷体", 12))
        self.db_name_edit = QLineEdit(self)
        self.db_name_edit.setStyleSheet("background:yellow")
        self.user_name = QLabel("用户名：", self)
        self.user_name.setFont(QFont("楷体", 12))
        self.user_name_edit = QLineEdit(self)
        self.user_name_edit.setStyleSheet("background:yellow")
        self.passwd = QLabel("密码：", self)
        self.passwd.setFont(QFont("楷体", 12))
        self.passwd_edit = QLineEdit(self)
        self.passwd_edit.setStyleSheet("background:yellow")
        self.import_model = QLabel("导入模型", self)
        self.import_model.setFont(QFont("楷体", 12))
        self.import_model_edit = QLineEdit(self)
        self.import_model_edit.setStyleSheet("background:white")
        self.import_model_edit.setEnabled(False)                   # 不可编辑
        self.import_model_button = QPushButton("...", self)
        self.import_model_button.setStyleSheet("background:yellow")
        self.yes_button = QPushButton("确定", self)
        self.yes_button.setStyleSheet("background:yellow")
        self.no_button = QPushButton("取消", self)
        self.no_button.setStyleSheet("background:yellow")

        self.title.setGeometry(300, 50, 500, 50)
        self.server_ip.setGeometry(300, 130, 200, 50)
        self.server_ip_edit_a.setGeometry(460, 145, 50, 25)
        self.server_ip_edit_b.setGeometry(520, 145, 50, 25)
        self.server_ip_edit_c.setGeometry(580, 145, 50, 25)
        self.server_ip_edit_d.setGeometry(640, 145, 50, 25)
        self.server_port.setGeometry(300, 210, 200, 50)
        self.server_port_edit.setGeometry(460, 225, 200, 25)
        self.db_name.setGeometry(300, 290, 200, 50)
        self.db_name_edit.setGeometry(460, 305, 200, 25)
        self.user_name.setGeometry(300, 370, 200, 50)
        self.user_name_edit.setGeometry(380, 385, 100, 25)
        self.passwd.setGeometry(520, 370, 200, 50)
        self.passwd_edit.setGeometry(580, 385, 100, 25)
        self.import_model.setGeometry(300, 450, 200, 50)
        self.import_model_edit.setGeometry(400, 460, 200, 30)
        self.import_model_button.setGeometry(600, 460, 50, 30)
        self.yes_button.setGeometry(300, 530, 200, 50)
        self.no_button.setGeometry(550, 530, 200, 50)

    def init_connect(self):
        """
        信号与槽初始化
        """
        self.import_model_button.clicked.connect(self.open_folder_dialog_slot)
        self.yes_button.clicked.connect(self.save_config_slot)
        self.no_button.clicked.connect(self.clear_slot)

    def init_config(self):
        """
        初始化配置信息
        :return:
        """
        # 获取配置信息
        config_info = self.config_process.get_config_info()
        host_ip = config_info["host"].split(".")

        # 设置配置信息
        self.server_ip_edit_a.setText(host_ip[0])
        self.server_ip_edit_b.setText(host_ip[1])
        self.server_ip_edit_c.setText(host_ip[2])
        self.server_ip_edit_d.setText(host_ip[3])
        self.server_port_edit.setText(config_info["port"])
        self.db_name_edit.setText(config_info["db"])
        self.user_name_edit.setText(config_info["user"])
        self.passwd_edit.setText(config_info["pwd"])
        self.import_model_edit.setText(config_info["model"])

    # 槽函数
    def open_folder_dialog_slot(self):
        """
        选择指定文件夹目录，导入模型
        :return:
        """
        folder_path = filedialog.askopenfilename()
        folder_path = folder_path.split(".")
        folder_path = folder_path[0] + "." + folder_path[1]
        print("选择的模型路径：", folder_path)

        self.import_model_edit.setText(folder_path)

    def list_judge_slot(self):
        """
        表单判空操作，若有空余，不可切换界面
        :return: True or False 表单非空，表单有空
        """
        if self.server_ip_edit_a.text() == "" or self.server_ip_edit_b.text() == "" or self.server_ip_edit_c.text() == "" or self.server_ip_edit_d.text() == "":
            QMessageBox.information(self, "提示", "host表单不能为空")
            print("host表单不能为空")
            return False
        elif self.server_port_edit.text() == "":
            QMessageBox.information(self, "提示", "port端口表单不能为空")
            print("port端口表单不能为空")
            return False
        elif self.db_name_edit.text() == "":
            QMessageBox.information(self, "提示", "数据库名不能为空")
            print("数据库名不能为空")
            return False
        elif self.user_name_edit.text() == "":
            QMessageBox.information(self, "提示", "数据库用户名不能为空")
            print("数据库用户名不能为空")
            return False
        elif self.passwd_edit.text() == "":
            QMessageBox.information(self, "提示", "数据库密码不能为空")
            print("数据库密码不能为空")
            return False
        elif self.import_model_edit.text() == "":
            QMessageBox.information(self, "提示", "模型路径不能为空")
            print("模型路径不能为空")
            return False
        else:
            return True

    def save_config_slot(self):
        """
        点击确定保存数据
        :return:
        """
        print("保存配置文件----------------------------------------------------------------------------------------------")
        # 判空操作
        flag = self.list_judge_slot()
        if flag is True:
            # 保存数据进config.ini配置文件中
            config_info = {
                "host": self.server_ip_edit_a.text() + "." + self.server_ip_edit_b.text() + "." +
                        self.server_ip_edit_c.text() + "." + self.server_ip_edit_d.text(),
                "user": self.user_name_edit.text(),
                "pwd": self.passwd_edit.text(),
                "db": self.db_name_edit.text(),
                "port": self.server_port_edit.text(),
                "model": self.import_model_edit.text()
            }
            self.config_process.save_config_info(config_info)
            QMessageBox.information(self, "提示", "配置文件保存成功")

    def clear_slot(self):
        """
        清空当前表单
        :return:
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序

    setting_win = SettingWin()
    setting_win.show()

    sys.exit(app.exec())  # exec()程序持续运行
