# encoding:utf-8
# 外部文件引入
import src.crabapple as crab


# add vpt
def addVpt(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    try:
        sql = "INSERT INTO vpt(plants_name,value) VALUES(\"{}\",\"{}\")".format(values['plants_name'],values['value'])
        crab.sqlExe(sql)
        return crab.responseMsg(0, "Add vpt successfully!")
    except:
        return crab.responseDate(1, "Add vpt missing field,pleass cheking!")


# del vpt
def delVpt(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    vpt_id = int(values['vpt_id'])
    try:
        crab.sqlExe("DELETE FROM vpt WHERE vpt_id={}".format(vpt_id))
        return crab.responseMsg(0, "Delete vpt information successfully")
    except:
        return crab.responseMsg(1, "Delete vpt information failure!")


# edit vpt
def editVpt(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    values = req.get_json()
    vpt_id = values['vpt_id']
    res = vptPojo(crab.sqlExe("SELECT * FROM vpt WHERE vpt_id=\"{}\"".format(vpt_id)))
    if len(res) == 0:
        return crab.responseMsg(1, "Have not this vptId!")
    else:
        try:
            res = res[0]
            for i in values:
                res[i] = values[i]
            sql = "UPDATE vpt SET  plants_name=\"{}\", value=\"{}\" WHERE " \
                  "vpt_id={}".format(res['plants_name'],res['value'], vpt_id)
            crab.sqlExe(sql)
            return crab.responseMsg(0, "Edit vpt information successfully!")
        except:
            return crab.responseMsg(1, "Edit vpt information failure!")


# vpt
def getVpts(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    sql = "SELECT * FROM vpt"
    try:
        values = req.get_json()
        sql += (" WHERE" + crab.getByConditions(values))
    except:
        sql = sql
    try:
        res = vptPojo(crab.sqlExe(sql))
        return crab.responseDate(0, res)
    except:
        return crab.responseMsg(1, "Get vpt information failure!")

def vptPojo(data):
    pojoModel = ['vpt_id', 'plants_name','value']
    return crab.toList(pojoModel, data)

