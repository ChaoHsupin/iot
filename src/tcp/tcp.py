# coding=utf-8
# from socket import *
import json
import socket
from threading import Thread
import time

import src.crabapple as crab


def tcpServer():
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 重复使用绑定信息,不必等待2MSL时间
    tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('', 93)
    tcpSocket.bind(address)
    tcpSocket.listen(5)

    try:
        while True:
            time.sleep(0.01)
            print('接受tcp数据开启等待')
            newData, newAddr = tcpSocket.accept()
            print('%s客户端已经连接，准备处理数据' % newAddr[0])
            p = Thread(target=recv, args=(newData, newAddr))
            p.start()
    finally:
        tcpSocket.close()


def recv(newData, newAddr):
    device_id=-1
    user_id=-1
    while True:
        recvData = newData.recv(1024)
        if len(recvData) > 0:
            recvData = str(recvData)
            receveInfo = json.loads(recvData[2:len(recvData) - 4])
            method=receveInfo['method']
            if method=='update':
                try:
                    device_id=int(receveInfo['gatewayNo'])
                    user_id=int(receveInfo['userkey'])
                    re=crab.sqlExe("SELECT COUNT(*) FROM user a,device b WHERE"
                                   " a.user_id=b.user_id AND a.user_id={} AND b.device_id={}".format(user_id,device_id))
                    if int(re[0][0]) ==1:
                        newData.send('OK'.encode('utf-8'))
                    else:
                        device_id = -1
                        user_id = -1
                        continue
                except:
                    device_id = -1
                    user_id = -1
                    continue
            elif method=='upload':
                if device_id==-1 or user_id==-1:
                    continue
                try:
                    recvData = receveInfo['data']
                    for i in recvData:
                        crab.sqlExe(
                            "INSERT INTO monitor(device_id,identification,value) values (\"{}\",\"{}\",{})".format(device_id,i['Name'], i['Value']))
                    print(recvData)
                    newData.send('upload OK'.encode('utf-8'))
                except:
                    continue
            elif method=='getcear':
                if device_id==-1 or user_id==-1:
                    continue
                try:
                    re=crab.sqlExe("SELECT b.value FROM device a,vpt b WHERE a.vpt_id=b.vpt_id AND a.device_id={}".format(device_id))
                    newData.send(str(re[0][0]).encode('utf-8'))
                except:
                    continue

        else:
            print('%s客户端已经关闭' % newAddr[0])
            break
    newData.close()


# 获取当前用户传感器不同档位值
def getRank(req):
    userId = crab.checkToken(req)
    if userId == -1:
        return crab.responseMsg(0, "Your identity is not identified!")
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect(('tcp.lewei50.com', 9960))
    tcp_client.send('{"method": "update","gatewayNo": "02","userkey": "{}"}&^!'.format(userId).encode('utf-8'))
    recv_data = tcp_client.recv(1024)
    resStr = recv_data.decode('utf-8')
    try:
        resStr = json.loads(resStr[0:len(resStr) - 4])
        if resStr['p1'] == 'ok':
            tcp_client.send('{"method":"getcear"}&^!'.encode('utf-8'))
            recv_data = tcp_client.recv(1024)
            resStr = recv_data.decode('utf-8')
            return crab.responseDate(0, resStr)
    except:
        return crab.responseMsg(1, 'had exception')
    finally:
        tcp_client.close()
