# 环境配置：
# 首先需要安装python3以及pip3
# 再安装face_recognition库，在shell中输入pip3 install face_recognition
#（其间可能需要手动安装dlib库，视情况而定，dlib库需要cmake编译，又因为本身是c++库需要python boost dev来转换成python库）
# 然后安装flask用于编写servlet
# 读写mysql数据库用flask_sqlalchemy

import face_recognition
from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json, base64

# 合法的图像文件后缀
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

NUMBER_OF_FEATURE = 128

app = Flask(__name__)
# config用于配置数据库属性
# SQLALCHEMY_DATABASE_URI是访问数据库的URL，格式为'mysql:username:password@localhost:3307/database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:profilebook@localhost:3307/faceDB'
# SQLALCHEMY_TRACK_MODIFICATIONS表示是否立即写入数据库，设置为False，可以提高效率
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库的一个表在flask中对应一个类
class login_face(db.Model):
    # __tablename__用于定义表名
    __tablename__ = 'login_face'
    # 接下去的变量是字段名，用db.Column来定义字段属性
    id = db.Column(db.String(32), primary_key=True)
    id_type = db.Column(db.String(16))
    name = db.Column(db.String(15))
    channel = db.Column(db.String(16))
    upload_date = db.Column(db.Time)
    feature = db.Column(db.String(4096))
    # 构造方法
    def __init__(self, id, id_type, name, channel, upload_date, feature_array):
        self.id = id
        self.id_type = id_type
        self.name = name
        self.channel = channel
        self.upload_date = upload_date
        self.feature = self.to_feature_string(feature_array)

    def to_feature_string(self, feature_array):
        feature_string = ''
        for i in range(NUMBER_OF_FEATURE - 1):
            feature_string += (str(feature_array[i]) + '|')
        feature_string += str(feature_array[NUMBER_OF_FEATURE - 1])
        return feature_string


class varify_record(db.Model):
    __tablename__ = 'varify_record'

    id = db.Column(db.String(32), primary_key=True)
    id_type = db.Column(db.String(16))
    name = db.Column(db.String(15))
    channel = db.Column(db.String(16))
    upload_date = db.Column(db.Time)
    # 构造方法
    def __init__(self, id, id_type, name, channel, upload_date, feature_array):
        self.id = id
        self.id_type = id_type
        self.name = name
        self.channel = channel
        self.upload_date = upload_date



# 判断传入的文件是不是合法的图像
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/faceService/addFaces', methods=['POST'])
@app.route('/faceService/checkPerson', methods=['POST'])
@app.route('/', methods=['GET'])
def upload():
    # 如果不是POST，则返回URL
    if request.method == 'POST':

        data = json.loads(request.form.get('data'))

        if 'methodName' not in data:
            splited_url = request.base_url.split('/')
            data['method'] = splited_url[-1]
        if data['methodName'] == 'setParameters':
            return '''
                set setparameters
            '''

        if ('cId' not in data) or ('img' not in data):
            return redirect(request.url)


        image = base64.b64decode(data['img'])
        user_id = data['cId']

        if data['methodName'] == 'addFaces':
            login_faces_in_image(user_id, image)
        if data['methodName'] == 'checkPerson':
            varify_faces_in_image(user_id, file)



    # 如果请求类型为GET，则返回主页面
    return '''
    <!doctype html>
    <title>Is this a picture of Obama?</title>
    <h1>Sign up for your face and varify via your identification!</h1>
    <form name="form" method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="text" name="user_id">
      <input type="button" name="login"  value="Login">
      <input type="button" name="upload"  value="Varify">
    </form>
    <script>
        alert("hello world");
      $("input[name="login"]").click(function() {

        $.ajax(
            type:"POST",
            url:"http://0.0.0.0:5050/faceService/addFaces",
            contentType:"application/json;charset=utf-8"
            data:JSON.stringify(GetJsonData()),
            dataType:"json",
            success: function(message) {
                alert("success");
            }
            error: function(message) {
                alert("failed");
            }
        );
        }
    )

    function GetJsonData() {

        var json = {
            "methodName":"setParameters",
            "cId":"330283199710244712",
            "cName":"xiaoziyang",
            "cType":"gonghao",
            "img":"",
            "channel":"pc"
        }
        return json;
    }
    </script>

    '''


def varify_faces_in_image(user_id, img):
    # sql = 'select feature from face_record where id = \'' + user_id + '\''
    # item = list()
    # item = db.session.execute(sql)
    # unknown_face_encodings = item[0].feature.split('|')
    known_face_encodings = Face.query.filter_by(id = user_id).one().feature.split('|')
    for i in range(NUMBER_OF_FEATURE):
        known_face_encodings[i] = float(known_face_encodings[i])

    # 对加载的图片进行特征提取
    unknown_face_encodings = face_recognition.face_encodings(img)

    # face_found是一个bool值，表示是否从图片中找到了人脸，没有找到人脸，编码长度为0
    face_found = False
    # passed表示是否通过人脸验证
    passed = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # 对比上传的图片和数据库内的图片是否相同
        match_results = face_recognition.compare_faces([known_face_encodings], unknown_face_encodings[0])
        if match_results[0]:
            passed = True

    # 将结果用json格式返回
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": passed
    }
    return jsonify(result)

def login_faces_in_image(user_id, img):
    user_face_encoding = face_recognition.face_encodings(img)[0]
    db.session.add(Face(user_id, user_face_encoding))
    db.session.commit()
    print("login successfully")
    return '''
    <!doctype html>
    <head>Login successfully!</head>
    '''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
