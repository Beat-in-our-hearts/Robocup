import os
# 打开文件
path = "../files_dir/face_lib"
dirs = os.listdir(path)
# 输出所有文件和文件夹
for file in dirs:
    print(file)
    file_name = os.path.splitext(file)[0]
    print(file_name)
