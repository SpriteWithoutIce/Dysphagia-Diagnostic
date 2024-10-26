import os

current_directory = os.getcwd()

files = os.listdir(current_directory)

# 要写入的文件名列表
file_names = [file for file in files if os.path.isfile(
    os.path.join(current_directory, file))]

with open('file_names.txt', 'w') as file:
    for name in file_names:
        file.write(name + '\n')

print("文件名已写入到 file_names.txt")
