# -*- coding: utf-8 -*-
# Project : homework
# Name : MainWin.py
# Author : hhs
# DATE : 2023/7/20 15:34
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from tkinter import messagebox

from view.LoginWin import LoginWin
from view.RegistWin import RegistWin
from view.TrashChangeWin import TrashChangeWin
from view.UserInforManageWin import UserInforManageWin
from view.UserInforAddWin import UserInforAddWin
from view.RecycleMonitorWin import RecycleMonitorWin
from view.RecycleRecordWin import RecycleRecordWin
from view.ErrorClassifyDisplayWin import ErrorClassifyDisplayWin
from view.SettingWin import SettingWin
from mySql.MySql import MySql
from tools.ConfigProcess import ConfigProcess


class MainWin(QWidget):
    def __init__(self, win_icon_path, user_icon_path):
        """
        主窗口类  继承QWidget
        :param win_icon_path:   界面图标存储路径
        :param user_icon_path:  用户头像存储路径
        """
        # 调用父类构造函数
        super().__init__()

        # 接收传参
        self.win_icon_path = win_icon_path
        self.default_icon_path = user_icon_path

        # 初始化
        self.__login_status = False                                 # 登录状态量：用户是否已登录
        self.login_win = LoginWin("resources/icon/trash_icon.png")  # 主界面包含登录界面
        self.read_config = ConfigProcess("resources/config.ini")    # 配置文件调用接口
        self.db_info = self.read_config.get_config_info()           # 获取数据库数据
        self.db = MySql(self.db_info["db"], self.db_info["pwd"], self.db_info["user"],
                        self.db_info["host"], self.db_info["port"]) # 数据库调用接口
        self.login_user_name = ""                                   # 当前登录用户
        self.init_win()
        self.init_control()
        self.init_connect()

    def init_win(self):
        """
        窗口初始化
        """
        self.setWindowTitle("智慧垃圾分类系统")
        self.setWindowIcon(QIcon(self.win_icon_path))
        self.setFixedSize(1280, 720)

    def init_control(self):
        """
        控件初始化
        """
        # 总体水平布局
        self.total_layout = QHBoxLayout()

        # 右窗口   栈窗口
        self.right_view = QStackedWidget()
        self.right_view.setStyleSheet("background:red")
        self.regist_win = RegistWin()                               # 栈窗口子窗
        self.user_infor_manage_win = UserInforManageWin()
        self.user_infor_add_win = UserInforAddWin()
        self.trash_change_win = TrashChangeWin()
        self.recycle_monitor_win = RecycleMonitorWin()
        self.recycle_record_win = RecycleRecordWin()
        self.error_classify_display_win = ErrorClassifyDisplayWin()
        self.setting_win = SettingWin()

        self.right_view.addWidget(self.regist_win)
        self.right_view.addWidget(self.user_infor_manage_win)
        self.right_view.addWidget(self.user_infor_add_win)
        self.right_view.addWidget(self.trash_change_win)
        self.right_view.addWidget(self.recycle_monitor_win)
        self.right_view.addWidget(self.recycle_record_win)
        self.right_view.addWidget(self.error_classify_display_win)
        self.right_view.addWidget(self.setting_win)

        self.right_view.setCurrentWidget(self.setting_win)           # 设置当前栈窗口

        # 左窗口
        self.left_view = QWidget()
        self.left_view.setStyleSheet("background:yellow")
        self.user_icon = QLabel(self.left_view)                                  # 用户头像
        self.user_icon.setScaledContents(True)                                   # 用户头像大小自适应
        self.user_icon.setPixmap(QPixmap(self.default_icon_path))                # 用户头像设置
        self.user_name = QLabel("user", self.left_view)                          # 用户名
        self.user_name.setAlignment(Qt.AlignCenter)                              # 用户名字体居中
        self.user_name.setStyleSheet("background:red")
        self.exit_button = QPushButton("退出", self.left_view)                    # 退出
        self.login_button = QPushButton("登录", self.left_view)
        self.regist_button = QPushButton("管理员注册", self.left_view)             # 界面切换按钮
        self.user_infor_manage_button = QPushButton("用户信息管理", self.left_view)
        self.trash_change_button = QPushButton("变废为宝模式", self.left_view)
        self.recycle_monitor_button = QPushButton("回收点监控模式", self.left_view)
        self.recycle_record_button = QPushButton("回收物品记录", self.left_view)
        self.error_classify_display_button = QPushButton("错误分类展示", self.left_view)
        self.setting_button = QPushButton("设置", self.left_view)

        self.user_icon.setGeometry(10, 10, 100, 100)                             # 设置按钮绝对布局
        self.user_name.setGeometry(115, 10, 100, 50)
        self.exit_button.setGeometry(115, 70, 100, 50)
        self.login_button.setGeometry(10, 130, 205, 50)
        self.regist_button.setGeometry(10, 210, 205, 50)
        self.user_infor_manage_button.setGeometry(10, 270, 205, 50)
        self.trash_change_button.setGeometry(10, 330, 205, 50)
        self.recycle_monitor_button.setGeometry(10, 390, 205, 50)
        self.recycle_record_button.setGeometry(10, 450, 205, 50)
        self.error_classify_display_button.setGeometry(10, 510, 205, 50)
        self.setting_button.setGeometry(10, 570, 205, 50)

        # 总体布局设置
        self.total_layout.addWidget(self.left_view, 2)
        self.total_layout.addWidget(self.right_view, 8)
        self.setLayout(self.total_layout)

    def init_connect(self):
        """
        信号与槽初始化
        :return:
        """
        # 界面切换
        self.exit_button.clicked.connect(self.login_out_slot)
        self.login_button.clicked.connect(self.login_win_slot)
        self.regist_button.clicked.connect(self.regist_win_slot)
        self.user_infor_manage_button.clicked.connect(self.user_infor_manage_win_slot)
        self.trash_change_button.clicked.connect(self.trash_change_win_slot)
        self.recycle_monitor_button.clicked.connect(self.recycle_monitor_win_slot)
        self.recycle_record_button.clicked.connect(self.recycle_record_win_slot)
        self.error_classify_display_button.clicked.connect(self.error_classify_display_win_slot)
        self.setting_button.clicked.connect(self.setting_win_slot)

        # 跳转用户信息录入界面
        self.user_infor_manage_win.go_to_user_infor_add_signal.connect(self.user_infor_add_win_slot)

        # 返回主界面
        self.login_win.back_to_main_signal.connect(self.back_to_main_slot)

    # 槽函数
    def login_out_slot(self):
        """
        退出登录
        :return:
        """
        if self.__login_status is True:
            # 退出弹窗
            login_out_msg = QMessageBox.question(self, "提示", "你确定要退出登录吗?",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if login_out_msg == QMessageBox.Yes:
                # 修改登出用户状态
                status_flag = self.db.execute("update tbl_adminInfo set adminStatus=0 where adminName='{}';"
                                              .format(self.login_user_name))
                if status_flag is True:
                    # 修改主界面界面数据
                    self.__login_status = False  # 修改登录状态量
                    self.user_icon.setPixmap(QPixmap("resources/icon/user_icon.png"))           # 重置图片
                    self.user_name.setText("null")
                    self.login_user_name = ""                                                   # 重置当前登录用户

                    self.right_view.setCurrentWidget(self.regist_win)  # 设置当前栈窗口
                else:
                    messagebox.showinfo("提示", "系统繁忙，请稍后重试")     # 提示弹窗
            else:
                pass

    def login_win_slot(self):
        """
        登录
        :return:
        """
        if self.__login_status is False:
            self.hide()
            self.login_win.show()                                           # 跳转登录界面
        else:
            pass

    def regist_win_slot(self):
        """
        跳转注册界面槽函数
        :return:
        """
        self.right_view.setCurrentWidget(self.regist_win)               # 设置当前栈窗口

    def user_infor_manage_win_slot(self):
        """
        跳转用户信息管理界面槽函数
        :return:
        """
        if self.__login_status is False:
            self.hide()
            self.login_win.show()                                                       # 跳转登录界面
        else:
            self.user_infor_manage_win.get_login_admin_name_slot(self.login_user_name)  # 获取当前登录用户
            self.right_view.setCurrentWidget(self.user_infor_manage_win)                # 设置当前栈窗口

    def user_infor_add_win_slot(self):
        """
        跳转用户信息录入界面
        :return:
        """
        self.right_view.setCurrentWidget(self.user_infor_add_win)       # 设置当前栈窗口

    def trash_change_win_slot(self):
        """
        跳转变废为宝模式界面
        :return:
        """
        if self.__login_status is False:
            self.hide()
            self.login_win.show()                                       # 跳转登录界面
        else:
            self.right_view.setCurrentWidget(self.trash_change_win)     # 设置当前栈窗口

    def recycle_monitor_win_slot(self):
        """
        跳转回收点监控模式界面
        :return:
        """
        if self.__login_status is False:
            self.hide()
            self.login_win.show()  # 跳转登录界面
        else:
            self.right_view.setCurrentWidget(self.recycle_monitor_win)  # 设置当前栈窗口

    def recycle_record_win_slot(self):
        """
        跳转回收物品记录界面
        :return:
        """
        if self.__login_status is False:
            self.hide()
            self.login_win.show()  # 跳转登录界面
        else:
            self.right_view.setCurrentWidget(self.recycle_record_win)  # 设置当前栈窗口

    def error_classify_display_win_slot(self):
        """
        跳转错误分类展示界面
        :return:
        """
        if self.__login_status is False:
            self.hide()
            self.login_win.show()  # 跳转登录界面
        else:
            self.right_view.setCurrentWidget(self.error_classify_display_win)  # 设置当前栈窗口

    def setting_win_slot(self):
        self.setting_win.init_config()
        self.right_view.setCurrentWidget(self.setting_win)  # 设置当前栈窗口

    def back_to_main_slot(self, user_name, login_judge_flag):
        """
        返回主界面槽函数
        :param user_name: 自定义信号返回的登录用户名
        :param login_judge_flag: 自定义信号返回的登录验证
        :return:
        """
        self.login_win.close()      # 关闭登录界面

        # 判断用户是否登录成功
        if login_judge_flag == 1:
            self.__login_status = True                          # 修改登录状态量
            print("self.__login_status = {}".format(self.__login_status))
            self.login_user_name = user_name                    # 获取当前登录用户名
            self.user_name.setText(user_name)                   # 显示当前登录用户名

            # 获取用户本地头像路径
            admin_icon_path = self.db.select_op("select adminIcon from tbl_adminInfo where adminName='{}';"
                                                .format(user_name))
            user_icon_path = self.db.select_op("select userIcon from tbl_userInfo where userName='{}';"
                                               .format(user_name))
            print(admin_icon_path, len(admin_icon_path), user_icon_path, len(user_icon_path))
            if len(admin_icon_path) != 0:
                print("用户头像路径：{}".format(admin_icon_path[0][0]))

                # 若用户未上传头像
                if admin_icon_path[0][0] == "null":
                    self.user_icon.setPixmap(QPixmap(self.default_icon_path))  # 显示默认头像
                else:
                    self.user_icon.setPixmap(QPixmap(admin_icon_path[0][0]))      # 显示当前登录管理员头像
            elif len(user_icon_path) != 0:
                print("用户头像路径：{}".format(user_icon_path[0][0]))

                # 若用户未上传头像
                if user_icon_path[0][0] == "null":
                    self.user_icon.setPixmap(QPixmap(self.default_icon_path))  # 显示默认头像
                else:
                    self.user_icon.setPixmap(QPixmap(user_icon_path[0][0]))  # 显示当前登录用户头像
        elif login_judge_flag == 0:
            self.__login_status = False         # 修改登录状态量
            print("self.__login_status = {}".format(self.__login_status))
            self.login_user_name = ""
            self.user_name.setText(user_name)   # 显示当前登录用户名

        self.show()                 # 显示主界面


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序

    main_win = MainWin("../resources/icon/trash_icon.png", "../resources/icon/user_icon.png")
    main_win.show()

    sys.exit(app.exec())  # exec()程序持续运行
