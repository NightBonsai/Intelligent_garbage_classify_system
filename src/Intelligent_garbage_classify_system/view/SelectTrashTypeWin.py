# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : SelectTrashTypeWin.py
# Author : hhs
# DATE : 2023/9/23 11:35

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class SelectTrashTypeWin(QWidget):
    """
    选择物品类型界面
    """
    # 自定义信号 带参信号：传字符串&整型    选择的物品类型
    back_to_trash_change_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()  # 调用父类构造函数

        # 初始化
        self.init_win()
        self.init_control()
        self.init_connect()

    def init_win(self):
        """
        窗口初始化
        :return:
        """
        self.setFixedSize(300, 200)
        self.setStyleSheet("background:red")
        self.setWindowFlags(Qt.FramelessWindowHint)     # 隐藏标题栏

    def init_control(self):
        """
        控件初始化
        :return:
        """
        self.select_trash_type_title = QLabel("所属分类", self)
        self.select_trash_type_title.setFont(QFont("楷体", 12))
        self.select_trash_type_edit = QComboBox(self)
        self.select_trash_type_edit.setStyleSheet("background:yellow")
        self.select_trash_type_edit.addItem("电池")
        self.select_trash_type_edit.addItem("瓶子")
        self.select_trash_type_edit.addItem("叶子")
        self.select_trash_type_edit.addItem("袋子")
        self.yes_button = QPushButton("确定", self)
        self.yes_button.setStyleSheet("background:yellow")

        self.select_trash_type_title.setGeometry(30, 50, 150, 50)
        self.select_trash_type_edit.setGeometry(125, 50, 150, 50)
        self.yes_button.setGeometry(30, 110, 245, 50)

    def init_connect(self):
        """
        信号与槽初始化
        :return:
        """
        self.yes_button.clicked.connect(self.back_to_trash_change_slot)

    def back_to_trash_change_slot(self):
        """
        发送返回变废为宝界面信号
        :return:
        """
        print("选择物品类型------------------------------------------------------------------------------------------------")
        # 获取选择的下拉框下标
        index = self.select_trash_type_edit.currentIndex()
        print("选择的物品类型： ", index)

        # 发送信号
        self.back_to_trash_change_signal.emit(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序

    select_trash_type_win = SelectTrashTypeWin()
    select_trash_type_win.show()

    sys.exit(app.exec())  # exec()程序持续运行
