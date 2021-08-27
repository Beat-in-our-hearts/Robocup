from PIL import Image, ImageDraw, ImageFont
import glob
import os
import time

pic_path = "../our_image/xz组训练集/image_set"
path_save = "../our_image/xz组训练集/image_set/result"

# now = time.perf_counter()
# im = Image.open(img_path)
# im.thumbnail((960, 540))
# print(im.format, im.size, im.mode)
# im.save(path_save, 'JPEG')
# print(time.perf_counter() - now)

# 待测图片的存储路径
dirs = os.listdir(pic_path)
print(f"Find {len(dirs)} files in {pic_path}:{dirs}\nFinding...")
num = 0
length = len(dirs)
# 遍历待测图片
for file in dirs:
    im = Image.open(f"{pic_path}/{file}")
    im.thumbnail((1920, 1080))
    im.save(f"{path_save}/{file}", 'JPEG')
    im.close()
    num += 1
    # print(f"{im.format}-{im.size}-{im.mode}{num}/{length}....")
