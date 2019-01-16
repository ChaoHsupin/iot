# encoding:utf-8
# 外部文件引入
import pojo
import crabapple as crab
from config import getResponse, log
# 依赖模块
import time
import datetime
import re
import pymysql
from flask_cors import CORS
from DBUtils.PooledDB import PooledDB
from flask import Flask, request, render_template, jsonify, send_from_directory, make_response


# list monitor
def getMonitors(req):
    if not crab.checkToken(req):
        return crab.responseMsg(0, "Your identity is not identified!")
    sql = "SELECT * FROM monitor"
    try:
        values = req.get_json()
        sql += (" WHERE"+crab.getByConditions(values))
    except:
        sql = sql
    try:
        res = monitorPojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get monitor information failure!")


def monitorPojo(data):
    pojoModel = ['monitor_id', 'sensor_id', 'value', 'create_time']
    return crab.toList(pojoModel, data)
