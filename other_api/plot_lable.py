import cv2
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

RED_color = (0, 0, 255)
BLUE_color = (255, 0, 0)
GREEN_color = (0, 255, 0)

pil_color = (255, 0, 0)
pil_txt_color = (255, 255, 255)

font_path = "C:\Windows\Fonts\Arial.ttf"


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
    调用cv2.rectangle，cv2.putText给图片做标注信息
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


def plot_time_on_pic(im):
    label = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    font = ImageFont.truetype(font_path, size=max(round(max(im.size) / 40), 12))
    txt_width, txt_height = font.getsize(label)
    draw = ImageDraw.Draw(im)
    draw.rectangle([0, 0, txt_width, txt_height], fill=pil_color)
    draw.text((0, 0), label, fill=pil_txt_color, font=font)
