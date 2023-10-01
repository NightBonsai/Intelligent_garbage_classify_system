# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : TrashChangeWin.py
# Author : hhs
# DATE : 2023/8/15 19:58

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
from tools.ClassifyModel import ClassifyModel

from view.SelectTrashTypeWin import SelectTrashTypeWin


class TrashChangeWin(QWidget):
    """
    变废为宝模式界面
    """
    def __init__(self):
        super().__init__()  # 调用父类构造函数

        # 初始化
        self.camera_flag = False                                    # 摄像头开启状态符
        self.login_user_flag = False                                # 用户登录状态符
        self.detect_result_flag = False                             # 物品检测状态符
        self.select_trash_type = None                               # 选择的物品类型
        self.login_user_name = ""                                   # 登录用户名
        self.detect_mat = ""                                        # 检测到的图片矩阵
        self.predict_mat = ""                                       # 用于检测的图片矩阵
        self.ai = BaiduAI()                                         # 百度AI调用接口
        self.read_config = ConfigProcess("resources/config.ini")    # 配置文件调用接口
        self.config_info = self.read_config.get_config_info()       # 获取数据库数据
        self.db = MySql(self.config_info["db"], self.config_info["pwd"], self.config_info["user"],
                        self.config_info["host"], self.config_info["port"])  # 数据库调用接口
        self.ob_model = ClassifyModel()                             # 模型预测调用接口
        self.model = self.ob_model.create_net()                     # 创建网络模型
        self.model.load(self.config_info["model"])                  # 加载模型
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
        self.title = QLabel("变废为宝模式", self)
        self.login_user_name_title = QLabel("用户: ", self)
        self.login_user_name_title.setFont(QFont("楷体", 12))
        self.login_user_name_title.setStyleSheet("background:yellow")
        self.open_camera_button = QPushButton("打开摄像头", self)
        self.open_camera_button.setStyleSheet("background:yellow")
        self.face_detect_button = QPushButton("用户识别", self)
        self.face_detect_button.setEnabled(False)
        self.face_detect_button.setStyleSheet("background:yellow")
        self.trash_detect_button = QPushButton("宝贝识别", self)
        self.trash_detect_button.setEnabled(False)
        self.trash_detect_button.setStyleSheet("background:yellow")
        self.trash_recycle_button = QPushButton("物品回收", self)
        self.trash_recycle_button.setStyleSheet("background:yellow")
        self.classify_error_button = QPushButton("分类报错", self)
        self.classify_error_button.setStyleSheet("background:yellow")
        self.trash_detect_result = QLabel("物品类型：", self)
        self.trash_detect_result.setFont(QFont("楷体", 12))
        self.trash_detect_result.setStyleSheet("background:yellow")
        self.face_detect_frame = QLabel(self)
        self.face_detect_frame.setScaledContents(True)
        self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))
        self.select_trash_type_win = SelectTrashTypeWin()       # 选择物品类型界面

        self.title.setGeometry(10, 10, 150, 50)
        self.login_user_name_title.setGeometry(100, 70, 150, 50)
        self.open_camera_button.setGeometry(100, 170, 150, 50)
        self.face_detect_button.setGeometry(100, 270, 150, 50)
        self.trash_detect_button.setGeometry(100, 370, 150, 50)
        self.trash_recycle_button.setGeometry(100, 470, 150, 50)
        self.classify_error_button.setGeometry(100, 570, 150, 50)
        self.trash_detect_result.setGeometry(300, 70, 512, 50)
        self.face_detect_frame.setGeometry(300, 150, 512, 512)

    def init_connect(self):
        """
        信号与槽初始化
        """
        self.open_camera_button.clicked.connect(self.open_camera_slot)
        self.face_detect_button.clicked.connect(self.face_detect_slot)
        self.trash_detect_button.clicked.connect(self.trash_detect_slot)
        self.trash_recycle_button.clicked.connect(self.trash_recycle_slot)
        self.classify_error_button.clicked.connect(self.select_trash_type_win_slot)
        self.select_trash_type_win.back_to_trash_change_signal.connect(self.back_to_trash_change_win_slot)

    # 槽函数
    def open_camera_slot(self):
        """
        打开摄像头获取视频流数据，QLabel显示
        :return:
        """
        # 初始化
        self.open_camera_button.setEnabled(False)       # 冻结打开摄像头开关
        self.face_detect_button.setEnabled(True)        # 解冻人脸检测按钮
        self.trash_detect_button.setEnabled(True)       # 解冻物品识别按钮
        self.detect_result_flag = False
        self.trash_detect_result.setText("物品类型:")

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)   # 打开摄像头
        self.camera_flag = True                         # 摄像头状态符 True
        while True:
            if self.cap.isOpened():
                if self.camera_flag is False:  # 若摄像头已关闭
                    """
                    此处进行人脸检测or物品检测
                    """
                    break

                status, self.detect_mat = self.cap.read()  # 读取状态，帧

                if status:
                    # 摄像头捕捉帧显示在QLabel中
                    self.predict_mat = self.detect_mat
                    rgb_mat = cv2.cvtColor(self.detect_mat, cv2.COLOR_BGR2RGB)  # 编码转RGB
                    q_image = QImage(rgb_mat.data, rgb_mat.shape[1], rgb_mat.shape[0],  # 转QImage
                                     rgb_mat.shape[1] * 3, QImage.Format_RGB888)

                    self.face_detect_frame.setPixmap(QPixmap.fromImage(q_image).scaled(512, 512))  # 显示在QLabel中
                else:
                    self.predict_mat = None

                cv2.waitKey(10)
        self.cap.release()

        self.detect_mat = None                          # 清空获取的图像数据
        self.open_camera_button.setEnabled(True)        # 解冻打开摄像头开关
        self.face_detect_button.setEnabled(False)       # 冻结人脸检测按钮
        self.trash_detect_button.setEnabled(False)      # 冻结物品识别按钮
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
        ret_dict = self.ai.detect_face(self.detect_mat, access_token)
        if ret_dict["face_num"] == 0:
            QMessageBox.information(self, "登录提示", "未检测到人脸")
        elif ret_dict["face_num"] > 1:
            QMessageBox.information(self, "登录提示", "检测到多张人脸")
        elif ret_dict["face_num"] == 1:
            x, y, width, height = ret_dict["image"]  # 获取人脸位置和大小

            # 画框
            img_mat = self.detect_mat
            cv2.rectangle(img_mat, (x, y), (x + width, y + height), (0, 255, 0), 2)  # 默认打开方式BGR
            rgb_mat = cv2.cvtColor(img_mat, cv2.COLOR_BGR2RGB)                      # 编码转置，BGR转RGB
            q_image = QImage(rgb_mat.data, rgb_mat.shape[1], rgb_mat.shape[0],      # 转QImage
                             rgb_mat.shape[1] * 3, QImage.Format_RGB888)
            self.face_detect_frame.setPixmap(QPixmap.fromImage(q_image).scaled(512, 512))  # 显示在QLabel中
            time.sleep(1)

            # 进行人脸登录
            self.login_judge_slot(img_mat[y:y+height, x:x+width])

    def login_judge_slot(self, face_mat):
        """
        请求百度AI平台进行人脸登录验证
        :param face_mat: 框出的人脸矩阵
        :return:
        """
        print("人脸登录判断----------------------------------------------------------------------------------------")
        # 上传人脸图像至百度AI平台进行人脸比对
        access_token = self.ai.get_access_token("5mGMwYSVemPCN9zLbtZHlQLh",
                                                "HT5ArjvXAfui3tvm2ifSZujQI3D8lGc4")
        user_name = self.ai.face_match(face_mat, "admins,users", access_token)
        print("认证用户为：{}".format(user_name))
        if user_name is not False:
            # 检查当前登录用户是否处于冻结状态
            freeze_flag = self.db.select_op("select userStatus from tbl_userInfo where userName='{}';"
                                            .format(user_name))
            print(freeze_flag[0][0])
            if freeze_flag[0][0] == 0:
                messagebox.showinfo("提示", "{}登录成功".format(user_name))              # 未冻结
                self.login_user_flag = True                                            # 记录当前登录用户状态
                self.login_user_name = user_name
                self.login_user_name_title.setText("用户: " + self.login_user_name)
            elif freeze_flag[0][0] == 1:    # 已冻结
                messagebox.showinfo("提示", "用户已冻结，申请解冻继续后续操作")               # 提示弹窗
        else:
            messagebox.showinfo("提示", "认证失败，人脸规格不符")

        self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))  # 重置图片

    def trash_detect_slot(self):
        """
        使用模型框出物品
        :return:
        """
        # 验证用户是否登录
        if self.login_user_flag is True:
            # 关闭摄像头
            self.camera_flag = False  # 关闭摄像头

            # 检测物品类型
            trash_type = self.ob_model.mat_classify(self.model, self.predict_mat)
            self.detect_result_flag = True
            self.trash_detect_result.setText("物品类型: " + trash_type)
            print("物品类型: " + trash_type)
        elif self.login_user_flag is False:
            messagebox.showinfo("提示", "请优先进行登录")

    def trash_recycle_slot(self):
        """
        物品回收，添加回收记录
        :return:
        """
        print("物品回收记录------------------------------------------------------------------------------------------------")
        # 验证用户是否登录
        if self.login_user_flag is True:
            # 验证是否识别物品
            if self.detect_result_flag is True:
                # 拼接图片保存路径，保存当前物品照片
                record_index = self.db.select_op("select recordId from "
                                                 "tbl_recycleRecordInfo order by recordId DESC limit 1;")
                save_path = "resources/detect_image/{}.jpg".format(record_index[0][0]+1)
                cv2.imwrite(save_path, self.predict_mat)

                # 回收记录表添加回收记录
                userId = self.db.select_op("select userId from tbl_userInfo where userName='{}';"
                                           .format(self.login_user_name))
                classType = self.trash_detect_result.text().split(": ")
                if classType[1] == "电池":
                    classType = 0
                elif classType[1] == "瓶子":
                    classType = 1
                elif classType[1] == "叶子":
                    classType = 2
                elif classType[1] == "袋子":
                    classType = 3
                else:
                    classType = 4
                classIcon = save_path
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
                flag = self.db.insert_op("insert into tbl_recycleRecordInfo(userId,classType,classIcon,createTime) "
                                         "values('{}','{}','{}','{}');"
                                         .format(userId[0][0], classType, classIcon, current_time))
                if flag is not False:
                    self.detect_result_flag = False                 # 初始化
                    self.trash_detect_result.setText("物品类型:")
                    self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))
                    messagebox.showinfo("提示", "物品回收成功")
                else:
                    messagebox.showinfo("提示", "系统繁忙，请稍后重试")
            else:
                messagebox.showinfo("提示", "请先识别物品")
        else:
            messagebox.showinfo("提示", "请先进行登录")

    def error_recycle_slot(self):
        """
        记录错误信息，添加错误信息记录
        :return:
        """
        print("错误信息记录----------------------------------------------------------------------------------------------")
        # 跳转界面选择完物品类型后
        # 验证用户是否登录
        if self.login_user_flag is True:
            # 验证是否识别物品
            if self.detect_result_flag is True:
                # 1.保存物品回收信息
                # 拼接图片保存路径，保存当前物品照片
                record_index = self.db.select_op("select recordId from "
                                                 "tbl_recycleRecordInfo order by recordId DESC limit 1;")
                save_path = "resources/detect_image/{}.jpg".format(record_index[0][0] + 1)
                cv2.imwrite(save_path, self.predict_mat)

                # 回收记录表添加回收记录
                userId = self.db.select_op("select userId from tbl_userInfo where userName='{}';"
                                           .format(self.login_user_name))
                classType = self.select_trash_type
                classIcon = save_path
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间

                recycle_record_flag = self.db.insert_op("insert into "
                                                        "tbl_recycleRecordInfo(userId,classType,classIcon,createTime) "
                                                        "values('{}',{},'{}','{}');"
                                                        .format(userId[0][0], classType, classIcon, current_time))
                # 2.保存错误信息
                errorType = self.trash_detect_result.text().split(": ")
                if errorType[1] == "电池":
                    errorType = 0
                elif errorType[1] == "瓶子":
                    errorType = 1
                elif errorType[1] == "叶子":
                    errorType = 2
                elif errorType[1] == "袋子":
                    errorType = 3
                else:
                    errorType = 4

                error_record_flag = self.db.insert_op("insert into "
                                                      "tbl_errorRecordInfo(errorType,classType,classIcon,createTime) "
                                                      "values({},{},'{}','{}');"
                                                      .format(errorType, classType, classIcon, current_time))

                if recycle_record_flag is not False and error_record_flag is not False:
                    self.detect_result_flag = False                                             # 初始化
                    self.select_trash_type = None                                               # 选择的物品类型
                    self.trash_detect_result.setText("物品类型:")
                    self.face_detect_frame.setPixmap(QPixmap("resources/icon/face_detect.png"))
                    messagebox.showinfo("提示", "物品回收成功，错误信息保存成功")
                else:
                    messagebox.showinfo("提示", "系统繁忙，请稍后重试")
            else:
                messagebox.showinfo("提示", "请先识别物品")
        else:
            messagebox.showinfo("提示", "请先进行登录")

    def select_trash_type_win_slot(self):
        """
        跳转物理类型选择界面
        :return:
        """
        self.select_trash_type_win.show()

    def back_to_trash_change_win_slot(self, select_type):
        """
        返回变废为宝界面
        :param select_type: 选择的物品类型
        :return:
        """
        self.select_trash_type_win.close()      # 关闭物品类型选择界面
        self.select_trash_type = select_type    # 获取选择的物品类型

        self.error_recycle_slot()               # 记录错误信息


if __name__ == "__main__":
    app = QApplication(sys.argv)

    trash_change_win = TrashChangeWin()
    trash_change_win.show()

    sys.exit(app.exec())
