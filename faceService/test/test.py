from API import add_face, check_person, parse_result
import os

def batch_login(file_folder):
    file_folder_path = os.getcwd() + '/' + file_folder
    image_name_list = os.listdir(file_folder_path)
    uid_list = [os.path.splitext(fullname)[0] for fullname in image_name_list]
    for i in range(len(uid_list)):
        res = add_face(uid_list[i], file_folder + image_name_list[i])
        code = parse_result(res, 'code')
        assert (code == 0) # 断言添加成功
    print('已成功添加' + str(len(uid_list)) + '个用户！')


if __name__ == '__main__':
    batch_login('login_image/') #批量添加人脸
