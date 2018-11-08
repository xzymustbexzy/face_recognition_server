from faceService import app, db
from faceService.model.Face import Face
from faceService.model.Log import Log
from faceService.exceptions import *
import face_recognition
from flask import Flask, jsonify, request, redirect, render_template
import base64
import datetime
from faceService import NUMBER_OF_FEATURE, tolerance, login_image_root, check_image_root
import json

# 接收到人脸注册请求
@app.route('/faceService/addFaces', methods=['POST'])
def add_face():
    code = Success.code
    message = Success.msg
    try:
        uid, uid_type, name, channel, img = get_data()
    except RequestFieldMissException as e: # 请求有字段缺失，抛出异常并直接返回
        code = e.code
        message = e.msg
        return jsonify({'code':code, 'message':message})
    image_path, upload_time = decode_and_save_img(uid, img, mode='login')
    code = login_faces_in_image(uid, uid_type, name, channel, image_path, upload_time)
    return jsonify({'code':code, 'message':message})


# 接收到人脸验证请求
@app.route('/faceService/checkPerson', methods=['POST'])
def check_person():
    code = Success.code
    message = Success.msg
    extra_ret = {}
    try:
        uid, uid_type, name, channel, img = get_data()
    except RequestFieldMissException as e:# 请求有字段缺失，抛出异常并直接返回
        code = e.code
        message = e.msg
        return jsonify({'code':code, 'message':message})
    image_path, upload_time = decode_and_save_img(uid, img, mode='check')
    code, extra_ret = varify_faces_in_image(uid, uid_type, name, channel, image_path, upload_time)
    result = dict({'code':code, 'message':message}, **extra_ret)
    return jsonify(result)



# 管理员页面路由
@app.route('/', methods=['GET'])
@app.route('/faceService/backStage', methods=['GET'])
def goto_login():
    return redirect('/faceService/backStage/login')

@app.route('/faceService/backStage/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        render_template('static', filename='login.html')
    
    # 登陆请求
    id = request.form.get('id')
    pwd = request.form.get('pwd')

    if id == None or id == '':
        return '''
        请填写您的用户名
        '''
    if pwd == None or pwd == '':
        return '''
        请填写您的密码
        '''

    if id == 'admin' and pwd == '12345678':
        return redirect('/faceService/backStage/admin/')
    else:
        return '''
        账号密码错误
        '''

@app.route('/faceService/backStage/admin/', methods=['GET'])
def admin():
    return render_template('welcome.html')

# 各个管理功能模块
@app.route('/faceService/backStage/admin/parameters', methods=['GET', 'POST'])
def parameters():
    parameters = Param('./faceService/parameters.json')
    if request.method == 'GET':
        return render_template('parameters.html', parameters=parameters.getParameters)
    # 设置参数
    request.form.get('parameters')
    




'''------------------------------API------------------------------------------'''
def get_data():
    # 从request中获取数据
    uid = request.form.get('uid')
    uid_type = request.form.get('uid_type')
    name = request.form.get('name')
    channel = request.form.get('channel')
    img = request.form.get('img')

    # 判断数据的合法性
    if uid is None:
        raise RequestIdMissException()
    elif uid_type is None:
        raise RequestIdTypeMissException()
    elif name is None:
        raise RequestNameMissException()
    elif channel is None:
        raise RequestChannelMissException()
    elif img is None:
        raise RequestImgMissException()

    return uid, uid_type, name, channel, img


def decode_and_save_img(uid, img, mode):
    image_root = check_image_root if mode == 'check' else login_image_root
    #对图片进行解码并保存
    image = base64.b64decode(img)
    upload_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_name = uid + '-' + upload_time + '.jpg'
    image_path = image_root + image_name
    image_save = open(image_path, 'wb')
    image_save.write(image)
    return image_path, upload_time


# 人脸验证函数
def varify_faces_in_image(user_id, uid_type, name, channel, image_path, check_time):
    # 对加载的图片进行特征提取
    img = face_recognition.load_image_file(image_path)
    unknown_face_encodings = face_recognition.face_encodings(img)

    # 读取数据库中对应人脸的特征
    try:
        known_face_encodings = Face.query.filter_by(uid=user_id).one().feature.split('|')
    except NoResultFound:
        return NoSuchIdException.code, {}

    for i in range(NUMBER_OF_FEATURE):
        known_face_encodings[i] = float(known_face_encodings[i])

    code = Success.code
    data = {'sim':0, 'simResult':'0', 'imgFlowNo':'0'}

    passed = False

    if len(unknown_face_encodings) > 0:
        face_distance = face_recognition.face_distance([known_face_encodings], unknown_face_encodings[0])[0]
        # 对比上传的图片和数据库内的图片是否相同
        data['sim'] = 1 / face_distance
        data['simResult'] = '1' if face_distance < tolerance else '0'
        passed = True if face_distance < tolerance else False
    else:
        code = CannotFoundFaceException.code

    db.session.add(Log(uid=user_id, uid_type=uid_type, name=name, channel=channel, check_time=check_time, img_path=image_path, sim=data['sim'], result=passed))
    db.session.commit()

    return code, {'data': data}


# 人脸注册函数
def login_faces_in_image(user_id, uid_type, name, channel, image_path, login_time):
    img = face_recognition.load_image_file(image_path)
    user_face_encoding = face_recognition.face_encodings(img)[0]
    try:
        db.session.add(Face(uid=user_id, uid_type=uid_type, name=name, channel=channel, feature_array=user_face_encoding, login_time=login_time, img_path=image_path))
        db.session.commit()
    except IntegrityError:
        return LoginIdExsistsException.code
    return Success.code

#参数类
class Param:
    filepath = ''
    para_dict = {}
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath, "r") as f:
            self.para_dict = json.load(f)
    def getParameters(self):
        return self.para_dic
    def setParameters(self, parameters):
        self.para_dic = parameters
        with open(self.filepath, "w") as f:
            json.dump(self.para_dic, f)
