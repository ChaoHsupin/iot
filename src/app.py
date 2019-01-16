# encoding:utf-8

# 外部文件引入

from flask import Flask, request
# 依赖模块
from flask_cors import CORS

import src.device.deviceApi as deviceApi
import src.monitor.monitorApi as monitorApi
import src.sensor.sensorApi as sensorApi
import src.user.userApi as userApi

app = Flask(__name__)
CORS(app, supports_credentials=True)


# 用户登陆
@app.route('/user/login', methods=['POST'])
def login():
    return userApi.login(request)


# 用户登出
@app.route('/user/logout', methods=['POST'])
def logout():
    return userApi.logout(request)


# 用户注册
@app.route('/user/register', methods=['POST'])
def register():
    return userApi.register(request)


# 添加设备
@app.route('/device/add', methods=['POST'])
def deviceAdd():
    return deviceApi.addDevice(request)


# 删除设备
@app.route('/device/del', methods=['POST'])
def deviceDel():
    return deviceApi.delDevice(request)


# 修改设备
@app.route('/device/edit', methods=['POST'])
def deviceEdit():
    return deviceApi.editDevice(request)


# 查询设备 String[deviceId]  不填返回所有
@app.route('/device/list', methods=['POST'])
def devices():
    return deviceApi.getDevices(request)


# 查询当前用户设备
@app.route('/device/current', methods=['POST'])
def curdevices():
    return deviceApi.getCurrentDevices(request)


# 添加传感器
@app.route('/sensor/add', methods=['POST'])
def sensorAdd():
    return sensorApi.addSensor(request)


# 删除传感器
@app.route('/sensor/del', methods=['POST'])
def sensorDel():
    return sensorApi.delSensor(request)


# 修改传感器
@app.route('/sensor/edit', methods=['POST'])
def sensorEdit():
    return sensorApi.editSensor(request)


# 查询传感器 String[deviceId]  不填返回所有
@app.route('/sensor/list', methods=['POST'])
def sensors():
    return sensorApi.getSensors(request)

# 监测数据获取
@app.route('/monitor/list', methods=['POST'])
def monitorList():
    return monitorApi.getMonitors(request)


#设备-传感器级联查询
@app.route('/deviceAndsensor/list', methods=['POST'])
def deviceAndsensorList():
    return deviceApi.getDeviceAndsensorList(request)


#传感器-数据级联查询
@app.route('/sensorAndData/list', methods=['POST'])
def sensorAndDataList():
    return sensorApi.getSensorAndDataList(request)



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=False)
