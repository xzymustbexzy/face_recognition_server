from server import app, db
from server.model.Face import Face
from server.model.Log import Log
import face_recognition
from flask import Flask, jsonify, request, redirect
import base64
import datetime
from server import NUMBER_OF_FEATURE, tolerance

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
        image_root = 'server/image/'
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
