# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# 创建项目对象
app = Flask(__name__)

# 加载配置文件
app.config.from_object('server.setting')     #模块下的setting文件名，不用加py后缀
app.config.from_envvar('FLASK_SETTINGS')   #环境变量，指向配置文件setting的路径，需手动配置
# ubuntu: export FLASK_SETTINGS=~/face_recognition/face_recognition_server/server/setting.py

NUMBER_OF_FEATURE = 0
tolerance = 0
with open('server/parameters.json', 'r') as parameters:
    parameters_dic = json.load(parameters)

'''parameters variable'''
NUMBER_OF_FEATURE = parameters_dic['NUMBER_OF_FEATURE']
tolerance = parameters_dic['tolerance']

#创建数据库对象
db = SQLAlchemy(app)

from server.model import Face, Log

from server.controller import faceService
