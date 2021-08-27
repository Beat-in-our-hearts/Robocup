from aip import AipFace
import base64
import cv2
import os

RED_color = (0, 0, 255)
BLUE_color = (255, 0, 0)
GREEN_color = (0, 255, 0)


""" 你的 APPID AK SK """
APP_ID = '24724684'
API_KEY = '1Gw70VWpThVjsfwc8myFBuA5'
SECRET_KEY = 'pdbxFfZ94LzQD988L4TzGuY8iy0uqFkc'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

path = "../files_dir/face_lib/Melania.jpg"
find_path = "../example/example3.jpeg"
with open(path, 'rb') as f:
    image = (base64.b64encode(f.read())).decode("utf-8")

imageType = "BASE64"
name = "Trump"
""" 如果有可选参数 """
options = {"face_field": "age,gender"}

""" 带参数调用人脸检测 """
result = client.detect(image, imageType, options)
age = result['result']['face_list'][0]["age"]
gender = result['result']['face_list'][0]["gender"]['type']
print(result['result']['face_list'][0]["age"])
print(result['result']['face_list'][0]["gender"]['type'])

groupId = "group1"

userId = "user2"

""" 如果有可选参数 """
options.clear()
options = {"user_info": f"gender:{gender};age:{age};name:{name}", "quality_control": "NORMAL"}

""" 带参数调用人脸注册 """
print(client.addUser(image, imageType, groupId, userId, options))


with open(find_path, 'rb') as f:
    image = (base64.b64encode(f.read())).decode("utf-8")

imageType = "BASE64"

groupIdList = "group1"

""" 如果有可选参数 """
options = {"max_face_num": 10, "match_threshold": 70, "quality_control": "LOW", "max_user_num": 3}

""" 带参数调用人脸搜索 M:N 识别 """
result = client.multiSearch(image, imageType, groupIdList, options)['result']

for i in result["face_list"]:
    print(i)


img = cv2.imread(find_path)
for face in result["face_list"]:
    if face['user_list']!=None:
        location = [int(face['location']['left']), int(face['location']['top']),
                    int(face['location']['left']) + int(face['location']['width']),
                    int(face['location']['top'] + face['location']['height'])]
        cv2.rectangle(img, (location[0], location[1]), (location[2], location[3]), RED_color, thickness=3)
        cv2.putText(img, face['user_list'][0]['user_info'], (location[0], location[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, RED_color,
                    thickness=1)

cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('input_image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
