# encoding:utf-8
# 外部文件引入
# 依赖模块
import base64
import hashlib
import time
import pymysql
from DBUtils.PooledDB import PooledDB
from flask import jsonify, make_response

db_config = {"host": "www.crabapple.xyz",
             "user": "root",
             "passwd": "123456",
             "db": "IOT",
             "charset": "utf8"
             }

spool = PooledDB(pymysql, 10, **db_config)


def sqlExe(SQL):
    conn = spool.connection()
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    re = cur.fetchall()
    cur.close()
    conn.close()
    return re


global userId
userId = -1


# getToken
def getToken(userId, username, password):
    if userId == None or username == None or password == None:
        return None
    dictStr = str({"userId": userId, "username": username, "password": password})
    set_time = str((int(time.time())) + 3600)
    tokenMethod = hashlib.md5("MD5".encode(encoding='UTF-8')).hexdigest()
    tokenTime = hashlib.md5(set_time.encode(encoding='UTF-8')).hexdigest()
    tokenInfo = hashlib.md5(dictStr.encode(encoding='UTF-8')).hexdigest()
    token = tokenMethod + "." + tokenTime + "." + tokenInfo
    return token


# get userId
def getUserId():
    global userId
    return userId


# 检查token是否过期
def checkToken(req):
    try:
        token = req.headers["Authorization"]
        global userId
        sql = u"SELECT user_id,end_time FROM user WHERE token='{}'".format(token)
        p = sqlExe(sql)
        if len(p) == 0:
            return -1
        else:
            userId = int(p[0][0])
        timestr = str(p[0][1])
        current_time = (int(time.time()))
        token_end_time = (int(time.mktime(time.strptime(timestr, "%Y-%m-%d %H:%M:%S"))))
        mines = current_time - token_end_time
        if 0 < mines and mines < 3600:
            return userId
        else:
            return -1
    except:
        return -1


# return data
def responseDate(code, info):
    response = make_response(jsonify({"code": code, "data": info}))
    response = setHeder(response)
    return response


# return msg
def responseMsg(code, info):
    response = make_response(jsonify({"code": code, "msg": info}))
    response = setHeder(response)
    return response


# return token
def responsToken(token):
    res = responseDate(0, {"token": token})
    res.headers['Authorization'] = token
    return res


# Set heder information
def setHeder(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


# 生成token
def getRandomStr(userId):
    return str(userId) + '.' + str(base64.b64encode(str(time.time()).encode('utf-8')), 'utf-8')


# 数据库结果映射字典
def toList(pojoModel, data):
    re = []
    for i in range(len(data)):
        dict = {}
        for j in range(len(pojoModel)):
            dict[pojoModel[j]] = data[i][j]
        re.append(dict)
    return re


# 多条件查询 条件语句生成器
def getByConditions(conList):
    length = len(conList)
    if length == 0:
        return ""
    else:
        index = 1
        sql = " "
        for i in conList:
            if i == 'begin_time':
                sql += "AND create_time > \"" + str(conList['begin_time']) + "\""
            elif i == 'end_time':
                sql += "AND create_time < " + "\"" + str(conList['end_time']) + "\""
            else:
                if isinstance(conList[i], str):
                    sql += (" " + str(i) + " = " + "\"" + str(conList[i]) + "\"")
                else:
                    sql += (" " + str(i) + " = " + str(conList[i]))
            if index != length:
                sql += " AND"
            index += 1
        return sql
