# encoding:utf-8


import pymysql
import time
from flask import Flask


def getResponse(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response


def log(type, context):
    print((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), " " + type + " " + context)
