from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

class Success(object):
    msg = '操作成功'
    code = 0

# 请求字段缺失
class RequestFieldMissException(BaseException):
    msg = '请求有字段缺失'
    code = 1

# 发送请求时没有收到id
class RequestIdMissException(RequestFieldMissException):
    def __init__(self):
        super.msg = '请求中缺失id字段，请检查！'
        super.code = 2
    def __str__(self):
        return self.msg

# 发送请求时没有收到id Type
class RequestIdTypeMissException(RequestFieldMissException):
    def __init__(self):
        super.msg = '请求中缺失id type字段，请检查！'
        super.code = 3
    def __str__(self):
        return self.msg

# 发送请求时没有收到name
class RequestNameMissException(RequestFieldMissException):
    def __init__(self):
        super.msg = '请求中缺失name字段，请检查！'
        super.code = 4
    def __str__(self):
        return self.msg


# 发送请求时没有收到channel
class RequestChannelMissException(RequestFieldMissException):
    def __init__(self):
        super.msg = '请求中缺失channel字段，请检查！'
        super.code = 5
    def __str__(self):
        return self.msg


# 发送请求时没有收到图像
class RequestImgMissException(RequestFieldMissException):
    def __init__(self):
        super.msg = '请求中缺失image字段，请检查！'
        super.code = 6
    def __str__(self):
        return self.msg


# 请求方式错误
class RequestMethodException(BaseException):
    msg = '请求方式错误！'
    code = 7
    def __str__(self):
        return self.msg


# 找不到人脸
class CannotFoundFaceException(BaseException):
    msg = '找不到人脸！'
    code = 8
    def __str__(self):
        return self.msg


# 人脸还没有注册过
class NoSuchIdException(object):
    msg = '您还没有注册过人脸！'
    code = 9


# 注册时id已经注册过人脸了
class LoginIdExsistsException(object):
    msg = '您的账号已经注册过了！'
    code = 10


# 发生未知错误
class UnknownException(BaseException):
    msg = '发生未知错误！'
    code = 11
    def __str__(self):
        return self.msg
