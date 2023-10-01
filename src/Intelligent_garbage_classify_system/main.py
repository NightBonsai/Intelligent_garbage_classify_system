# -*- coding: utf-8 -*-
# Project : pythonProject
# Name : main.py
# Author : hhs
# DATE : 2023/8/15 19:40

from PyQt5.QtWidgets import QApplication
from view.MainWin import MainWin
import sys

if __name__ == "__main__":
    """
    项目主入口
    """
    app = QApplication(sys.argv)    # 创建应用程序

    main_win = MainWin("resources/icon/trash_icon.png", "resources/icon/user_icon.png")
    main_win.show()

    sys.exit(app.exec())            # exec()程序持续运行
