from aip import AipFace
import base64
import cv2

RED_color = (0, 0, 255)
BLUE_color = (255, 0, 0)
GREEN_color = (0, 255, 0)

def Draw_Box_on_faces(image, face_list, show_mode=0):
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
        # # cv2.putText(image, f"age:{face['age']};gender:{face['gender']['type']}",
        #             (location[0], location[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, RED_color, thickness=1)
    if show_mode != 0:
        cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('input_image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

""" 你的 APPID AK SK """
APP_ID = '24724684'
API_KEY = '1Gw70VWpThVjsfwc8myFBuA5'
SECRET_KEY = 'pdbxFfZ94LzQD988L4TzGuY8iy0uqFkc'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

# with open("../example/example4.jpeg", 'rb') as f:
#     image = (base64.b64encode(f.read())).decode("utf-8")
#
# imageType = "BASE64"
#
# groupId = "group1"
#
# userId = "user1"
#
# """ 调用人脸注册 """
# print(client.addUser(image, imageType, groupId, userId))

with open("../example/example5.jpeg", 'rb') as f:
    image = (base64.b64encode(f.read())).decode("utf-8")

imageType = "BASE64"

groupIdList = "group1"

# """ 调用人脸搜索 M:N 识别 """
# client.multiSearch(image, imageType, groupIdList)

""" 如果有可选参数 """
options = {"max_face_num": 10, "match_threshold": 70,"quality_control":"LOW"}


""" 带参数调用人脸搜索 M:N 识别 """
result = client.multiSearch(image, imageType, groupIdList, options)['result']

for i in result["face_list"]:
    print(i)

img = cv2.imread("../example/example5.jpeg")
Draw_Box_on_faces(img, result["face_list"], 1)

# with open("../example/example3.jpeg", 'rb') as f:
#     image = (base64.b64encode(f.read())).decode("utf-8")
#
# imageType = "BASE64"
#
# groupIdList = "group1"
#
# """ 如果有可选参数 """
# options = {"max_face_num": 10, "match_threshold": 30, "user_id": "user1"}
# # options["quality_control"] = "NORMAL"
# # options["liveness_control"] = "LOW"
# # options["user_id"] = "233451"
# # options["max_user_num"] = 3
#
#
# """ 带参数调用人脸搜索 """
# print(client.search(image, imageType, groupIdList, options))
