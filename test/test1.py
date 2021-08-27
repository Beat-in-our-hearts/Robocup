# encoding:utf-8
import base64
import requests

'''
人脸检测与属性分析
'''
access_token = '24.c4bc8bad00b07a661e661f697ad20cb7.2592000.1631961695.282335-24724684'
base64_data = None
with open("../1.jpeg", 'rb') as f:
    base64_data = base64.b64encode(f.read())
    base64_str = base64_data.decode("utf-8")

request_url = f"https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={access_token}"
# print(request_url)
params = {"image":base64_str,"image_type":"BASE64","face_field":"age,expression,gender"}
# print(params)
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())
