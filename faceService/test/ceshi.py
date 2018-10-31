import os
root = '/'
file_folder = 'login_image'
file_folder_path = os.getcwd() + '/faceService/test/' + file_folder + '/'
image_name_list = os.listdir(file_folder_path)
uid_list = []
uid_list = [fullname.split('.')[0] for fullname in image_name_list]
print(uid_list)