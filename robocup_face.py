"""
    robocup 百度人脸识别
    作者：陆祖兴
    日期：2021/8/20
    版本：v1.0
"""
import base64
import cv2
import requests
import time
from aip import AipFace
from PIL import Image, ImageDraw, ImageFont
import os

# ----------------全局变量-----------------------
RED_color = (0, 0, 255)
BLUE_color = (255, 0, 0)
GREEN_color = (0, 255, 0)

Face_lib_path = "files_dir/face_lib"  # 已知的人脸库，人名与图片名称一致
Pic_path = "files_dir/pic_path"  # 待测图片路径
Result_path = "files_dir/result"  # 保存路径


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
        self.client = AipFace(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def find_all_faces(self, image_path, wanted_info='age,gender', max_face_num=10, options=None):
        """
        调用了封装过的百度API，识别图片的人脸信息
        :param image_path: 图片路径，支持绝对路径和相对路径
        :param wanted_info 想要获取的信息
        :param max_face_num: 默认10，全部人脸图识别
        :param options: 可选参数
        :return: 百度API的结果
        """
        with open(image_path, 'rb') as f:
            image = (base64.b64encode(f.read())).decode("utf-8")
        imageType = "BASE64"
        # 如果无可选参数，默认只需要年龄和性别
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
            info_result = self.face_lib_find(image)
            # print(info_result)
            age = info_result['face_list'][0]["age"]
            gender = info_result['face_list'][0]["gender"]['type']
            file_name = os.path.splitext(file)[0]
            userId = file_name
            """ 如果有可选参数 """
            # user_info是人脸识别后需要打印的信息
            options = {"user_info": f"gender:{gender};age:{age};name:{file_name}", "quality_control": "NORMAL"}
            """ 带参数调用人脸注册 """
            self.client.addUser(image, "BASE64", groupId, userId, options)
            f.close()
        print("All faces already added into face_lib!\n\n")

    def Face_multiSearch(self, pic_path, result_path, cv2_or_PIL="cv2", groupIdList="robocup"):
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
            result = self.client.multiSearch(image, "BASE64", groupIdList, options)['result']
            f.close()
            filename = f"{result_path}/{time.time()}.png"
            if cv2_or_PIL == 'cv2':
                img = cv2.imread(f'{pic_path}/{file}')
                Draw_Box_on_faces_auto(img, result["face_list"], 0)
                cv2.imwrite(filename, img)
            elif cv2_or_PIL == 'PIL':
                im = Image.open(f'{pic_path}/{file}')

            print(f"{filename}:The save was successful!")
        print("Face recognition ends...\n\n")

    def Clear(self, groupId="robocup"):
        """
        删除这个库，防止对另一个测试数据产生干扰
        :param groupId: 组别ID
        :return:
        """
        self.client.groupDelete(groupId)


def Get_Access_Token(client_id="1Gw70VWpThVjsfwc8myFBuA5", client_secret="pdbxFfZ94LzQD988L4TzGuY8iy0uqFkc", mode=0):
    """
    本函数用于获取Access_Token，可以理解为验证码，验证码有效期为30天，需要定期调用本函数获取
    :param client_id: 官网获取的AK
    :param client_secret: 为官网获取的SK
    :param mode:0:默认参数，1:access_token
    :return:
    """
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    response = requests.get(host)
    if response and mode != 0:
        print(response.json()["access_token"])
    else:
        print(response.json())


def Get_Face_Result(image_path, mode=0,
                    wanted_info="age,expression,gender",
                    access_token='24.c4bc8bad00b07a661e661f697ad20cb7.2592000.1631961695.282335-24724684'):
    """
    用于返回获取图片的信息
    :param image_path: 图片路径，支持绝对路径和相对路径
    :param mode: 0：默认参数；1：需要的结果
    :param wanted_info: 想要获取的信息
    :param access_token: 百度API的Access_Token（验证码）
    :return:
    """
    with open(image_path, 'rb') as f:
        base64_data = (base64.b64encode(f.read())).decode("utf-8")
    request_url = f"https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={access_token}"
    if mode != 0:
        params = {"image": base64_data, "image_type": "BASE64", "face_field": wanted_info, "max_face_num": 10}
    else:
        params = {"image": base64_data, "image_type": "BASE64", "max_face_num": 10}
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    # print(response.json()["result"])
    return response.json()["result"]


def Draw_Box_on_faces(image, face_list, text_info_list, show_mode=0):
    """
    调用cv2.rectangle，cv2.putText给图片做标注信息
    :param image: cv2 图片类型
    :param face_list: 百度API调用结果中人脸识别信息
    :param show_mode: 0：不显示；1：显示图片
    :return:
    """
    for face in face_list:
        location = [int(face['location']['left']), int(face['location']['top']),
                    int(face['location']['left']) + int(face['location']['width']),
                    int(face['location']['top'] + face['location']['height'])]
        cv2.rectangle(image, (location[0], location[1]), (location[2], location[3]), RED_color, thickness=3)
        cv2.putText(image, text_info_list, (location[0], location[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, RED_color,
                    thickness=1)
    if show_mode != 0:
        cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('input_image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def Draw_Box_on_faces_auto(image, face_list, show_mode=0):
    """
    调用cv2.rectangle，cv2.putText给图片做标注信息
    :param image: cv2 图片类型
    :param face_list: 百度API调用结果中人脸识别信息
    :param show_mode: 0：不显示；1：显示图片
    :return:
    """
    for face in face_list:
        if len(face['user_list']) != 0:
            location = [int(face['location']['left']), int(face['location']['top']),
                        int(face['location']['left']) + int(face['location']['width']),
                        int(face['location']['top'] + face['location']['height'])]
            cv2.rectangle(image, (location[0], location[1]), (location[2], location[3]), RED_color, thickness=3)
            # print(face['user_list'][0]['user_info'])
            cv2.putText(image, face['user_list'][0]['user_info'], (location[0], location[1] - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1, RED_color, thickness=1)
    if show_mode != 0:
        cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('input_image', image)
        cv2.waitKey(0)
        # time.sleep(10000)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    """
    人脸识别步骤：识别人脸库中所有人脸；多对多识别；框选识别部分
    """
    face_baidu = Face_BD()  # 调用百度API
    face_baidu.Add_face_lib(Face_lib_path)  # 添加人脸库
    time.sleep(1)  # 服务器有响应时间，避免冲突需要延时处理
    face_baidu.Face_multiSearch(Pic_path, Result_path)  # 框选目标人脸，并保存
    time.sleep(1)  # 服务器有响应时间，避免冲突需要延时处理
    face_baidu.Clear()
