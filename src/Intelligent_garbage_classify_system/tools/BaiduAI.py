# -*- coding: utf-8 -*-
# Project : Intelligent_garbage_classify_system
# Name : BaiduAI.py
# Author : hhs
# DATE : 2023/9/12 21:37

import cv2
import requests
import base64
import json


class BaiduAI:
    """
    百度AI开放平台操作类
    """
    def __init__(self):
        pass

    def get_access_token(self, api_key, secret_key):
        """
        从百度AI平台获取access_token
        :param api_key: 官网获取AK
        :param secret_key: 官网获取SK
        :return: access_token
        """
        print("获取at------------------------------------------------------------------------------------------------")
        host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}" \
            .format(api_key, secret_key)

        response = requests.get(host)
        if response:
            print("access_token = " + response.json()["access_token"])
            return response.json()["access_token"]
        else:
            print("get access token error")

    def detect_face(self, image_mat, access_token):
        """
        人脸检测与属性分析
        :param image_mat:  人脸图像矩阵
        :param access_token: 从百度AI平台获取的access_token
        :return:
        """
        print("人脸检测------------------------------------------------------------------------------------------------")
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        request_url = request_url + "?access_token=" + access_token  # 请求百度AI服务的路径

        # 获取当前摄像头人脸图片
        # 矩阵转换为utf8
        image = cv2.imencode('.jpg', image_mat)[1]
        img_encode = str(base64.b64encode(image))[2:-1]

        # 发给百度AI平台的数据体&数据头
        params = {"image": img_encode, "image_type": "BASE64"}
        params = json.dumps(params)                                 # 发给百度AI平台的数据体，dict变json字符串
        headers = {'content-type': 'application/json'}

        # 来自百度AI服务器的反馈
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            if response.json().get("result", ""):
                print("face_num = ", response.json()["result"]["face_num"]),
                print("x = ", response.json().get("result", "")["face_list"][0]["location"]["left"]),
                print("y = ", response.json().get("result", "")["face_list"][0]["location"]["top"]),
                print("width = ", response.json().get("result", "")["face_list"][0]["location"]["width"]),
                print("height = ", response.json().get("result", "")["face_list"][0]["location"]["height"])

                # 返回人脸位置
                if response.json()["result"]['face_num'] == 1:
                    result = response.json()["result"]
                    return {
                        "image": (
                            int(response.json().get("result", "")["face_list"][0]["location"]["left"]),
                            int(response.json().get("result", "")["face_list"][0]["location"]["top"]),
                            int(response.json().get("result", "")["face_list"][0]["location"]["width"]),
                            int(response.json().get("result", "")["face_list"][0]["location"]["height"])
                        ),
                        "face_num": 1
                    }
                elif response.json()["result"]["face_num"] == 0:  # 未检测到人脸
                    return {"image": (), "face_num": 0}
                elif response.json()["result"]["face_num"] > 1:  # 检测到多张脸
                    return {"image": (), "face_num": 0}
            else:  # 结果异常
                return {"image": (), "face_num": -1}

    def face_match(self, image_mat, group, access_token):
        """
        与人脸库的人脸进行比对
        :param image_mat:  人脸图片矩阵
        :param group: 人脸用户组，管理员or用户：admins，users
        :param access_token: 从百度AI平台获取的access_token
        :return:登录成功or失败    True or False；登录成功返回登录用户名
        """
        print("人脸比对------------------------------------------------------------------------------------------------")
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        request_url = request_url + "?access_token=" + access_token  # 请求百度AI服务的路径

        # 获取框内人脸
        image = cv2.imencode('.jpg', image_mat)[1]
        img_encode = str(base64.b64encode(image))[2:-1]

        # 发给百度AI平台的数据体&数据头
        params = {"image": img_encode, "image_type": "BASE64", "group_id_list": "{}".format(group)}
        params = json.dumps(params)  # 发给百度AI平台的数据体，dict变json字符串
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            if response.json()["error_code"] == 0:
                print("face_score: {}".format(response.json()["result"]["user_list"][0]["score"]))

                # 若用户相似度阈值高于80，说明为对应用户
                if response.json()["result"]["user_list"][0]["score"] > 80:
                    print("{} match success".format(response.json()["result"]["user_list"][0]["user_id"]))
                    return response.json()["result"]["user_list"][0]["user_id"]
                else:
                    return False
            else:
                return False

    def face_regist(self, image_mat, group, user_name, access_token):
        """
        人脸库注册
        :param image_mat: 人脸图片矩阵
        :param group: 要加入的用户组：管理员or用户：admins，users
        :param user_name: 管理员用户名
        :param access_token: 从百度AI平台获取的access_token
        :return: 人脸库注册成功与否：True or False
        """
        print("人脸上传------------------------------------------------------------------------------------------------")
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
        request_url = request_url + "?access_token=" + access_token  # 请求百度AI服务的路径

        # 获取框内人脸
        image = cv2.imencode('.jpg', image_mat)[1]
        img_encode = str(base64.b64encode(image))[2:-1]

        # 发给百度AI平台的数据体&数据头
        params = {"image": img_encode, "image_type": "BASE64",
                  "group_id": "{}".format(group), "user_id": "{}".format(user_name)}
        params = json.dumps(params)  # 发给百度AI平台的数据体，dict变json字符串
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            if response.json()["error_msg"] == "SUCCESS":
                print("{} regist success".format(user_name))
                return True
            else:
                return False

