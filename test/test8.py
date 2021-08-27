from utils.plots import colors, plot_one_box
import sys
import time
from pathlib import Path
import torch
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

im = Image.open("../example/example1.png")

lw = max(int(min(im.size) / 200), 2)  # line width
draw = ImageDraw.Draw(im)
box=(100,100,200,200)
color=(128, 128, 128)
txt_color=(255, 255, 255)
draw.rectangle(box, width=lw + 1, outline=color)  # plot
label = "hee"
font = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", size=max(round(max(im.size) / 40), 12))
txt_width, txt_height = font.getsize(label)
draw.rectangle([box[0], box[1] - txt_height + 4, box[0] + txt_width, box[1]], fill=color)
draw.text((box[0], box[1] - txt_height + 1), label, fill=txt_color, font=font)

im.show()
