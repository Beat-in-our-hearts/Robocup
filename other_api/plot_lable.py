import cv2
from datetime import datetime
import os

from PIL import Image, ImageDraw, ImageFont

RED_color = (0, 0, 255)
BLUE_color = (255, 0, 0)
GREEN_color = (0, 255, 0)

pil_color = (255, 0, 0)
pil_txt_color = (255, 255, 255)

# 获取上级目录
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
font_path = root_path + "/Arial.ttf"

def Draw_Box_in_face_with_txt(image, face_list, text_info_list, show_mode=0):
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


def Draw_Box_on_faces_cv2(image, face_list, show_mode=0):
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


def Draw_Box_on_faces_PIL(im, face_list, show_mode=0):
    """
    调用draw.rectangle,draw.text绘制方框
    :param im: PIL(Image) 图片类型
    :param face_list: 百度API调用结果中人脸识别信息
    :param show_mode: 0：不显示；1：显示图片
    :return:
    """
    for face in face_list:
        if len(face['user_list']) != 0:
            location = [int(face['location']['left']), int(face['location']['top']),
                        int(face['location']['left']) + int(face['location']['width']),
                        int(face['location']['top'] + face['location']['height'])]
            lw = max(int(min(im.size) / 200), 2)  # line width
            draw = ImageDraw.Draw(im)
            draw.rectangle(location, width=lw + 1, outline=pil_color)  # plot
            label = face['user_list'][0]['user_info']
            font = ImageFont.truetype(font_path, size=max(round(max(im.size) / 40), 12))
            txt_width, txt_height = font.getsize(label)
            draw.rectangle([location[0], location[1] - txt_height + 4, location[0] + txt_width, location[1]],
                           fill=pil_color)
            draw.text((location[0], location[1] - txt_height + 1), label, fill=pil_txt_color, font=font)
    if show_mode != 0:
        im.show()


def Draw_Box_on_single_face_PIL(im, location, text, show_mode=0):
    """
    调用draw.rectangle,draw.text绘制方框，文字默认为方框的上一行
    :param im: PIL(Image) 图片类型
    :param location:  四元组（xyxy）
    :param show_mode: 0：不显示；1：显示图片
    :return:
    """
    lw = max(int(min(im.size) / 200), 2)  # line width
    draw = ImageDraw.Draw(im)
    draw.rectangle(location, width=lw + 1, outline=pil_color)  # plot
    font = ImageFont.truetype(font_path, size=max(round(max(im.size) / 40), 12))
    txt_width, txt_height = font.getsize(text)
    draw.rectangle([location[0], location[1], location[0] + txt_width, location[1] + txt_height+4],
                   fill=pil_color)
    draw.text((location[0], location[1]), text, fill=pil_txt_color, font=font)

    if show_mode != 0:
        im.show()


def Draw_txt_on_single_face_PIL(im, location, text, show_mode=0):
    """
    draw.text添加文字信息，默认在方框的下一行
    :param im: PIL(Image) 图片类型
    :param location: 四元组（xyxy）
    :param show_mode: 0：不显示；1：显示图片
    :return:
    """
    lw = max(int(min(im.size) / 200), 2)  # line width
    draw = ImageDraw.Draw(im)
    # draw.rectangle(location, width=lw + 1, outline=pil_color)  # plot
    font = ImageFont.truetype(font_path, size=max(round(max(im.size) / 40), 12))
    txt_width, txt_height = font.getsize(text)
    draw.rectangle([location[0], location[3] - txt_height - 4, location[0] + txt_width, location[3]],
                   fill=pil_color)
    draw.text((location[0], location[3] - txt_height - 4), text, fill=pil_txt_color, font=font)

    if show_mode != 0:
        im.show()


def plot_time_on_pic(im):
    label = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    font = ImageFont.truetype(font_path, size=max(round(max(im.size) / 40), 12))
    txt_width, txt_height = font.getsize(label)
    draw = ImageDraw.Draw(im)
    draw.rectangle([0, 0, txt_width+2, txt_height+5], fill=pil_color)
    draw.text((0, 0), label, fill=pil_txt_color, font=font)
