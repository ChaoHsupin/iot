# encoding:utf-8
# 外部文件引入

# 依赖模块
from random import sample
import time
import re
import pymysql
from DBUtils.PooledDB import PooledDB
from flask import render_template, jsonify, make_response

db_config = {"host": "localhost",
             "user": "root",
             "passwd": "123456",
             "db": "iot",
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
userId=-1

#get userId
def getUserId():
    global userId
    return userId

# 检查token是否过期
def checkToken(req):
    token =req.headers["Authorization"]
    global userId
    sql = u"SELECT user_id,end_time FROM user WHERE token='{}'".format(token)
    p = sqlExe(sql)
    if len(p)==0:
        return False
    else:
        userId=int(p[0][0])
    timestr = str(p[0][1])
    current_time = (int(time.time()))
    token_end_time = (int(time.mktime(time.strptime(timestr, "%Y-%m-%d %H:%M:%S"))))
    mines = current_time - token_end_time
    if 0 < mines and mines < 3600:
        return True
    else:
        return False


# return data
def responseDate(code, info):
    response = make_response(jsonify({"code": code, "data": info}))
    response=setHeder(response)
    return response

# return msg
def responseMsg(code, info):
    response = make_response(jsonify({"code": code, "msg": info}))
    response=setHeder(response)
    return response

# return token
def responsToken(token):
    res=responseMsg(0,"Login successfully!")
    res.headers['Authorization'] = token
    return res

# Set heder information
def setHeder(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

# 随机生成一组10位字符串
def getRandomStr():
    Num = [i for i in range(36)]
    for i in range(10):
        Num[i] = chr(i + ord('0'))
    for i in range(26):
        Num[10 + i] = chr(i + ord('A'))
    return str(''.join(sample(Num, 10)))



# 数据库结果映射字典
def toList(pojoModel,data):
    re=[]
    for i in range(len(data)):
        dict={}
        for j in range(len(pojoModel)):
            dict[pojoModel[j]]=data[i][j]
        re.append(dict)
    return re

# 多条件查询 条件语句生成器
def getByConditions(conList):
    length=len(conList)
    if length==0:
        return ""
    else:
        index=1
        sql=" "
        for i in conList:
            if i=='begin_time':
                sql+=" create_time > \""+str(conList['begin_time'])+"\""
            elif i=='end_time':
                sql+=" create_time < "+"\""+str(conList['end_time'])+"\""
            else:
                if isinstance(conList[i], str):
                    sql += (" " + str(i) + " = " +"\"" +str(conList[i])+"\"")
                else:
                    sql += (" " + str(i) + " = " +str(conList[i]))
            if index != length:
                sql+=" AND"
            index+=1
        return sql