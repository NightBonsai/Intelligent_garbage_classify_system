# -*- coding: utf-8 -*-
# Project : homework
# Name : LoginWin.py
# Author : hhs
# DATE : 2023/7/20 15:51
import sys
import cv2
import requests
import base64
import json
import time
from tkinter import messagebox

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tools.BaiduAI import BaiduAI
from mySql.MySql import MySql
from tools.ConfigProcess import ConfigProcess


class LoginWin(QWidget):
    """
    登录界面类
    """
    # 自定义信号 带参信号：传字符串&整型    用户名 登录成功判断
    back_to_main_signal = pyqtSignal(str, int)

    def __init__(self, win_icon_path):
        super().__init__()

        # 接收传参
        self.win_icon_path = win_icon_path

        # 初始化
        self.cap = 0
        self.camera_flag = False                                        # 摄像头开启状态符
        self.user_face_mat = ""                                         # 用户头像矩阵
        self.ai = BaiduAI()                                             # 百度AI调用接口
        self.read_config = ConfigProcess("resources/config.ini")        # 配置文件调用接口
        self.db_info = self.read_config.get_config_info()               # 获取数据库数据
        self.db = MySql(self.db_info["db"], self.db_info["pwd"], self.db_info["user"],
                         self.db_info["host"], self.db_info["port"])    # 数据库调用接口
        self.init_win()
        self.init_control()
        self.init_connect()

    def init_win(self):
        """
        窗口初始化
        """
        self.setWindowTitle("智能垃圾分类系统")
        self.setWindowIcon(QIcon(self.win_icon_path))
        self.setFixedSize(1280, 720)

    def init_control(self):
        """
        控件初始化
        """
        self.login_win_title = QLabel("智能垃圾分类系统登录", self)
        self.login_win_title.setFont(QFont("楷体", 16, QFont.Bold))   # 设置label控件字体样式
        self.open_camera_button = QPushButton("打开摄像头", self)
        self.face_detect_button = QPushButton("检测人脸", self)
        self.face_detect_button.setEnabled(False)
        self.back_to_main_button = QPushButton("返回", self)
        self.face_detect_frame = QLabel(self)
        self.face_detect_frame.setScaledContents(True)
        self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))

        self.login_win_title.setGeometry(470, 10, 300, 50)
        self.open_camera_button.setGeometry(360, 100, 100, 50)
        self.face_detect_button.setGeometry(565, 100, 100, 50)
        self.back_to_main_button.setGeometry(770, 100, 100, 50)
        self.face_detect_frame.setGeometry(360, 180, 512, 512)

    def init_connect(self):
        """
        信号与槽初始化
        """
        self.open_camera_button.clicked.connect(self.open_camera_slot)
        self.face_detect_button.clicked.connect(self.face_detect_slot)
        self.back_to_main_button.clicked.connect(self.back_to_main_login_fail_slot)

    # 槽函数
    def open_camera_slot(self):
        """
        打开摄像头检测人脸，登录验证
        """
        self.open_camera_button.setEnabled(False)               # 冻结打开摄像头开关
        self.face_detect_button.setEnabled(True)                # 解冻人脸检测按钮

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)           # 打开摄像头
        self.camera_flag = True                                 # 摄像头状态符 True
        while True:
            if self.cap.isOpened():
                status, self.user_face_mat = self.cap.read()    # 读取状态，帧

                if status:
                    if self.camera_flag is False:               # 若摄像头已关闭
                        """
                        此处进行人脸检测
                        """
                        break

                    # 摄像头捕捉帧显示在QLabel中
                    rgb_mat = cv2.cvtColor(self.user_face_mat, cv2.COLOR_BGR2RGB)                   # 编码转RGB
                    q_image = QImage(rgb_mat.data, rgb_mat.shape[1], rgb_mat.shape[0],              # 转QImage
                                     rgb_mat.shape[1] * 3, QImage.Format_RGB888)

                    self.face_detect_frame.setPixmap(QPixmap.fromImage(q_image).scaled(512, 512))  # 显示在QLabel中

                cv2.waitKey(10)
        self.cap.release()

        self.user_face_mat = None                               # 清空获取的图像数据
        self.open_camera_button.setEnabled(True)                # 解冻打开摄像头开关
        self.face_detect_button.setEnabled(False)               # 冻结人脸检测按钮
        self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))

    def face_detect_slot(self):
        """
        请求百度AI平台，框出人脸
        :return:
        """
        # 关闭摄像头
        self.camera_flag = False  # 关闭摄像头

        # 检测一张人脸
        access_token = self.ai.get_access_token("5mGMwYSVemPCN9zLbtZHlQLh",
                                                "HT5ArjvXAfui3tvm2ifSZujQI3D8lGc4")
        ret_dict = self.ai.detect_face(self.user_face_mat, access_token)
        if ret_dict["face_num"] == 0:
            QMessageBox.information(self, "登录提示", "未检测到人脸")
        elif ret_dict["face_num"] > 1:
            QMessageBox.information(self, "登录提示", "检测到多张人脸")
        elif ret_dict["face_num"] == 1:
            x, y, width, height = ret_dict["image"]  # 获取人脸位置和大小

            # 画框
            img_mat = self.user_face_mat
            cv2.rectangle(img_mat, (x, y), (x + width, y + height), (0, 255, 0), 2)  # 默认打开方式BGR
            rgb_mat = cv2.cvtColor(img_mat, cv2.COLOR_BGR2RGB)  # 编码转置，BGR转RGB
            q_image = QImage(rgb_mat.data, rgb_mat.shape[1], rgb_mat.shape[0],  # 转QImage
                             rgb_mat.shape[1] * 3, QImage.Format_RGB888)
            self.face_detect_frame.setPixmap(QPixmap.fromImage(q_image).scaled(512, 512))  # 显示在QLabel中
            time.sleep(1)

            # 进行人脸登录
            self.login_judge_slot(img_mat[y:y+height, x:x+width])

    def login_judge_slot(self, face_mat):
        """
        请求百度AI平台进行人脸登录
        :param face_mat: 框出的人脸矩阵
        :return:
        """
        print("人脸登录验证----------------------------------------------------------------------------------------------")
        # 上传人脸图像至百度AI平台进行人脸登录
        print(face_mat.shape, type(face_mat))
        access_token = self.ai.get_access_token("5mGMwYSVemPCN9zLbtZHlQLh",
                                                "HT5ArjvXAfui3tvm2ifSZujQI3D8lGc4")
        user_name = self.ai.face_match(face_mat, "admins,users", access_token)
        print("登录用户为：{}".format(user_name))

        if user_name is not False:
            # 发送返回主界面信号
            self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))  # 重置图片
            self.back_to_main_signal.emit(user_name, 1)
        else:
            messagebox.showinfo("提示", "登录失败，人脸规格不符")    # 提示弹窗
            self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))  # 重置图片

    def back_to_main_login_fail_slot(self):
        """
        关闭摄像头，发送返回主界面信号
        :return:
        """
        # 关闭摄像头
        if self.camera_flag is True:
            self.camera_flag = False                                                # 状态位置False
            self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))    # 重置图片

        # 发送返回主界面信号
        self.back_to_main_signal.emit("null", 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # "../resources/icon/school_icon.png", "../resources/icon/face_detect_icon.png"
    login_win = LoginWin("resources/icon/trash_icon.png")
    login_win.show()

    sys.exit(app.exec())
