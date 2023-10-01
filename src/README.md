# Intelligent_garbage_classify_system
四阶段实战项目-智能垃圾分类系统源码：项目代码**只提供思路**，**仅供参考**

## 未上传训练模型
- 1.网盘获取识别模型：https://pan.baidu.com/s/1OA8zKkpmmRUAFDyrsil2hQ?pwd=g2tx  提取码：g2tx
- 2.导入源码根目录 **./recources/model/** 中

## Ubuntu导入数据库 
- 1.进入MySQL
  ```
  mysql -u root -p
  # root为mysql账号，之后输入自己的root密码
  ```
- 2.新建数据库
  ```
  create database IGCS_DB;
  ```
- 3.导入.sql文件
  ```
  use IGCS_DB;
  source IGCS_DB.sql文件路径;
  ```

## 设置config.ini
- 修改 **./resources/config.ini** 配置文件下的**host**，改为要连接虚拟机Ubuntu16.04的IP地址
- ![image](https://github.com/NightBonsai/Intelligent_garbage_classify_system/assets/107353989/89af9018-cbf4-43e0-ae6c-fa27c407808d)

## 使用PyCharm2019.2.3打开源码文件，运行 **main.py**脚本即可运行应用
