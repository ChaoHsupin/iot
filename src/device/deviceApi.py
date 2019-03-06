# encoding:utf-8
# 外部文件引入

import src.crabapple as crab


# add device
def addDevice(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    try:
        sql = "INSERT INTO device(device_name,device_type,place,is_control,is_public,user_id) VALUES(" \
              "\"{}\",\"{}\",\"{}\",{},{},{})".format(values['device_name'], values['device_type'], values['place'],
                                                      values['is_control'], values['is_public'], userId, )
        crab.sqlExe(sql)
        return crab.responseMsg(0, "Add device successfully!")
    except:
        return crab.responseDate(1, "Add device missing field,pleass cheking!")


# del device
def delDevice(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    device_id = int(values['device_id'])
    try:
        crab.sqlExe("DELETE FROM device WHERE device_id={}".format(device_id))
        return crab.responseMsg(0, "Delete device information successfully")
    except:
        return crab.responseMsg(1, "Delete device information failure!")


# edit device
def editDevice(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    device_id = values['device_id']
    res = devicePojo(crab.sqlExe("SELECT * FROM device WHERE device_id=\"{}\"".format(device_id)))
    if len(res) == 0:
        return crab.responseMsg(1, "Hava not this deviceId!")
    else:
        try:
            res = res[0]
            for i in values:
                res[i] = values[i]
            sql = "UPDATE device SET device_name=\"{}\", device_type=\"{}\", place=\"{}\", is_control={}, is_public={}, vpt_id={} WHERE " \
                  "device_id={}".format(res['device_name'], res['device_type'], res['place'], res['is_control'],
                                        res['is_public'],res['vpt_id'], res['device_id'])
            crab.sqlExe(sql)
            return crab.responseMsg(0, "Edit device information successfully!")
        except:
            return crab.responseMsg(1, "Edit device information failure!")


# list device
def getDevices(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    sql = "SELECT * FROM device"
    try:
        values = req.get_json()
        sql += (" WHERE" + crab.getByConditions(values))
    except:
        sql = sql
    try:
        res = devicePojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get device information failure!")


# current user's device
def getCurrentDevices(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    try:
        sql = "SELECT * FROM device WHERE user_id={}".format(crab.getUserId())
        res = devicePojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get device information failure!")


# 设备传感器级联
def getDeviceAndsensorList(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    sql = "SELECT * FROM device,sensor WHERE device.device_id=sensor.device_id"
    try:
        values = req.get_json()
        sql += crab.getByConditions(values)
    except:
        sql = sql
    try:
        res = deviceSensorPojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get device information failure!")


def devicePojo(data):
    pojoModel = ['device_id', 'device_name', 'device_type', 'place', 'is_control', 'is_public', 'user_id','vpt_id']
    return crab.toList(pojoModel, data)


def deviceSensorPojo(data):
    pojoModel = ['device_id', 'device_name', 'device_type', 'place', 'is_control', 'is_public', 'user_id','vpt_id',
                 'sensor_id', 'device_id', 'identification', 'sensor_name', 'sensor_type', 'unit', 'value_max',
                 'value_min', 'is_warn', 'sort']
    return crab.toList(pojoModel, data)
