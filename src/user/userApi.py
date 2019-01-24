# encoding:utf-8
# 外部文件引入
import src.crabapple as crab


# login
def login(req):
    values = req.get_json()
    name = str(values['name'])
    password = str(values['password'])
    try:
        sqlRes = crab.sqlExe(u"SELECT user_id,password FROM user WHERE name='{}'".format(name))
        userId = sqlRes[0][0]
        resPassword = sqlRes[0][1]
        newToken = crab.getRandomStr(userId)
        if resPassword == password:
            crab.sqlExe("UPDATE user SET token=\"{}\" WHERE user_id={}".format(newToken, userId))
            return crab.responsToken(newToken)
        else:
            return crab.responseMsg(1, "Your username or password error!")
    except:
        return crab.responseMsg(1, "Your username or password error!")


# logout
def logout(req):
    token = req.headers["Authorization"]
    userId=crab.checkToken(req)
    if userId==-1:
        return crab.responseMsg(1, "Your token had overtime!")
    try:
        newToken = crab.getRandomStr(userId)
        sqll = "UPDATE user SET token=\"{}\" WHERE token=\"{}\"".format(newToken, token)
        crab.sqlExe(sqll)
        return crab.responseMsg(0, "Logout successfully!")
    except:
        return crab.responseMsg(1, "Logout failure!")


# register
def register(req):
    values = req.get_json()
    name = str(values['name'])
    password = str(values['password'])
    try:
        hasUser = crab.sqlExe("SELECT COUNT(*) FROM user WHERE name=\"{}\"".format(name))
        if hasUser[0][0] != 0:
            return crab.responseMsg(0, "Username has not existence!")
        else:
            crab.sqlExe("INSERT INTO user(name,password) VALUES(\"{}\",\"{}\")".format(name, password))
            return crab.responseMsg(0, "Register Successfully!")
    except:
        return crab.responseMsg(1, "Server exception!")
