from API import add_face, check_person, parse_result
import os
import json
import threading

class login_agent(threading.Thread):
    def __init__(self, threadID, name, file_folder):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.file_folder = file_folder
    def run(self):
        print ("开始线程：" + self.name)
        self.multithread_login()
        print ("退出线程：" + self.name)

    def multithread_login(self):
        file_folder_path = os.getcwd() + '/' + self.file_folder
        image_name_list = os.listdir(file_folder_path)
        name_list = [os.path.splitext(fullname)[0] for fullname in image_name_list]
        for i in range(len(name_list)):
            res = add_face(str(self.threadID) + ':' + str(i), name_list[i], self.file_folder + image_name_list[i])
            code = parse_result(res, 'code')
            assert (code == 0) # 断言添加成功
            print('成功添加用户' + name_list[i])
        print('已成功添加' + str(len(name_list)) + '个用户！')

if __name__ == '__main__':
    thread0 = login_agent(0, '线程0', 'login_face/batch_01/')
    thread1 = login_agent(1, '线程1', 'login_face/batch_02/')
    thread2 = login_agent(2, '线程2', 'login_face/batch_03/')
    thread3 = login_agent(3, '线程3', 'login_face/batch_04/')
    thread0.start()
    thread1.start()
    thread2.start()
    thread3.start()
    thread0.join()
    thread1.join()
    thread2.join()
    thread3.join()
    print('批量注册完成！')
