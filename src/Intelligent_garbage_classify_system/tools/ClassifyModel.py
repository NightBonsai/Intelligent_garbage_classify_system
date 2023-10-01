# -*- coding: utf-8 -*-
# Project : step4project09
# Name : ClassifyModel.py
# Author : lyh
# DATE : 2023/9/13 17:01

import os
# 1、错误+警告 2、只显示错误 3、都不显示
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from warnings import simplefilter
simplefilter("ignore", FutureWarning)  # 忽略警告FutureWarning

import numpy as np
import pandas as pd
import tensorflow.compat.v1 as tf
from tflearn.layers.conv import conv_2d, max_pool_2d            # 卷积、池化
from tflearn.layers.core import input_data, fully_connected, dropout    # 输入数据、全连、舍去部分功能
from tflearn.layers.estimator import regression
import tflearn
import cv2
from tqdm import tqdm           # 进度条
from random import shuffle      # 随机打乱

IMG_SIZE = 256                                                # 图片大小


class ClassifyModel():
    """
    CNN卷积神经网络训练测试类
    """
    def create_net(self):
        """
        创建模型，网络搭建
        :return: 模型网络
        """
        print("搭建CNN卷积神经网络----------------------------------------------------------------------------------------")
        # # 搭建网络 卷积 激活 池化 全连
        # # 1、输入层                     任意行    256 * 256       深度-灰度-1
        # conv_input = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name="input")
        #
        # # 2、第一层卷积神经网络
        # #               输入数据  输出高度 卷积核大小  激活函数
        # conv1 = conv_2d(conv_input, 16, 5, activation='relu')
        # conv1 = max_pool_2d(conv1, 2)
        # # 3、第二层神经网络
        # conv2 = conv_2d(conv1, 16, 5, activation='relu')
        # conv2 = max_pool_2d(conv2, 2)
        # # 4、第三层神经网络
        # conv3 = conv_2d(conv2, 32, 5, activation='relu')
        # conv3 = max_pool_2d(conv3, 2)
        # # 4、第四层神经网络
        # conv4 = conv_2d(conv3, 32, 5, activation='relu')
        # conv4 = max_pool_2d(conv4, 2)
        # # 4、第五层神经网络
        # conv5 = conv_2d(conv4, 64, 5, activation='relu')
        # conv5 = max_pool_2d(conv5, 2)
        # # 4、第六层神经网络
        # conv6 = conv_2d(conv5, 64, 5, activation='relu')
        # conv6 = max_pool_2d(conv6, 2)
        # # 4、第七层神经网络
        # conv7 = conv_2d(conv6, 128, 5, activation='relu')
        # conv7 = max_pool_2d(conv7, 2)
        # # 4、第八层神经网络
        # conv8 = conv_2d(conv7, 128, 5, activation='relu')
        # conv8 = max_pool_2d(conv8, 2)
        # # 4、第九层神经网络
        # conv9 = conv_2d(conv8, 1024, 5, activation='relu')
        # conv9 = max_pool_2d(conv9, 2)
        #
        # # 5、全连层
        # fully_connect1 = fully_connected(conv9, 1024, activation='relu')
        # # 防止过拟合，提高泛化能力，防止太过依赖网络神经节点，而忽视本身的特征
        # fully_connect1 = dropout(fully_connect1, 0.7)       # 舍去部分的特征
        # # 过拟合：在训练集特征选取较好，模型准确率较高，但是一旦出现不在训练集中的数据，准确率大幅降低
        #
        # # 6、分类器   分为4类
        # fully_connect2 = fully_connected(fully_connect1, 4, activation='softmax')
        #
        # lr = 1e-4       # learning rate  学习率learning_rate
        # # 7、综合损失函数+优化器
        # model_net = regression(fully_connect2, optimizer='adam',
        #                loss='categorical_crossentropy', learning_rate=lr, name='model_net')
        #
        # # 8、创建模型
        # model = tflearn.DNN(model_net, tensorboard_dir="log")
        # # 1-8创建模型、用于训练or预测
        # return model

        # 网络搭建
        # 1.输入层 任意行         50 *50      深度-灰度-1
        conv_input = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name="input")
        conv1 = conv_2d(conv_input, 64, 7, activation='relu')
        conv1 = max_pool_2d(conv1, 5)
        # 2 第二层神经网络
        conv2 = conv_2d(conv1, 128, 7, activation='relu')
        conv2 = max_pool_2d(conv2, 5)
        # 3 第三层神经网络
        conv3 = conv_2d(conv2, 256, 7, activation='relu')
        conv3 = max_pool_2d(conv3, 5)
        # 第四次神经网络
        conv4 = conv_2d(conv3, 512, 7, activation='relu')
        conv4 = max_pool_2d(conv4, 5)
        # 第五次神经网络
        conv5 = conv_2d(conv4, 1024, 7, activation='relu')
        conv5 = max_pool_2d(conv5, 5)

        conv6 = conv_2d(conv5, 1024, 7, activation='relu')
        conv6 = max_pool_2d(conv6, 5)

        # 4全连层
        # # 防止过拟合，提高泛化能力
        fc1 = fully_connected(conv6, 1024, activation='relu')
        fc1 = dropout(fc1, 0.5)

        fc2 = fully_connected(fc1, 4, activation='softmax')
        lr = 1e-4

        model_net = regression(fc2, optimizer='adam',
                               loss='categorical_crossentropy',
                               learning_rate=lr,
                               name='model_net')
        model = tflearn.DNN(model_net, tensorboard_dir="log")
        return model

    def model_train(self, npy_path, model_path):
        """
        依据数据集进行模型训练
        :param npy_path:   数据集路径
        :param model_path: 模型保存路径
        :return:
        """
        print("模型训练----------------------------------------------------------------------------------------")
        model = self.create_net()     # 创建网络模型

        # 1、加载数据
        data = np.load(npy_path, allow_pickle=True)
        # print(len(data), type(data), data[0])

        # 2、数据分割   训练集   测试集
        train_data = data[:-30]     # 训练集
        test_data = data[-30:]      # 测试集

        # [None IMG_SIZE, IMG_SIZE, 1]
        x_train = np.array([i[0] for i in train_data]).reshape((-1, IMG_SIZE, IMG_SIZE, 1))
        y_train = [i[1] for i in train_data]
        x_test = np.array([i[0] for i in test_data]).reshape((-1, IMG_SIZE, IMG_SIZE, 1))
        y_test = [i[1] for i in test_data]

        # 3.模型训练  生成模型的时候运行  预测的时候不再运行
        model.fit({'input': x_train},
                  {'model_net': y_train},
                  n_epoch=3,                                                    # 训练轮数
                  validation_set=({'input': x_test}, {'model_net': y_test}),
                  snapshot_step=10,                                             # 训练10次打印一次
                  show_metric=True,                                             # 保存日志
                  run_id='model_class')
        # 4.模型保存
        model.save(model_path)

    def label_img(self, img_name):
        """
        根据图片名获取标签，猫狗共两类：电池:[1,0,0,0];瓶子:[0,1,0,0];叶子:[0,0,1,0];塑料袋:[0,0,0,1]
        :param img_name: 图片路径
        :return: 当前图片标签
        """
        label_name = img_name.split('.')[0]  # bag.序号.png
        # print(label_name)
        if label_name == 'power':
            return [1, 0, 0, 0]
        elif label_name == 'bottle':
            return [0, 1, 0, 0]
        elif label_name == "leave":
            return [0, 0, 1, 0]
        elif label_name == "bag":
            return [0, 0, 0, 1]
        return []

    def create_train_data(self, dir_path, npy_path):
        """
        创建数据集
        :param dir_path:  整个图片的文件夹目录
        :param npy_path:  数据集保存路径
        :return:
        """
        print("创建数据集----------------------------------------------------------------------------------------")
        training_data = []
        for img_path in tqdm(os.listdir(dir_path)):
            # print(img_path)
            label = self.label_img(img_path)
            if len(label) != 0:
                img_path = os.path.join(dir_path, img_path)                         # 对图片路径进行拼接
                img_mat = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)                # 变成单通道--灰度
                # print(img_mat.shape)
                if img_mat is not None:
                    img = cv2.resize(img_mat, (IMG_SIZE, IMG_SIZE))                 # 更改大小
                    training_data.append([np.array(img), np.array(label)])
        shuffle(training_data)
        np.save(npy_path, training_data)

    def preprocess_mat(self, mat):
        """
        对摄像头获取的一帧画面进行预处理
        :param mat: 图像矩阵 ndarray
        :return:
        """
        resized_mat = cv2.resize(mat, (IMG_SIZE, IMG_SIZE))             # 图像大小转置
        gray_mat = cv2.cvtColor(resized_mat, cv2.COLOR_BGR2GRAY)        # 转置灰度图
        normalized_mat = gray_mat / 255.0                               # 图像归一化处理
        normalized_mat2= normalized_mat.reshape(IMG_SIZE, IMG_SIZE, 1)  # 0维添加一个额外的维度，适应模型输入，改变通道数为1
        processed_mat = np.expand_dims(normalized_mat2, axis=0)
        print(type(processed_mat), processed_mat.shape)

        return processed_mat

    def mat_classify(self, model_path, mat):
        """
        对摄像头获取的一帧数据进行预测
        :param mat: 摄像头获取图片矩阵
        :return:
        """
        print("对摄像头获取的一帧数据进行预测----------------------------------------------------------------------------------------")
        # 图像预处理
        processed_frame = self.preprocess_mat(mat)

        # 预测图像
        y_predict = model_path.predict(processed_frame)
        print(y_predict)
        trash = None  # 垃圾
        index = np.argmax(y_predict)
        print(index)
        if index == 0:  # 测试集30张图片  打印结果有30个
            trash = "电池"
        elif index == 1:
            trash = "瓶子"
        elif index == 2:
            trash = "叶子"
        elif index == 3:
            trash = "袋子"
        else:
            trash = "null"
        return trash

    def create_test_pic(self, pic_path):
        """
        预测一张图片，针对本地图片
        :param pic_path: 图片路径
        :return:
        """
        training_data = []
        img = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), 0)
        print(img.shape, type(img))
        if img is not None:
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            print(img.shape, type(img))
            training_data.append([np.array(img)])
        return np.array(training_data).reshape((-1, IMG_SIZE, IMG_SIZE, 1))

    def get_classify(self, model_path, pic_path):
        """
        对垃圾进行预测分类，针对本地图片
        :param model_path: 模型路径
        :param pic_path:  要预测的图片路径
        :return:
        """
        # model = self.create_net()    # 创建模型
        # # 加载模型
        # model.load(model_file)
        # 预测
        # y_predict = model.predict(create_test_data("./test"))   # 一个文件夹
        y_predict = model_path.predict(self.create_test_pic(pic_path))   # 一张图片
        # print(y_predict)
        trash = None  # 垃圾
        index = np.argmax(y_predict)
        if index == 0:  # 测试集30张图片  打印结果有30个
            trash = "袋子"
        elif index == 1:
            trash = "瓶子"
        elif index == 2:
            trash = "叶子"
        elif index == 3:
            trash = "电池"
        else:
            trash = "没检测出来"
        return trash


