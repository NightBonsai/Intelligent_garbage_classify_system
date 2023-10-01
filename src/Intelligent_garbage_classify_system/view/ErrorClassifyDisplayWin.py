# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : ErrorClassifyDisplayWin.py
# Author : hhs
# DATE : 2023/8/15 20:34

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from mySql.MySql import MySql
from tools.ConfigProcess import ConfigProcess
from tkinter import messagebox


class ErrorClassifyDisplayWin(QWidget):
    """
    错误分类展示界面
    """
    def __init__(self):
        super().__init__()  # 调用父类构造函数

        # 初始化
        self.read_config = ConfigProcess("resources/config.ini")                        # 配置文件调用接口
        self.db_info = self.read_config.get_config_info()                               # 获取数据库数据
        self.db = MySql(self.db_info["db"], self.db_info["pwd"], self.db_info["user"],
                        self.db_info["host"], self.db_info["port"])                     # 数据库调用接口
        self.error_record_list = None                                                   # 错误记录列表
        self.init_win()
        self.init_control()
        self.init_connect()

    def init_win(self):
        """
        窗口初始化
        """
        self.setFixedSize(1024, 720)

    def init_control(self):
        """
        控件初始化
        """
        self.title = QLabel("错误分类展示", self)
        self.origin_time_title = QLabel("选择起始时间", self)
        self.origin_time_title.setFont(QFont("楷体", 12))
        self.ending_time_title = QLabel("选择结束时间", self)
        self.ending_time_title.setFont(QFont("楷体", 12))
        self.origin_time_edit = QDateTimeEdit(QDate.currentDate(), self)                      # 指定当前地日期为控件的日期
        self.origin_time_edit.setDisplayFormat('yyyy-MM-dd')                                            # 设置显示格式
        self.origin_time_edit.setCalendarPopup(True)                                                    # 设置日历可弹出
        self.origin_time_edit.setStyleSheet("background:yellow")
        self.ending_time_edit = QDateTimeEdit(QDate.currentDate(), self)
        self.ending_time_edit.setDisplayFormat('yyyy-MM-dd')
        self.ending_time_edit.setCalendarPopup(True)
        self.ending_time_edit.setStyleSheet("background:yellow")
        self.search_button = QPushButton("检索", self)
        self.search_button.setStyleSheet("background:yellow")
        self.error_record_table = QTableWidget(self)
        self.error_record_table.setColumnCount(5)                                                           # 设置列数
        self.error_record_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)               # 表格横向缩放
        self.error_record_table.setHorizontalHeaderLabels(["序号", "错误类别", "物品类型", "图片", "时间"])      # 设置列标题
        self.error_record_table.setStyleSheet("background:yellow")

        self.title.setGeometry(10, 10, 150, 50)
        self.origin_time_title.setGeometry(10, 70, 150, 50)
        self.ending_time_title.setGeometry(350, 70, 150, 50)
        self.origin_time_edit.setGeometry(170, 70, 150, 50)
        self.ending_time_edit.setGeometry(510, 70, 150, 50)
        self.search_button.setGeometry(850, 70, 150, 50)
        self.error_record_table.setGeometry(10, 130, 1004, 570)

    def init_connect(self):
        """"
        信号与槽初始化
        """
        self.search_button.clicked.connect(self.search_slot)

    # 槽函数
    def search_slot(self):
        """
        依据时间段检索错误回收记录数据
        :return:
        """
        # 检索对应时间段数据
        print("错误回收记录检索------------------------------------------------------------------------------------------------")
        print("开始时间: ", self.origin_time_edit.text())
        print("结束时间: ", self.ending_time_edit.text())
        self.error_record_list = self.db.select_op("select * from tbl_errorRecordInfo where "
                                                   "createTime>='{} 00:00:00' and createTime<'{} 23:59:59';"
                                                   .format(self.origin_time_edit.text(), self.ending_time_edit.text()))
        self.error_record_table.setRowCount(len(self.error_record_list))    # 设置行数
        print(self.error_record_list, len(self.error_record_list))

        for i in range(len(self.error_record_list)):
            # 创建物品信息item
            self.row_item = QTableWidgetItem("{}".format(i + 1))
            if self.error_record_list[i][1] == 0:
                self.error_type_item = QTableWidgetItem("电池")
            elif self.error_record_list[i][1] == 1:
                self.error_type_item = QTableWidgetItem("瓶子")
            elif self.error_record_list[i][1] == 2:
                self.error_type_item = QTableWidgetItem("叶子")
            elif self.error_record_list[i][1] == 3:
                self.error_type_item = QTableWidgetItem("袋子")
            else:
                self.error_type_item = QTableWidgetItem("null")

            if self.error_record_list[i][2] == 0:
                self.class_type_item = QTableWidgetItem("电池")
            elif self.error_record_list[i][2] == 1:
                self.class_type_item = QTableWidgetItem("瓶子")
            elif self.error_record_list[i][2] == 2:
                self.class_type_item = QTableWidgetItem("叶子")
            elif self.error_record_list[i][2] == 3:
                self.class_type_item = QTableWidgetItem("袋子")
            else:
                self.class_type_item = QTableWidgetItem("null")

            self.trash_icon_item = QTableWidgetItem()
            self.trash_icon_item.setFlags(Qt.ItemIsEnabled)
            if self.error_record_list[i][3] == "null":
                self.trash_icon_item.setIcon(QIcon("resources/icon/trash_icon.png"))
            else:
                self.trash_icon_item.setIcon(QIcon(self.error_record_list[i][3]))
            self.create_time_item = QTableWidgetItem("{}".format(self.error_record_list[i][4]))

            # 错误信息item添加进QTableWidget中
            self.error_record_table.setItem(i, 0, self.row_item)
            self.error_record_table.setItem(i, 1, self.error_type_item)
            self.error_record_table.setItem(i, 2, self.class_type_item)
            self.error_record_table.setIconSize(QSize(200, 200))                    # 设置图片栏显示大小
            self.error_record_table.setColumnWidth(i, 200)
            self.error_record_table.setRowHeight(i, 200)
            self.error_record_table.setItem(i, 3, self.trash_icon_item)
            self.error_record_table.setItem(i, 4, self.create_time_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序

    error_classify_display_win = ErrorClassifyDisplayWin()
    error_classify_display_win.show()

    sys.exit(app.exec())  # exec()程序持续运行
