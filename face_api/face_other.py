import base64
import requests


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
