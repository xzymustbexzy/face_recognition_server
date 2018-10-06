from server import app, db
from server.model.Face import Face
from server.model.Log import Log
import sqlalchemy
import face_recognition
from flask import Flask, jsonify, request, redirect
import base64
import datetime
from server import NUMBER_OF_FEATURE, tolerance

#返回的code所对应的消息
messages = {
    0:'Success',
    1:'Request mothed error!',
    2:'Can not find face',
    3:'Your id have been already logined'
}

def com_ret(code):
    result = {
        'code':code,
        'message':messages[code]
    }
    return result


def get_data():
    uid = request.form.get('uid')
    uid_type = request.form.get('uid_type')
    name = request.form.get('name')
    channel = request.form.get('channel')
    img = request.form.get('img')
    if (uid is None) or (img is None):
        return redirect(request.url)

    return uid, uid_type, name, channel, img


def decode_and_save_img(uid, img):
    #对图片进行解码并保存
    image = base64.b64decode(img)
    image_root = 'server/image/'
    upload_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_name = uid + '-' + upload_time + '.jpg'
    image_path = image_root + image_name
    image_save = open(image_path, 'wb')
    image_save.write(image)
    return image_path, upload_time

# 接收到人脸注册请求
@app.route('/faceService/addFaces', methods=['POST'])
def add_face():
    uid, uid_type, name, channel, img = get_data()
    code = 0
    image_path, upload_time = decode_and_save_img(uid, img)
    code = login_faces_in_image(uid, uid_type, name, channel, image_path, upload_time)
    result = com_ret(code)
    return jsonify(result)


# 接收到人脸验证请求
@app.route('/faceService/checkPerson', methods=['POST'])
def check_person(): 
    uid, uid_type, name, channel, img = get_data()
    extra_ret = {}
    code = 0
    image_path, upload_time = decode_and_save_img(uid, img)
    code, extra_ret = varify_faces_in_image(uid, uid_type, name, channel, image_path, upload_time)
    result = dict(com_ret(code), **extra_ret)
    return jsonify(result)


# 接收到修改参数请求
@app.route('/faceService/serParameters', methods=['POST'])
def set_parameters():
    return '''
        set parameters
        '''


def varify_faces_in_image(user_id, uid_type, name, channel, image_path, check_time):
    # 对加载的图片进行特征提取
    img = face_recognition.load_image_file(image_path)
    unknown_face_encodings = face_recognition.face_encodings(img)

    # 读取数据库中对应人脸的特征
    known_face_encodings = Face.query.filter_by(uid=user_id).one().feature.split('|')
    for i in range(NUMBER_OF_FEATURE):
        known_face_encodings[i] = float(known_face_encodings[i])

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
    try:
        db.session.add(Face(uid=user_id, uid_type=uid_type, name=name, channel=channel, feature_array=user_face_encoding, login_time=login_time, img_path=image_path))
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return 3
    return 0
