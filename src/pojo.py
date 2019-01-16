#encoding:utf-8

def _checking(data):
    model=['id','day','checkin','checkout']
    return toList(model,data)

def _email(data):
    model=['time','proto','sip','sport','dip','dport','from','to','subject']
    return toList(model,data)

def _login(data):
    model=['proto','dip','dport','sip','sport','state','time','user']
    return toList(model,data)

def _tcpLog(data):
    model=['stime','dtime','proto','dip','port','sip','sport','uplink_length','downlink_length','lo','la','over_time','over_amount','country','city','category']
    return toList(model,data)

def _weblog(data):
    model=['time','sip','sport','dip','dport','host','type']
    return toList(model,data)

def toList(model,data):
    re=[]
    for i in range(len(data)):
        dict={}
        for j in range(len(model)):
            dict[model[j]]=data[i][j]
        re.append(dict)
    return re