from urllib import parse, request
import json
import base64
import datetime

HOST = 'localhost'
PORT = '8000'
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

def generate_data(uid, name, img_encoding):
    data = {}
    data['uid'] = uid
    data['uid_type'] = '工号'
    data['name'] = name
    data['channel'] = '测试程序'
    data['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['img'] = img_encoding
    data = stringnify(data)
    return data

# 模拟注册事件
def add_face(uid, name, img_path):
    img_encoding = read_img(img_path)
    url = ROOT_URL + 'addFaces'
    data = generate_data(uid, name, img_encoding)
    res = post(url, data)
    return res

# 模拟验证事件
def check_person(uid, name, img_path):
    img_encoding = read_img(img_path)
    url = ROOT_URL + 'checkPerson'
    data = generate_data(uid, name, img_encoding)
    res = post(url, data)
    return res

# 解析返回的json字串
def parse_result(result_str, field_name, inside_data=False):
    result_dic = json.loads(result_str)
    if not inside_data:
        return result_dic[field_name]
    else:
        return result_dic['data'][field_name]


'''测试代码
'''
def test_get():
    print(get(url=ROOT_URL))

def test_login():
    print(add_face('000001', 'trump', 'trump.jpg'))

def test_check():
    print(check_person('000001', 'trump', 'check_face/trump_3.jpg'))

if __name__ == '__main__':
    test_check()
