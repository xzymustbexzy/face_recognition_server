from urllib import parse, request
import json
import base64
import datetime

HOST = 'localhost'
PORT = '5050'
FILE = '/faceService/'
ROOT_URL = 'http://' + HOST + ':' + PORT + FILE


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

def stringnify(data):
    data = parse.urlencode(data).encode('utf-8')
    return data

def read_img(img_path):
    img = open(img_path, "rb")
    img_encoding = base64.b64encode(img.read())
    img.close()
    return img_encoding

def generate_data(uid, img_encoding):
    data = {}
    data['uid'] = uid
    data['uid_type'] = 'work id'
    data['name'] = 'test' + uid
    data['channel'] = 'for test'
    data['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['img'] = img_encoding
    data = stringnify(data)
    return data


def add_face(uid, img_path):
    img_encoding = read_img(img_path)
    url = ROOT_URL + 'addFaces'
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
def test_get():
    print(get(url=ROOT_URL))

def test_login():
    print(add_face('trump', 'trump.jpg'))

def test_check():
    print(check_person('trump', 'trump3.jpg'))

if __name__ == '__main__':
    test_check()
