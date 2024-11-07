# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# radient.py - by LP_OVER
import socket
import gc
def GetToFile(url,file,timeout=2,bufferSize=1024):#此处file是对象
    if not url.startswith("http://"):url = "http://" + url
    print("访问:"+url)
    url_parse = url.split('/')
    print("目标"+url_parse[2])
    host = url_parse[2]
    path = '/'
    if len(url_parse) > 3:
        path = '/' + '/'.join(url_parse[3:])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))
    s.settimeout(timeout)
    s.send(('GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(path, host)).encode())
    StatusCode = ""
    while True:
        gc.collect()
        try:data = s.recv(bufferSize)
        except:break
        if StatusCode != "200":
            StatusCode = data.decode().split('\r\n')[0].split(' ')[1]
            try:file.write(data.decode().split("\r\n\r\n")[1])
            except:pass
        elif StatusCode == "200":file.write(data.decode())
        elif StatusCode != "" and len(StatusCode) > 0:
            raise CodeError("status_code is {}".format(StatusCode))
        del data
    s.close()
    

def NormalGet(url,timeout=2):
    #解析url
    print("访问:"+url)
    url_parse = url.split('/')
    print("目标"+url_parse[2])
    host = url_parse[2]
    path = '/'
    if len(url_parse) > 3:path = '/' + '/'.join(url_parse[3:])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))
    s.settimeout(timeout)
    s.send(('GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(path, host)).encode())
    response = b''
    while True:
        try:data = s.recv(1024)
        except:break
        if data == b"" and len(response)>0:break
        response += data
    s.close()
    return response.decode()

def ParseResponse(response):
    response_parse = response.split('\r\n\r\n')
    headers = response_parse[0].split('\r\n')
    status_line = headers[0].split(' ')
    status_code = status_line[1]
    body = response_parse[1]
    return status_code, body
def Get(url, timeout=2):
    response = NormalGet(url, timeout)
    status_code, body = ParseResponse(response)
    if status_code == "308" or status_code == "301" or status_code == "302":print("重定向找我干嘛")
    else:OSError("status_code is {}".format(status_code))
    return status_code, body
    # [0]是状态码 , [1]是响应体 , 建议放变量里面
