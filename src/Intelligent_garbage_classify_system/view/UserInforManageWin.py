# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : UserInforManageWin.py
# Author : hhs
# DATE : 2023/8/15 19:57

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from mySql.MySql import MySql
from tools.ConfigProcess import ConfigProcess
from tkinter import messagebox


class UserInforManageWin(QWidget):
    """
    用户数据管理界面
    """
    # 自定义信号 跳转用户信息录入界面
    go_to_user_infor_add_signal = pyqtSignal()

    def __init__(self):
        super().__init__()  # 调用父类构造函数

        # 初始化
        self.read_config = ConfigProcess("resources/config.ini")        # 配置文件调用接口
        self.db_info = self.read_config.get_config_info()               # 获取数据库数据
        self.db = MySql(self.db_info["db"], self.db_info["pwd"], self.db_info["user"],
                        self.db_info["host"], self.db_info["port"])     # 数据库调用接口
        self.user_infor_list = 0                                        # 查询的用户数据列表
        self.login_admin_name = ""                                      # 当前登录的管理员用户名
        self.init_win()
        self.init_control()
        self.init_connect()

    def init_win(self):
        """
        窗口初始化
        :return:
        """
        self.setFixedSize(1024, 720)

    def init_control(self):
        """
        控件初始化
        :return:
        """
        self.title = QLabel("用户数据管理界面", self)
        self.user_manage_title = QLabel("用户信息管理", self)
        self.user_manage_title.setFont(QFont("楷体", 12))
        self.admin_authentication_title = QLabel("管理员身份验证", self)
        self.admin_authentication_title.setFont(QFont("楷体", 12))
        self.admin_authentication_edit = QLineEdit(self)
        self.admin_authentication_edit.setMaxLength(12)
        self.admin_authentication_edit.setEchoMode(QLineEdit.Password)
        self.admin_authentication_edit.setStyleSheet("background:yellow")
        self.user_infor_add_button = QPushButton("添加用户信息", self)
        self.user_infor_add_button.setStyleSheet("background:yellow")
        self.user_infor_renew_button = QPushButton("刷新用户信息", self)
        self.user_infor_renew_button.setStyleSheet("background:yellow")
        self.user_manage_table = QTableWidget(self)
        self.user_manage_table.setColumnCount(5)                                                # 设置列数
        self.user_manage_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)     # 表格横向缩放
        self.user_manage_table.setHorizontalHeaderLabels(["序号", "id", "用户名", "头像", "管理"])   # 设置列标题
        self.user_manage_table.setStyleSheet("background:yellow")

        self.title.setGeometry(10, 10, 150, 50)
        self.user_manage_title.setGeometry(10, 70, 150, 50)
        self.admin_authentication_title.setGeometry(530, 70, 150, 50)
        self.admin_authentication_edit.setGeometry(690, 70, 150, 50)
        self.user_infor_add_button.setGeometry(170, 70, 150, 50)
        self.user_infor_renew_button.setGeometry(850, 70, 150, 50)
        self.user_manage_table.setGeometry(10, 130, 1004, 570)

    def init_connect(self):
        """
        信号与槽初始化
        :return:
        """
        self.user_infor_add_button.clicked.connect(self.go_to_user_infor_add_slot)
        self.user_infor_renew_button.clicked.connect(self.user_infor_renew_slot)

    # 槽函数
    def get_login_admin_name_slot(self, admin_name):
        """
        获取当前登录的管理员用户名
        :param admin_name: 管理员用户名
        :return:
        """
        self.login_admin_name = admin_name

    def go_to_user_infor_add_slot(self):
        """
        发送跳转用户信息录入界面信号
        :return:
        """
        self.go_to_user_infor_add_signal.emit()

    def user_infor_renew_slot(self):
        """
        刷新用户数据列表
        :return:
        """
        print("刷新用户数据列表----------------------------------------------------------------------------------------")
        self.user_infor_list = self.db.select_op("select userId,userName,userIcon,userStatus from tbl_userInfo;")
        self.user_manage_table.setRowCount(len(self.user_infor_list))       # 设置行数
        print(self.user_infor_list, len(self.user_infor_list))

        for i in range(len(self.user_infor_list)):
            # 创建用户信息item
            self.row_item = QTableWidgetItem("{}".format(i + 1))
            self.user_id_item = QTableWidgetItem("{}".format(self.user_infor_list[i][0]))
            self.user_name_item = QTableWidgetItem("{}".format(self.user_infor_list[i][1]))
            self.user_icon_item = QTableWidgetItem()
            self.user_icon_item.setFlags(Qt.ItemIsEnabled)                              # 用户点击表格时，图片被选中
            if self.user_infor_list[i][2] == "null":
                self.user_icon_item.setIcon(QIcon("resources/icon/user_icon.png"))
            else:
                self.user_icon_item.setIcon(QIcon(self.user_infor_list[i][2]))
            self.user_freeze_item = 0
            if self.user_infor_list[i][3] == 0:
                self.user_freeze_item = QPushButton("冻结", self)
            # 判断是否为冻结用户
            elif self.user_infor_list[i][3] == 1:
                self.user_freeze_item = QPushButton("解冻", self)
            self.user_freeze_item.setStyleSheet('QPushButton{margin:3px}')
            self.user_freeze_item.clicked.connect(self.user_freeze_slot)    # 信号与槽，进行冻结or解冻

            # 用户信息item添加进QTableWidget中
            self.user_manage_table.setItem(i, 0, self.row_item)
            self.user_manage_table.setItem(i, 1, self.user_id_item)
            self.user_manage_table.setItem(i, 2, self.user_name_item)
            self.user_manage_table.setIconSize(QSize(50, 50))               # 设置图片栏显示大小
            self.user_manage_table.setColumnWidth(i, 50)
            self.user_manage_table.setRowHeight(i, 50)
            self.user_manage_table.setItem(i, 3, self.user_icon_item)
            self.user_manage_table.setCellWidget(i, 4, self.user_freeze_item)

    def user_freeze_slot(self):
        """
        冻结用户判断
        :param row: 冻结按钮位于第几行
        :param col: 冻结按钮位于第几列
        :return:
        """
        print("冻结用户验证----------------------------------------------------------------------------------------------")
        # 表单验证
        if self.admin_authentication_edit.text() == "":
            messagebox.showinfo("提示", "请先输入密码进行管理员验证")  # 提示弹窗
        else:
            # 管理员密码验证
            admin_pwd = self.db.select_op("select adminPwd from tbl_adminInfo where adminName='{}';"
                                          .format(self.login_admin_name))
            print("管理员密码：{}".format(admin_pwd[0][0]))
            if self.admin_authentication_edit.text() == admin_pwd[0][0]:
                # 获取当前操作按钮坐标
                button = self.sender()
                if button:
                    row = self.user_manage_table.indexAt(button.pos()).row()
                    column = self.user_manage_table.indexAt(button.pos()).column()
                    # self.tableWidget.removeRow(row)
                    print('当前操作按钮坐标: ', row, column)

                # 判断当前用户是否已冻结
                if self.user_infor_list[row][3] == 0:                                                           # 未冻结
                    freeze_flag = self.db.execute("update tbl_userInfo set userStatus=1 where userName='{}';"
                                                  .format(self.user_infor_list[row][1]))
                    if freeze_flag is True:
                        pass
                    else:
                        messagebox.showinfo("提示", "用户冻结失败，请稍后重试")  # 提示弹窗
                elif self.user_infor_list[row][3] == 1:                                                         # 已冻结
                    unfreeze_flag = self.db.execute("update tbl_userInfo set userStatus=0 where userName='{}';"
                                                    .format(self.user_infor_list[row][1]))
                    if unfreeze_flag is True:
                        pass
                    else:
                        messagebox.showinfo("提示", "用户解冻失败，请稍后重试")  # 提示弹窗
                # 刷新用户数据表
                self.admin_authentication_edit.setText("")
                self.user_infor_renew_slot()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序

    user_infor_manage_win = UserInforManageWin()
    user_infor_manage_win.show()

    sys.exit(app.exec())  # exec()程序持续运行
