import time

from face_api.face_run import Face_BD
from object_api.detect import object_find
from other_api.del_flies import del_file

# ----------------全局变量-----------------------
Face_lib_path = "files_dir/face_lib"    # 已知的人脸库，人名与图片名称一致
temp_path = "files_dir/temp_path"       # 临时文件夹:人脸识别的图片路径/物品识别的保存路径
pt_path = "object_api/last.pt"          # 物品识别的pt保存路径
Pic_path = "files_dir/pic_path"         # 物品识别的图片路径
Result_path = "files_dir/result"        # 人脸识别的保存路径

if __name__ == "__main__":

    # ---------------物品识别---------------
    object_find(Pic_path, temp_path, pt_path)

    # ---------------人脸识别---------------
    time.sleep(1)
    face_baidu = Face_BD()  # 调用百度API
    face_baidu.Add_face_lib(Face_lib_path)  # 添加人脸库
    time.sleep(1)  # 服务器有响应时间，避免冲突需要延时处理
    face_baidu.Face_multiSearch(f"{temp_path}/exp", Result_path)  # 框选目标人脸，并保存
    time.sleep(1)  # 服务器有响应时间，避免冲突需要延时处理

    # --------------删除临时文件--------------
    face_baidu.Clear()
    del_file(temp_path)
