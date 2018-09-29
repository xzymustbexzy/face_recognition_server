from urllib import parse, request
import json
import base64
import datetime

ROOT_URL = 'http://0.0.0.0:5050/faceService/'


def post(url, data):
    req = request.Request(url=url, data=data)
    res = request.urlopen(req)
    res = res.read()
    return res

def get(url):
    req = request.Request(url=url)
    res = request.urlopen(req)
    res = res.read()
    return res

def jsonify(data):
    data = json.dumps(data).encode(encoding='utf-8')
    return data

def read_img(img_path):
    img = open(img_path, "rb")
    img_encoding = base64.b64encode(img.read())
    img.close()
    return img_encoding

def generate_data(uid, img_encoding):
    data = {}
    data['uid'] = uid
    data['uid_type'] = '工号'
    data['name'] = 'test' + uid
    data['channel'] = '测试途径'
    data['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['img'] = img_encoding
    return data


def add_face(uid, img_path):
    img_encoding = read_img(img_path)
    url = ROOT_URL + 'addFace'
    data = generate_data(uid, img_encoding)
    res = post(url, data)
    return res

def check_person(uid, img_path):
    img_encoding = read_img(img_path)
    url = ROOT_URL + 'checkPerson'
    data = generate_data(uid, img_encoding)
    res = post(url, data)
    return res



'''测试代码'''
def simple_test():
    print(get(url=ROOT_URL))

if __name__ == '__main__':
    simple_test()