# 环境配置：
# 首先需要安装python3以及pip3
# 再安装face_recognition库，在shell中输入pip3 install face_recognition
#（其间可能需要手动安装dlib库，视情况而定，dlib库需要cmake编译，又因为本身是c++库需要python boost dev来转换成python库）
# 然后安装flask用于编写servlet
# 读写mysql数据库用flask_sqlalchemy

from server import app

# 服务器为localhost，运行的端口号为5050
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
