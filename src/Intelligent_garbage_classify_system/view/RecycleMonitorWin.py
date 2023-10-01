# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : RecycleMonitorWin.py
# Author : hhs
# DATE : 2023/8/15 20:30

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class RecycleMonitorWin(QWidget):
    """
    回收点监控模式界面
    """
    def __init__(self):
        super().__init__()  # 调用父类构造函数

        # 初始化
        self.init_win()
        self.init_control()

    def init_win(self):
        self.setFixedSize(1024, 720)

    def init_control(self):
        self.title = QLabel("回收点监控模式", self)
        self.title.setGeometry(10, 10, 150, 50)
