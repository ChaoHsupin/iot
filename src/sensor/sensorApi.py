# encoding:utf-8
# 外部文件引入
import src.crabapple as crab


# add sensor
def addSensor(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    try:
        sql = "INSERT INTO sensor(device_id,identification,sensor_name,sensor_type,unit,value_max,value_min," \
              "is_warn,sort) VALUES(" \
              "{},\"{}\",\"{}\",\"{}\",\"{}\",{},{},{},{})".format(values['device_id'], values['identification'],
                                                                   values['sensor_name'], values['sensor_type'],
                                                                   values['unit'], values['value_max'],
                                                                   values['value_min'], values['is_warn'],
                                                                   values['sort'])
        crab.sqlExe(sql)
        return crab.responseMsg(0, "Add sensor successfully!")
    except:
        return crab.responseDate(1, "Add sensor missing field,pleass cheking!")


# del sensor
def delSensor(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    sensor_id = int(values['sensor_id'])
    try:
        crab.sqlExe("DELETE FROM sensor WHERE sensor_id={}".format(sensor_id))
        return crab.responseMsg(0, "Delete sensor information successfully")
    except:
        return crab.responseMsg(1, "Delete sensor information failure!")


# edit sensor
def editSensor(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    sensor_id = values['sensor_id']
    res = sensorPojo(crab.sqlExe("SELECT * FROM sensor WHERE sensor_id=\"{}\"".format(sensor_id)))
    if len(res) == 0:
        return crab.responseMsg(1, "Have not this sensorId!")
    else:
        try:
            res = res[0]
            for i in values:
                res[i] = values[i]
            sql = "UPDATE sensor SET device_id={}, identification=\"{}\", sensor_name=\"{}\", sensor_type=\"{}\"," \
                  " unit=\"{}\",value_max={},value_min={},is_warn={},sort={} WHERE " \
                  "sensor_id={}".format(res['device_id'], res['identification'],
                                        res['sensor_name'], res['sensor_type'], res['unit'], res['value_max'],
                                        res['value_min'], res['is_warn'], res['sort'], sensor_id)
            crab.sqlExe(sql)
            return crab.responseMsg(0, "Edit sensor information successfully!")
        except:
            return crab.responseMsg(1, "Edit sensor information failure!")


# sensor
def getSensors(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    sql = "SELECT * FROM sensor"
    try:
        values = req.get_json()
        sql += (" WHERE" + crab.getByConditions(values))
    except:
        sql = sql
    try:
        res = sensorPojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get sensor information failure!")


# 传感器数据级联
def getSensorAndDataList(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    sql = "SELECT * FROM sensor,monitor WHERE sensor.identification=monitor.identification"
    try:
        values = req.get_json()
        sql += crab.getByConditions(values)
    except:
        sql = sql
    try:
        res = sensorDataPojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get sensor and data information failure!")


def sensorPojo(data):
    pojoModel = ['sensor_id', 'device_id', 'identification', 'sensor_name', 'sensor_type', 'unit', 'value_max',
                 'value_min', 'is_warn', 'sort']
    return crab.toList(pojoModel, data)


def sensorDataPojo(data):
    pojoModel = ['sensor_id', 'device_id', 'identification', 'sensor_name', 'sensor_type', 'unit', 'value_max',
                 'value_min', 'is_warn', 'sort', 'monitor_id', 'sensor_id', 'value', 'create_time']
    return crab.toList(pojoModel, data)
