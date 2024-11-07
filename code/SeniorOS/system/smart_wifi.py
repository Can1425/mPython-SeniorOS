# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# SmartWifi - by LP_OVER
def main():
    import network
    import socket
    import gc
    import SeniorOS.lib.log_manager as LogManager
    import SeniorOS.system.pages as Pages
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='SeniorOS-WIFI', authmode=4, password='12345678')
    ap.active(True)
    Log = LogManager.lm
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(socket.getaddrinfo("0.0.0.0", 80)[0][-1])
    s.listen(5)
    Log.Info(ap.ifconfig()[0])
    ssid="";pwd=""
    gc.collect()
    while True:
        client_sock, client_addr = s.accept()
        print('Client address:', client_addr)
        returnText=''
        while True:
            h = client_sock.readline()
            returnText += h.decode('utf-8')
            if h == b'' or h == b'\r\n':break
        if returnText.startswith('GET /?ssid='):
            returnText=returnText.split("/")[1]
            returnText=returnText[:-5]
            returnText=returnText.split("=")[1]
            Log.Info("WifiSSID:{}".format(returnText))
            ssid=returnText
            client_sock.write('get')
        elif returnText.startswith('GET /?pwd='):
            returnText=returnText.split("/")[1]
            returnText=returnText[:-5]
            returnText=returnText.split("=")[1]
            Log.Info("WifiPassword:{}".format(returnText))
            pwd=returnText
            client_sock.write('get')
        elif returnText.startswith("GET /exit"):
            Pages.ConfigureWLAN(ssid,pwd)
            del s,ap,client_sock,client_addr,ssid,pwd,returnText,h
            gc.collect()
            return(ssid,pwd)
        client_sock.write("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n")
        client_sock.write('''
                        <!DOCTYPE html>
                        <html lang="zh-cn">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>SeniorOS WiFi Configuration</title>
                            <style>
                                body { font-family: sans-serif; background: #f5f5f7; margin: 0; padding: 100px; color: #333; }
                                .form-container { max-width: 400px; margin: 40px auto; background: #fff; padding: 20px; box-shadow: 0 8px 16px rgba(0,0,0,.2); border-radius: 19px; }
                                input[type="text"], input[type="submit"] { width: calc(100% - 22px); padding: 10px; margin: 10px 0; border: 1px solid #d9d9d9; border-radius: 10px; font-size: 16px; }
                                input[type="submit"] { background: #007aff; color: white; cursor: pointer; }
                                input[type="submit"]:hover { background: #006ae3; }
                                a { display: inline-block; padding: 10px 15px; background: #ff3b30; color: white; text-decoration: none; border-radius: 25px; font-size: 16px; }
                                a:hover { background: #e6332e; }
                            </style>
                        </head>
                        <body>
                            <div class="form-container">
                                <form action="http://192.168.4.1" method="get">
                                    <label for="ssid">WiFi名称</label>
                                    <input type="text" id="ssid" name="ssid" placeholder="输入您的WIFI名称">
                                    <input type="submit" value="上传Wifi名称">
                                </form>
                                <form action="http://192.168.4.1" method="get">
                                    <label for="pwd">Wifi密码</label>
                                    <input type="text" id="pwd" name="pwd" placeholder="输入您的WiFi密码">
                                    <input type="submit" value="上传WiFi密码">
                                </form>
                                <a href="http://192.168.4.1/exit">退出并连接</a>
                            </div>
                        </body>
                        </html>
                        ''')
        client_sock.close()