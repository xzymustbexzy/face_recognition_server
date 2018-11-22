from faceService import app, db
from faceService.model.Face import Face
from faceService.model.Log import Log
from faceService.exceptions import *
import face_recognition
from flask import Flask, jsonify, request, redirect, render_template, url_for
import base64, math
import datetime
from faceService import NUMBER_OF_FEATURE, NUMBER_OF_PERSON_PER_PAGE, tolerance, login_image_root, check_image_root
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
        return render_template('login.html')

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

@app.route('/faceService/backStage/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('welcome.html')
    resource = request.form.get('resource')
    if resource is None:
        return render_template('welcome.html')
    elif resource == 'parameters':
        return parameters()
    elif resource == 'loginedFace':
        page_id = request.form.get('page_id')
        return loginedFace(page_id)
    elif resource == 'checkLog':
        page_id = request.form.get('page_id')
        return checkLog(page_id)

# 各个管理功能模块
def parameters():
    parameters = Param('./faceService/parameters.json')
    action = request.form.get('action')
    if action == 'get':
        return render_template('parameters.html', parameters=parameters.getParameters())
    # 设置参数
    i = 0
    param_list = []
    while True:
        param = request.form.get('param' + str(i))
        i = i + 1
        if param is None:
            break
        param_list.append(param)
    parameters.setParameters(param_list)
    return render_template('parameters.html', parameters=parameters.getParameters())


def loginedFace(page_id):
    persons = []
    person_set = Face.query.all()
    person_num = len(person_set)
    page_num = math.floor(person_num/NUMBER_OF_PERSON_PER_PAGE) + 1
    page_id = int(page_id)
    for i in range((page_id - 1) * NUMBER_OF_PERSON_PER_PAGE, min(page_id * NUMBER_OF_PERSON_PER_PAGE, person_num)):
        p = person_set[i]
        person = {}
        person['id'] = p.uid
        person['id_type'] = p.uid_type
        person['name'] = p.name
        person['channel'] = p.channel
        person['login_time'] = p.login_time
        root_image_path = 'faceService/static/images/'
        person['path'] = p.img_path[len(root_image_path):]
        persons.append(person)
    return render_template('loginedFace.html', persons=persons,total_page_num=page_num)


def checkLog(page_id):
    logs = []
    log_set = Log.query.all()
    log_num = len(log_set)
    log_num =  math.floor(log_num/NUMBER_OF_PERSON_PER_PAGE) + 1
    page_id = int(page_id)
    for i in range((page_id - 1) * NUMBER_OF_PERSON_PER_PAGE, min(page_id * NUMBER_OF_PERSON_PER_PAGE, log_num)):
        L = log_set[i]
        log = {}
        log['num'] = L.num
        log['id'] = L.uid
        log['id_type'] = L.uid_type
        log['name'] = L.name
        log['channel'] = L.channel
        log['check_time'] = L.check_time
        log['sim'] = L.sim
        log['result'] = L.result
        root_image_path = 'faceService/static/images/'
        log['path'] = L.img_path[len(root_image_path):]
        logs.append(log)

    return render_template('checkLog.html', logs=logs)

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
    upload_time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
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
        data['sim'] = 1 - face_distance
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
        para_list = []
        name_map = {'check_image_root':'验证人脸照片存放路径',
                    'login_image_root':'注册人脸照片存放路径',
                    'tolerance':'容忍度'
                    }
        i = 0
        for key in self.para_dict:
            parameter = {}
            parameter['name'] = name_map[key]
            parameter['value'] = self.para_dict[key]
            parameter['no'] = 'param' + str(i)
            i = i + 1
            para_list.append(parameter)
        return para_list
    def setParameters(self, param_list):
        i = 0
        for key in self.para_dict:
            self.para_dict[key] = param_list[i]
            i = i + 1
        with open(self.filepath, "w") as f:
            json.dump(self.para_dict, f)