if __name__ == "__main__":
    pic_path0 = "../resources/model/test/bag.1.png"
    pic_path1 = "../resources/model/test/bottle.1.png"
    pic_path2 = "../resources/model/test/leave.3862.png"
    pic_path3 = "../resources/model/test/power.1.png"
    # model_file = "../resources/model/trash_classify.model"
    model_file = "../resources/model/dst.model"

    # 训练
    # ob_model = ClassifyModel()                               # 创建模型对象
    # ob_model.create_train_data("../resources/model/image", "../resources/model/trash_TrainData.npy")          # 生成训练集
    # ob_model.model_train("../resources/model/trash_TrainData.npy", "../resources/model/trash_classify.model")   # 模型训练

    # 预测
    ob_model = ClassifyModel()                          # 创建模型对象
    model = ob_model.create_net()                       # 创建模型
    model.load(model_file)                              # 加载模型

    trash0 = ob_model.get_classify(model, pic_path0)
    trash1 = ob_model.get_classify(model, pic_path1)
    # trash2 = ob_model.get_classify(model, pic_path2)
    trash3 = ob_model.get_classify(model, pic_path3)
    print(trash0, type(trash0))
    print(trash1, type(trash1))
    # print(trash2, type(trash2))
    print(trash3, type(trash3))

# 1、搭建网络
# 2、创建模型
# 3、数据分割
# 4、模型训练
# 5、保存模型
# 6、加载模型
# 7、预测
