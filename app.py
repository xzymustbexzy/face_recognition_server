# 环境配置：
# 首先需要安装python3以及pip3
# 再安装face_recognition库，在shell中输入pip3 install face_recognition
#（其间可能需要手动安装dlib库，视情况而定，dlib库需要cmake编译，又因为本身是c++库需要python boost dev来转换成python库）
# 然后安装flask用于编写servlet
# 读写mysql数据库用flask_sqlalchemy

import face_recognition
from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import base64
import datetime

# 合法的图像文件后缀
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

NUMBER_OF_FEATURE = 128

tolerance = 0.6

app = Flask(__name__)
# config用于配置数据库属性
# SQLALCHEMY_DATABASE_URI是访问数据库的URL，格式为'mysql:username:password@localhost:3307/database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:profilebook@localhost:3307/faceDB'
# SQLALCHEMY_TRACK_MODIFICATIONS表示是否立即写入数据库，设置为False，可以提高效率
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库的一个表在flask中对应一个类
class Face(db.Model):
    # __tablename__用于定义表名
    __tablename__ = 'login_face'
    # 接下去的变量是字段名，用db.Column来定义字段属性
    uid = db.Column(db.String(32), primary_key=True)#用户id
    uid_type = db.Column(db.String(16))#用户id的类型
    name = db.Column(db.String(15))#用户名
    channel = db.Column(db.String(16))#提交渠道
    login_time = db.Column(db.String(19))#注册时间
    feature = db.Column(db.String(4096))#特征字串
    img_path = db.Column(db.String(4096))#图片存放路径
    # 构造方法
    def __init__(self, uid, uid_type, name, channel, login_time, feature_array, img_path):
        self.uid = uid
        self.uid_type = uid_type
        self.name = name
        self.channel = channel
        self.login_time = login_time
        self.feature = self.to_feature_string(feature_array)
        self.img_path = img_path


def to_feature_string(self, feature_array):#将特征向量转化为特征字串
        feature_string = ''
        for i in range(NUMBER_OF_FEATURE - 1):
            feature_string += (str(feature_array[i]) + '|')
        feature_string += str(feature_array[NUMBER_OF_FEATURE - 1])
        return feature_string


class Log(db.Model):
    __tablename__ = 'check_log'

    num = db.Column(db.Integer, primary_key=True, autoincrement=True)#图片流水号
    uid = db.Column(db.String(32))#用户id
    uid_type = db.Column(db.String(16))#用户id的类型
    name = db.Column(db.String(15))#用户名
    channel = db.Column(db.String(16))#提交渠道
    check_time = db.Column(db.String(19))#验证时间
    img_path = db.Column(db.String(4096))#图片存放路径
    result = db.Column(db.Boolean)#验证结果
    sim = db.Column(db.Float)#验证相似度
    # 构造方法
    def __init__(self, uid, uid_type, name, channel, check_time, img_path, sim, result):
        self.uid = uid
        self.uid_type = uid_type
        self.name = name
        self.channel = channel
        self.check_time = check_time
        self.img_path = img_path
        self.sim = sim
        self.result = result



# 判断传入的文件是不是合法的图像
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#返回的code所对应的消息
messages = {
    0:'Success',
    1:'Request mothed error!',
    2:'Can not find face'
}

def com_ret(code):
    result = {
        'code':code,
        'message':messages[code]
    }
    return result

@app.route('/faceService/addFaces', methods=['POST'])
@app.route('/faceService/checkPerson', methods=['POST'])
@app.route('/faceService/', methods=['GET'])
def upload():

    extra_ret = {}
    code = 0

    # 如果不是POST，则返回URL
    if request.method == 'POST':

        methodName = request.form.get('method')
        uid = request.form.get('uid')
        uid_type = request.form.get('uid_type')
        name = request.form.get('name')
        channel = request.form.get('channel')
        img = request.form.get('img')

        print('uid_type=', uid_type)
        print('name=', name)
        print('channel=', channel)

        if methodName is None:
            splited_url = request.base_url.split('/')
            methodName = splited_url[-1]
        if methodName == 'setParameters':
            return '''
                set setparameters
            '''

        if (uid is None) or (img is None):
            return redirect(request.url)

        #对图片进行解码并保存
        image = base64.b64decode(img)
        image_root = 'image/'
        upload_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_name = uid + '-' + upload_time + '.jpg'
        image_path = image_root + image_name
        image_save = open(image_path, 'wb')
        image_save.write(image)

        user_id = uid

        if methodName == 'addFaces':
            code = login_faces_in_image(user_id, uid_type, name, channel, image_path, upload_time)
        if methodName == 'checkPerson':
            code, extra_ret = varify_faces_in_image(user_id, uid_type, name, channel, image_path, upload_time)



    else:
        code = 1

    result = dict(com_ret(code), **extra_ret)
    return jsonify(result)


def varify_faces_in_image(user_id, uid_type, name, channel, image_path, check_time):
    # sql = 'select feature from face_record where id = \'' + user_id + '\''
    # item = list()
    # item = db.session.execute(sql)
    # unknown_face_encodings = item[0].feature.split('|')
    known_face_encodings = Face.query.filter_by(uid=user_id).one().feature.split('|')
    for i in range(NUMBER_OF_FEATURE):
        known_face_encodings[i] = float(known_face_encodings[i])

    # 对加载的图片进行特征提取
    img = face_recognition.load_image_file(image_path)
    unknown_face_encodings = face_recognition.face_encodings(img)


    code = 0
    data = {'sim':0, 'simResult':'0', 'imgFlowNo':'0'}

    passed = False

    if len(unknown_face_encodings) > 0:
        face_distance = face_recognition.face_distance([known_face_encodings], unknown_face_encodings[0])[0]
        # 对比上传的图片和数据库内的图片是否相同
        data['sim'] = 1 / face_distance
        data['simResult'] = '1' if face_distance < tolerance else '0'
        passed = True if face_distance < tolerance else False
    else:
        code = 2


    db.session.add(Log(uid=user_id, uid_type=uid_type, name=name, channel=channel, check_time=check_time, img_path=image_path, sim=data['sim'], result=passed))
    db.session.commit()

    return code, {'data': data}

def login_faces_in_image(user_id, uid_type, name, channel, image_path, login_time):

    img = face_recognition.load_image_file(image_path)
    user_face_encoding = face_recognition.face_encodings(img)[0]
    db.session.add(Face(uid=user_id, uid_type=uid_type, name=name, channel=channel, feature_array=user_face_encoding, login_time=login_time, img_path=image_path))
    db.session.commit()
    return 0

#运行的端口号为5050
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
