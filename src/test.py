# encoding:utf-8
# for i in range(5):
#     print(i)
import csv
import json
import time
import re

# file=open("met.csv",mode='r',encoding='utf-8-sig')
# data=csv.reader(file)
# he=next(data)
# for d in data:
#     # print(d)
#     print (u"update weblog set type='{}' where host like concat('%{}%');".format(d[1],d[0]))
#


#
# str=re.findall(u'\.\w+\.',"www.jd.com")
# print(str)
# print(str[0][1:len(str[0])-1])

# text=str(sorted({'a':1,'c':4}.items(), key=lambda x: x[1], reverse=True))
# print(text)
#
# elecShop = text.replace('[(','{').replace(')]','}').replace('\',','\':').replace('(','').replace(')','')
# print(elecShop)
# dict=eval(elecShop)
# print(dict)


#
# def tur_convert_list(data):
#     return data.replace("((","").replace(",))","").replace("(","").replace(",)","").replace("\'","")
# data=str((('电商',), ('邮箱',), ('科技',), ('直播',), ('办公',)))
#
#
# print(tur_convert_list(data).strip(',').split(','))

import pymysql
from DBUtils.PooledDB import PooledDB

# from random import sample
# def getRandomStr():
#     Num = [i for i in range(36)]
#     for i in range(10):
#         Num[i] = chr(i + ord('0'))
#     for i in range(26):
#         Num[10 + i] = chr(i + ord('A'))
#     print(''.join(sample(Num, 10)))
#
#
# print("ddddd{}{}{}{}{}".format(1,2,3,4,5))

def getByConditions(conList):
    length=len(conList)
    if length==0:
        return ""
    else:
        index=1
        sql=" WHERE"
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

print(getByConditions({'a':1,'b':2,'begin_time':12321}))
print(getByConditions({'a':1,'b':2,'begin_time':12321,'end_time':7867}))