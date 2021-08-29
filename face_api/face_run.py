"""
    百度人脸库，单独把人脸部分拿出来了
    更新如下：   1.优化了图像标注部分，可以选择cv2或者PIL标注
               2.按照比赛规则进行了一些修改，把标注的年龄信息删除了
               3.把全局变量单独放置在main,py中，优化了结构
    作者：陆祖兴
    日期：2021/8/21
    版本：v2
"""
import os
import cv2
import time
import base64
from aip import AipFace
from other_api.plot_lable import Draw_Box_on_faces_cv2,Draw_Box_on_faces_PIL,plot_time_on_pic
from PIL import Image, ImageDraw, ImageFont

class Face_BD:
    """
    robocup封装百度人脸库
    Add_face_lib：用于添加人脸库到云端
    find_all_faces，face_lib_find：用于识别图片的人脸特征信息
    Face_multiSearch：用于识别图片集中对应人脸库的人脸，标识并保存
    """

    def __init__(self):
        self.APP_ID = '24724684'
        self.API_KEY = '1Gw70VWpThVjsfwc8myFBuA5'
        self.SECRET_KEY = 'pdbxFfZ94LzQD988L4TzGuY8iy0uqFkc'
        self.client = AipFace(self.APP_ID, self.API_KEY, self.SECRET_KEY)#初始化连接百度API

    def find_all_faces(self, image_path, wanted_info='gender', max_face_num=10, options=None):
        """
        调用了封装过的百度API，识别图片的人脸信息
        :param image_path: 图片路径，支持绝对路径和相对路径
        :param wanted_info 想要获取的信息
        :param max_face_num: 默认10，全部人脸图识别
        :param options: 可选参数
        :return: 百度API的结果
        """
        with open(image_path, 'rb') as f:
            image = (base64.b64encode(f.read())).decode("utf-8")#base64格式打开图片
        imageType = "BASE64"
        # 如果无可选参数，默认只需要性别
        if options == None:
            options = {"face_field": f"{wanted_info}", "max_face_num": max_face_num}
        f.close()
        return self.client.detect(image, imageType, options)['result']

    def face_lib_find(self, image, wanted_info='age,gender', max_face_num=1, options=None):
        """
        调用了封装过的百度API，识别图片的人脸信息，和前面的有一点点区别，不用反复打开文件，在创建人脸库的时候调用
        :param image: base64格式化后的图片数据
        :param wanted_info 想要获取的信息
        :param max_face_num: 默认1，单个人脸图识别
        :param options: 可选参数
        :return: 百度API的结果
        """
        # print(image)
        imageType = "BASE64"
        # 如果无可选参数，默认只需要年龄和性别
        if options == None:
            options = {"face_field": f"{wanted_info}", "max_face_num": max_face_num}
        return self.client.detect(image, imageType, options)['result']

    def Add_face_lib(self, faces_lib_path, groupId="robocup"):
        """
        用于添加人脸库
        :param groupId: 百度API中人脸库的组别信息
        :return:
        """
        # 获取需要添加的人脸库的文件路径等
        dirs = os.listdir(faces_lib_path)
        print(f"Find {len(dirs)} files in {faces_lib_path}:{dirs}\nFace Lib Creating...")
        for file in dirs:
            with open(f'{faces_lib_path}/{file}', 'rb') as f:
                image = (base64.b64encode(f.read())).decode("utf-8")
            info_result = self.face_lib_find(image)#获取单个人脸图的信息
            # print(info_result)
            age = info_result['face_list'][0]["age"] # 更新内容
            gender = info_result['face_list'][0]["gender"]['type']
            file_name = os.path.splitext(file)[0]
            userId = file_name
            """ 如果有可选参数 """
            # user_info是人脸识别后需要打印的信息
            options = {"user_info": f"gender:{gender};name:{file_name}", "quality_control": "NORMAL"}
            """ 带参数调用人脸注册 """
            self.client.addUser(image, "BASE64", groupId, userId, options)
            f.close()
        print("All faces already added into face_lib!\n")

    def Face_multiSearch(self, pic_path, result_path, cv2_or_PIL="PIL", groupIdList="robocup"):
        """
        在一张图片中识别多个包含在人脸库中的人脸，并保存
        :param pic_path: 待测图片路径
        :param result_path: 保存路径
        :param cv2_or_PIL:'cv2'表示使用opencv；'PIL'表示使用PIL；两者都是画图
        :param groupIdList: 云端人脸库的组别
        :return:
        """
        # 待测图片的存储路径
        dirs = os.listdir(pic_path)
        print(f"Find {len(dirs)} files in {pic_path}:{dirs}\nFinding...")
        # 遍历待测图片
        for file in dirs:
            with open(f'{pic_path}/{file}', 'rb') as f:
                image = (base64.b64encode(f.read())).decode("utf-8")
            """ 如果有可选参数 """
            options = {"max_face_num": 10, "match_threshold": 70, "quality_control": "LOW", "max_user_num": 3}

            """ 带参数调用人脸搜索 M:N 识别 """
            result = self.client.multiSearch(image, "BASE64", groupIdList, options)
            if 'result' in result:
                result = result['result']
            else:
                result = None
            f.close()
            filename = f"{result_path}/{time.time()}.png"

            # 图片标注方式
            if cv2_or_PIL == 'cv2':
                img = cv2.imread(f'{pic_path}/{file}')
                if result != None:
                    Draw_Box_on_faces_cv2(img, result["face_list"], 0)
                cv2.imwrite(filename, img)
            elif cv2_or_PIL == 'PIL':
                im = Image.open(f'{pic_path}/{file}')
                plot_time_on_pic(im)
                if result != None:
                    Draw_Box_on_faces_PIL(im,result["face_list"],0)
                im.save(filename)
            print(f"{filename}:The save was successful!")
        print("Face recognition ends...\n")

    def Clear(self, groupId="robocup"):
        """
        删除这个库，防止对另一个测试数据产生干扰
        :param groupId: 组别ID
        :return:
        """
        self.client.groupDelete(groupId)
