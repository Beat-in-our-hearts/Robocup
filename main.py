"""
作者：陆祖兴
时间：2021/8/29
版本：2.0

阅读指南：
程序分为人脸部分、物品部分、其他功能三个主要库
由于比赛规则的修改，已经将各个版本的函数都放在一起了

目前需要阅读的：
物品库：detec.py
人脸库：Add_face_lib（添加人脸库）、Face_multiSearch_v2（人脸识别、性别识别、人脸对比）
其他功能库：Draw_txt_on_single_face_PIL（批注姓名）；Draw_Box_on_single_face_PIL（人脸、性别框选）；plot_time_on_pic（时间戳）

【注意】main.py必须放置在根目录保证文件路径正确性
"""

import time

from face_api.face_run import Face_BD
from object_api.detect import object_find
from other_api.del_flies import del_file
import os
# 获取上级目录
root_path = os.path.dirname(__file__)

# ----------------全局变量-----------------------
Face_lib_path = root_path + "/files_dir/face_lib"  # 已知的人脸库，人名与图片名称一致
temp_path = root_path + "/files_dir/temp_path"  # 临时文件夹:人脸识别的图片路径/物品识别的保存路径
pt_path = root_path + "/object_api/pt/best_xz.pt"  # 物品识别的pt保存路径
Pic_path = root_path + "/files_dir/pic_path"  # 物品识别的图片路径
Result_path = root_path + "/files_dir/result"  # 人脸识别的保存路径

if __name__ == "__main__":
    # ---------------物品识别---------------
    object_find(Pic_path, temp_path, pt_path)

    # ---------------人脸识别---------------
    time.sleep(1)
    face_baidu = Face_BD()  # 调用百度API
    face_baidu.Add_face_lib(Face_lib_path)  # 添加人脸库
    time.sleep(1)  # 服务器有响应时间，避免冲突需要延时处理
    face_baidu.Face_multiSearch_v2(f"{temp_path}/exp", Result_path)  # 框选目标人脸，并保存
    time.sleep(1)  # 服务器有响应时间，避免冲突需要延时处理

    # --------------删除临时文件--------------
    face_baidu.Clear()
    del_file(temp_path)
