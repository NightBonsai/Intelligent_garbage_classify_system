# -*- coding: utf-8 -*-
# Project : homework6
# Name : RegistWin.py
# Author : hhs
# DATE : 2023/7/27 14:55
import sys
import cv2
import time
import datetime
from tkinter import messagebox

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tools.BaiduAI import BaiduAI
from mySql.MySql import MySql
from tools.ConfigProcess import ConfigProcess


class RegistWin(QWidget):
    """
    注册界面
    """
    def __init__(self):
        super().__init__()  # 调用父类构造函数

        # 初始化
        self.camera_flag = False                                    # 摄像头开启状态符
        self.user_face_mat = ""                                     # 用户头像矩阵
        self.ai = BaiduAI()                                         # 百度AI调用接口
        self.read_config = ConfigProcess("resources/config.ini")    # 配置文件调用接口
        self.db_info = self.read_config.get_config_info()           # 获取数据库数据
        self.db = MySql(self.db_info["db"], self.db_info["pwd"], self.db_info["user"],
                        self.db_info["host"], self.db_info["port"]) # 数据库调用接口
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
        self.title = QLabel("管理员注册界面", self)
        self.admin_name_title = QLabel("管理员", self)
        self.admin_name_title.setFont(QFont("楷体", 12))
        self.admin_pwd_title = QLabel("输入密码", self)
        self.admin_pwd_title.setFont(QFont("楷体", 12))
        self.admin_pwd_reconfirm_title = QLabel("确认密码", self)
        self.admin_pwd_reconfirm_title.setFont(QFont("楷体", 12))
        self.admin_name_edit = QLineEdit(self)
        self.admin_name_edit.setMaxLength(12)
        self.admin_name_edit.setStyleSheet("background:yellow")
        self.admin_pwd_edit = QLineEdit(self)
        self.admin_pwd_edit.setMaxLength(12)
        self.admin_pwd_edit.setEchoMode(QLineEdit.Password)
        self.admin_pwd_edit.setStyleSheet("background:yellow")
        self.admin_pwd_reconfirm_edit = QLineEdit(self)
        self.admin_pwd_reconfirm_edit.setMaxLength(12)
        self.admin_pwd_reconfirm_edit.setEchoMode(QLineEdit.Password)
        self.admin_pwd_reconfirm_edit.setStyleSheet("background:yellow")

        self.open_camera_button = QPushButton("打开摄像头", self)
        self.open_camera_button.setStyleSheet("background:yellow")
        self.face_detect_button = QPushButton("检测人脸", self)
        self.face_detect_button.setEnabled(False)
        self.face_detect_button.setStyleSheet("background:yellow")
        self.close_camera_button = QPushButton("关闭摄像头", self)
        self.close_camera_button.setStyleSheet("background:yellow")
        self.face_detect_frame = QLabel(self)
        self.face_detect_frame.setScaledContents(True)
        self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))

        self.title.setGeometry(10, 10, 150, 50)
        self.admin_name_title.setGeometry(10, 70, 150, 50)
        self.admin_name_edit.setGeometry(100, 70, 150, 50)
        self.admin_pwd_title.setGeometry(10, 130, 150, 50)
        self.admin_pwd_edit.setGeometry(100, 130, 150, 50)
        self.admin_pwd_reconfirm_title.setGeometry(10, 190, 150, 50)
        self.admin_pwd_reconfirm_edit.setGeometry(100, 190, 150, 50)
        self.open_camera_button.setGeometry(300, 70, 150, 50)
        self.face_detect_button.setGeometry(480, 70, 150, 50)
        self.close_camera_button.setGeometry(660, 70, 150, 50)
        self.face_detect_frame.setGeometry(300, 150, 512, 512)

    def init_connect(self):
        """
        信号与槽初始化
        :return:
        """
        self.open_camera_button.clicked.connect(self.open_camera_slot)
        self.face_detect_button.clicked.connect(self.face_detect_slot)
        self.close_camera_button.clicked.connect(self.close_camera_slot)

    # 槽函数
    def open_camera_slot(self):
        """
        打开摄像头检测人脸
        :return:
        """
        self.open_camera_button.setEnabled(False)       # 冻结打开摄像头开关
        self.face_detect_button.setEnabled(True)        # 解冻人脸检测按钮

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)   # 打开摄像头
        self.camera_flag = True                         # 摄像头状态符 True
        while True:
            if self.cap.isOpened():
                if self.camera_flag is False:  # 若摄像头已关闭
                    """
                    此处进行人脸检测
                    """
                    break

                status, self.user_face_mat = self.cap.read()  # 读取状态，帧

                if status:
                    # 摄像头捕捉帧显示在QLabel中
                    rgb_mat = cv2.cvtColor(self.user_face_mat, cv2.COLOR_BGR2RGB)  # 编码转RGB
                    q_image = QImage(rgb_mat.data, rgb_mat.shape[1], rgb_mat.shape[0],  # 转QImage
                                     rgb_mat.shape[1] * 3, QImage.Format_RGB888)

                    self.face_detect_frame.setPixmap(QPixmap.fromImage(q_image).scaled(512, 512))  # 显示在QLabel中

                cv2.waitKey(10)
        self.cap.release()

        self.user_face_mat = None                       # 清空获取的图像数据
        self.open_camera_button.setEnabled(True)        # 解冻打开摄像头开关
        self.face_detect_button.setEnabled(False)       # 冻结人脸检测按钮
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
            print(x, y, width, height)

            # 画框
            img_mat = self.user_face_mat
            cv2.rectangle(img_mat, (x, y), (x + width, y + height), (0, 255, 0), 2)  # 默认打开方式BGR
            rgb_mat = cv2.cvtColor(img_mat, cv2.COLOR_BGR2RGB)  # 编码转置，BGR转RGB
            q_image = QImage(rgb_mat.data, rgb_mat.shape[1], rgb_mat.shape[0],  # 转QImage
                             rgb_mat.shape[1] * 3, QImage.Format_RGB888)
            self.face_detect_frame.setPixmap(QPixmap.fromImage(q_image).scaled(512, 512))  # 显示在QLabel中
            time.sleep(1)

            # 进行人脸注册
            self.regist_judge_slot(img_mat[y:y + height, x:x + width])

    def regist_judge_slot(self, face_mat):
        """
        请求百度AI平台进行人脸注册
        :param face_mat: 框出的人脸矩阵
        :return:
        """
        print("人脸注册验证----------------------------------------------------------------------------------------------")
        # 表单判空操作
        if self.admin_name_edit.text() and self.admin_pwd_edit.text() and self.admin_pwd_reconfirm_edit.text():
            # 判断两次密码输入是否一致
            if self.admin_pwd_edit.text() == self.admin_pwd_reconfirm_edit.text():
                # 判断用户名是否已经存在
                search_flag = self.db.select_op("select * from tbl_adminInfo where adminName='{}';"
                                                .format(self.admin_name_edit.text()))
                # 若用户名不存在
                if len(search_flag) == 0:
                    # 判断人脸库是否存在对应人脸
                    # cv2.imshow("result", face_mat)
                    access_token = self.ai.get_access_token("5mGMwYSVemPCN9zLbtZHlQLh",
                                                            "HT5ArjvXAfui3tvm2ifSZujQI3D8lGc4")
                    match_flag = self.ai.face_match(face_mat, "admins,users", access_token)
                    print(match_flag)
                    # 若未检测到对应人脸
                    if match_flag is False:
                        # 上传人脸图像至百度AI平台进行人脸注册
                        access_token = self.ai.get_access_token("5mGMwYSVemPCN9zLbtZHlQLh",
                                                                "HT5ArjvXAfui3tvm2ifSZujQI3D8lGc4")
                        regist_flag = self.ai.face_regist(face_mat, "admins", self.admin_name_edit.text(), access_token)
                        if regist_flag is not False:
                            # 数据库写入新管理员信息
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # 获取当前时间
                            status_flag = self.db.insert_op("insert into tbl_adminInfo(adminName,adminPwd"
                                                            ",adminStatus,adminIcon,registTime) "
                                                            "values('{}','{}','0','null','{}');"
                                                            .format(self.admin_name_edit.text(),
                                                                    self.admin_pwd_edit.text(), current_time))
                            print("数据库写入新管理员信息：{}".format(status_flag))
                            if status_flag is not False:
                                self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))  # 重置图片
                                self.admin_name_edit.setText("")                                             # 表单清空
                                self.admin_pwd_edit.setText("")
                                self.admin_pwd_reconfirm_edit.setText("")
                                messagebox.showinfo("提示", "注册成功")                                        # 提示弹窗
                            else:
                                messagebox.showinfo("提示", "系统繁忙，请稍后重试")                                 # 提示弹窗
                                self.admin_name_edit.setText("")  # 表单清空
                                self.admin_pwd_edit.setText("")
                                self.admin_pwd_reconfirm_edit.setText("")
                        else:
                            messagebox.showinfo("提示", "注册失败，请稍后重试")
                            self.admin_name_edit.setText("")  # 表单清空
                            self.admin_pwd_edit.setText("")
                            self.admin_pwd_reconfirm_edit.setText("")
                    else:
                        messagebox.showinfo("提示", "人脸数据已存在")
                        self.admin_name_edit.setText("")  # 表单清空
                        self.admin_pwd_edit.setText("")
                        self.admin_pwd_reconfirm_edit.setText("")
                else:
                    messagebox.showinfo("提示", "用户名已存在")
                    self.admin_name_edit.setText("")  # 表单清空
                    self.admin_pwd_edit.setText("")
                    self.admin_pwd_reconfirm_edit.setText("")
            else:
                messagebox.showinfo("提示", "密码输入不一致")
                self.admin_name_edit.setText("")  # 表单清空
                self.admin_pwd_edit.setText("")
                self.admin_pwd_reconfirm_edit.setText("")
        else:
            messagebox.showinfo("提示", "表单不能为空")                                         # 判空提示弹窗

    def close_camera_slot(self):
        """
        关闭摄像头
        :return:
        """
        if self.camera_flag is True:
            self.camera_flag = False                                                # 状态位置False
            self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))    # 重置图片


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序

    regist_win = RegistWin()
    regist_win.show()

    sys.exit(app.exec())  # exec()程序持续运行
