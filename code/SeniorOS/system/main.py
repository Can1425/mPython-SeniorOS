import gc
import SeniorOS.lib.log_manager as LogManager
Log = LogManager.Log
LogManager.Output("system/main.mpy", "INFO")
import os;os.chdir('/')
import SeniorOS.system.core as Core;gc.collect()
from SeniorOS.lib.devlib import wifi;gc.collect()
import SeniorOS.system.pages as Pages
info=Core.Data.Get("text","connectWifiMode")
wifilist=[]
if info == 0:
    Pages.WifiPages()
elif info == 1:
    wifilist=[Core.Data.Get("list","wifiName"),Core.Data.Get("list","wifiPassword")]
    net=wifi()
    net.sta.active(True)
    netscan=net.sta.scan()
    GetWifiCfg=lambda num: str(netscan[num][0].decode('utf-8')).replace("\r","")
    connect=False
    for i in wifilist[0]:
        for j in range(len(netscan)):
            if connect:break
            if str(i)==GetWifiCfg(j):
                try:
                    net.connectWiFi(wifilist[0][i],wifilist[1][i])
                    import ntptime
                    ntptime.settime(8,"time.windows.com")
                    del ntptime;gc.collect()
                    connect=True
                except:
                    Log.Error("连接WiFi失败")
                    Log.Message("请使用浏览器打开https://ys.mihoyo.com/进行求助")
    del wifilist,net,netscan,connect
    gc.collect()
elif info == 2:
    import SeniorOS.system.smart_wifi as SmartWifi
    SmartWifi.main()
del info;gc.collect()
#-----------------
while True:Pages.Home()#注：Pages.Home实际上没有任何返回数据，直接循环即可
#returnData=Pages.Home()
#while not returnData:
#    returnData=Pages.Home()