import gc
import SeniorOS.system.daylight as DayLight;gc.collect()
import SeniorOS.system.core as Core
import SeniorOS.system.ftreader as FTReader
import SeniorOS.system.radient as Radient ;gc.collect()
import ntptime
from SeniorOS.lib.devlib import *;gc.collect()
import time
import machine
import SeniorOS.lib.log_manager as LogManager
import SeniorOS.lib.pages_manager as PagesManager;gc.collect()
import _thread
import os;gc.collect()

source = "http://" + Core.Data.Get("text", "radienPluginsSource")
Log = LogManager.Log
Log.Info("system/pages.mpy")
wifi=wifi()

def ConfigureWLAN(ssid, password):
    oled.fill(0)
    oled.Bitmap(16, 20, bytearray([0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00, 0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X3C,0X00,0X00,0X00,0X30, 0X00,0X00,0X00,0X70,0X00,0X78,0X00,0X03,0XFE,0X00,0X00,0X00,0X70,0X00,0X00,0X03, 0XFE,0X03,0XFE,0X00,0X07,0XFC,0X00,0X00,0X00,0X30,0X00,0X00,0X07,0X8F,0X07,0XFE, 0X00,0X06,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X0E,0X03,0X86,0X00,0X00,0X06,0X00, 0X0E,0X03,0XE0,0X20,0X38,0X01,0X8C,0X01,0X8E,0X00,0X00,0X0E,0X00,0X3F,0X87,0XF8, 0X71,0XFE,0X0F,0X98,0X00,0XCE,0X00,0X00,0X0F,0X00,0X7B,0XC7,0XFC,0X71,0XFF,0X1F, 0X98,0X00,0XCE,0X00,0X00,0X07,0XF0,0X60,0XCE,0X0C,0X63,0X83,0X18,0X18,0X00,0XC7, 0XF0,0X00,0X03,0XFC,0XE0,0XCE,0X0C,0X63,0X03,0X38,0X18,0X00,0XC3,0XFC,0X00,0X00, 0X1C,0XFF,0XCE,0X0C,0X63,0X03,0X38,0X18,0X00,0XC0,0X1C,0X00,0X00,0X0C,0XFF,0XCC, 0X0C,0X67,0X03,0X30,0X18,0X00,0XC0,0X0C,0X00,0X00,0X0C,0XC0,0X0C,0X0C,0X67,0X03, 0X30,0X0C,0X01,0XC0,0X0C,0X00,0X00,0X1C,0XC0,0X0C,0X1C,0XE7,0X07,0X30,0X0E,0X03, 0X80,0X1C,0X00,0X00,0X3C,0XE0,0X0C,0X1C,0XE7,0X8E,0X30,0X07,0X8F,0X00,0X3C,0X00, 0X1F,0XF8,0X7F,0X8C,0X1C,0XE3,0XFE,0X30,0X03,0XFE,0X1F,0XF8,0X00,0X1F,0XE0,0X3F, 0X8C,0X18,0XC1,0XF8,0X30,0X00,0XF8,0X1F,0XE0,0X00,0X00,0X00,0X00,0X00,0X00,0X00, 0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00, 0X00,0X00,0X00,0X00,]), 98, 20, 1)
    oled.show()
    Quit = Core.SharedVar.LoadQuit()
    Quit.value = False
    _thread.start_new_thread(LoadWait,(Quit,"None",False))
    try:
        if wifi.connectWiFi(ssid, password):
            ntptime.settime(8,"time.windows.com")
            time.sleep(2)
            Quit.value = True
            return True
        else:
            Quit.value = True
            return False
    except: 
        time.sleep(2)
        Quit.value = True
        return False

def WifiPages():
    DayLight.VastSea.Off()
    wifiNum = DayLight.ListOptions(Core.Data.Get("list", "wifiName"), False, eval("[/Language('请选择配置')/]"))
    oled.show()
    ConfigureWLAN((Core.Data.Get("list", "wifiName")[wifiNum]), (Core.Data.Get("list", "wifiPassword")[wifiNum]))


def CloudNotification():
    time.sleep_ms(int(eval("[/Const('interval')/]")))
    DayLight.App.Style1(eval("[/Language('云端通知')/]"))
    Quit = Core.SharedVar.LoadQuit()
    Quit.value = False
    _thread.start_new_thread(LoadWait, (Quit, eval("[/Language('请稍等')/]"), False))
    oled.show()
    try:
        notifications = Radient.Get(source + '/Notifications.sros')[1].split(';')
        print(notifications)
    except IndexError as e:
        Quit.value = True
        print(e)
        return
    Quit.value = True
    DayLight.App.Style1(eval("[/Language('云端通知')/]"))
    oled.DispChar(notifications[0], 5, 18)
    oled.DispChar(notifications[1], 5, 32)
    oled.DispChar(notifications[2], 5, 45)
    oled.show()
    while not button_a.is_pressed():pass
    del notifications
    return

def HS_CPU():
    oled.fill(0)
    oled.DispChar("目前频率:{} MHZ".format(str(machine.freq()/1000000)),0,16)
    oled.DispChar("MPU - ESP32",0,0)
    oled.show()
    while True:
        if button_a.is_pressed():return
def HS_Ram():
    while not button_a.is_pressed():
        oled.fill(0)
        oled.DispChar("Ram - total:520kb",0,0)
        oled.DispChar(f"内存可用:{str(gc.mem_free())} Bytes",0,16)
        oled.DispChar("触摸键释放内存",0,32)
        oled.show()
        if eval("[/GetButtonExpr('python')/]"):Collect()
    return 0
def HS_Flash():
    fileSystemFree=os.statvfs("/")[3] * os.statvfs("/")[1]
    oled.fill(0)
    oled.DispChar("Flash - total: 8MB",5,0)
    oled.DispChar("可用:{} MB".format(fileSystemFree/81920),5,16)
    DayLight.ProgressBoxMove(5,32,100,10,((100 - 0) / (8 - 0)) * ((fileSystemFree / 81920) - 0) + 0)
    oled.show()
    while not button_a.is_pressed():
        if button_a.is_pressed():
            del fileSystemFree
            gc.collect()    
            return 0
def PeripheralPanel():
    PeripheralList = ["引脚控制"]
    PeripheralPin = ["Pin.P0","Pin.P1","Pin.P2","Pin.P3","Pin.P13","Pin.P14","Pin.P15","Pin.P16"]
    while not button_a.is_pressed():
        options = DayLight.Select.Style4(PeripheralList, False, "控制面板")
        if options == 0:
            DayLight.VastSea.Transition() 
            options = DayLight.Select.Style4(PeripheralPin, False, "选择引脚")
            if options!=None:
                DayLight.VastSea.Transition() 
                selsetPin=PeripheralPin[options]
            else: 
                DayLight.VastSea.Transition(False)
                return
            SS=DayLight.Select.Style4(["输出","输入"], False, "选择模式")
            if SS == 0:
                while not button_a.is_pressed():
                    oled.fill(0)
                    oled.DispChar("引脚 {} 的值为".format(selsetPin),5,0)
                    PIN=eval("Pin({},Pin.IN)".format(selsetPin))
                    oled.DispChar(str(PIN.value()),5,16)
                    oled.show()
                DayLight.VastSea.Transition(False)
                return
            elif SS == 1:
                while not button_a.is_pressed():
                    val=DayLight.Select.Style4(["高","低"], False, "选择{}电平".format(selsetPin))
                    if val != None:
                        DayLight.VastSea.Transition()
                        PIN=eval("Pin({},Pin.OUT)".format(selsetPin))
                        if val == 0:PIN.on()
                        else:PIN.off()
                    else:
                        DayLight.VastSea.Transition(False)
                        return
                return 
        else:
            DayLight.VastSea.Transition(False)
            return

def EquipmentPanel():
    ListOperation = {
    0: HS_CPU,
    1: HS_Ram,
    2: HS_Flash,
    3: PeripheralPanel
    }
    hardware=["CPU","RAM","Flash","外设控制"]
    while not button_a.is_pressed():
        options = DayLight.Select.Style4(hardware, False, "设备面板")
        if options != None:
            DayLight.VastSea.Transition()
            ListOperation.get(options)()
            DayLight.VastSea.Transition(False)
        else:
            return
        
def Home():
    oled.fill(0)
    time.sleep_ms(int(eval("[/Const('interval')/]")))
    while not eval("[/GetButtonExpr('thab')/]"):
        PagesManager.Main.Import('SeniorOS.style.home', 'Style{}'.format(Core.Data.Get("text", "homeStyleNum")), False)
        if button_a.is_pressed():
            DayLight.VastSea.SeniorMove.Text(eval("[/Language('云端通知')/]"),-10,-20,5,0)
            PagesManager.Main.Import("SeniorOS.system.pages", "CloudNotification")
            DayLight.VastSea.SeniorMove.Text(eval("[/Language('云端通知')/]"),5,0,-10,-20)
            break
        elif button_b.is_pressed():
            DayLight.VastSea.SeniorMove.Text(eval("[/Language('设备面板')/]"),138,-20,5,0)
            PagesManager.Main.Import("SeniorOS.system.pages", "EquipmentPanel")
            DayLight.VastSea.SeniorMove.Text(eval("[/Language('设备面板')/]"),5,0,138,-20)
            break
        elif eval("[/GetButtonExpr('py')/]"):
            PagesManager.Main.Import('SeniorOS.style.home', 'IsPYTouth')
        elif eval("[/GetButtonExpr('on')/]"):
            PagesManager.Main.Import('SeniorOS.style.home', 'IsONTouth')
        elif eval("[/GetButtonExpr('th')/]"):
            DayLight.VastSea.SeniorMove.Line(128, 0, 0, 0, 0, 46, 128, 46)
            PagesManager.Main.Import("SeniorOS.apps.port", "App")
            DayLight.VastSea.SeniorMove.Line(0, 46, 128, 46, 128, 0, 0, 0)
            break

def HomeomePlugInSet():
    while not button_a.is_pressed():
        options = DayLight.Select.Style4(["快捷启动1", "快捷启动2"], False, "桌面快捷启动")
        if options != None:
            DayLight.VastSea.Transition()
            set = DayLight.Select.Style1(Core.Data.Get("list", "localAppName"), 25, False, "选择")
            if set != None:
                Core.Data.Write("list", "homePlugIn", "app{}".format(str(set)), options)
                Message('好耶，设置成功')
                return True
            else:
                DayLight.VastSea.Transition(False)

def About():
    oled.fill(0)
    while not button_a.is_pressed():
        oled.Bitmap(16, 15, bytearray([0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00, 0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X3C,0X00,0X00,0X00,0X30, 0X00,0X00,0X00,0X70,0X00,0X78,0X00,0X03,0XFE,0X00,0X00,0X00,0X70,0X00,0X00,0X03, 0XFE,0X03,0XFE,0X00,0X07,0XFC,0X00,0X00,0X00,0X30,0X00,0X00,0X07,0X8F,0X07,0XFE, 0X00,0X06,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X0E,0X03,0X86,0X00,0X00,0X06,0X00, 0X0E,0X03,0XE0,0X20,0X38,0X01,0X8C,0X01,0X8E,0X00,0X00,0X0E,0X00,0X3F,0X87,0XF8, 0X71,0XFE,0X0F,0X98,0X00,0XCE,0X00,0X00,0X0F,0X00,0X7B,0XC7,0XFC,0X71,0XFF,0X1F, 0X98,0X00,0XCE,0X00,0X00,0X07,0XF0,0X60,0XCE,0X0C,0X63,0X83,0X18,0X18,0X00,0XC7, 0XF0,0X00,0X03,0XFC,0XE0,0XCE,0X0C,0X63,0X03,0X38,0X18,0X00,0XC3,0XFC,0X00,0X00, 0X1C,0XFF,0XCE,0X0C,0X63,0X03,0X38,0X18,0X00,0XC0,0X1C,0X00,0X00,0X0C,0XFF,0XCC, 0X0C,0X67,0X03,0X30,0X18,0X00,0XC0,0X0C,0X00,0X00,0X0C,0XC0,0X0C,0X0C,0X67,0X03, 0X30,0X0C,0X01,0XC0,0X0C,0X00,0X00,0X1C,0XC0,0X0C,0X1C,0XE7,0X07,0X30,0X0E,0X03, 0X80,0X1C,0X00,0X00,0X3C,0XE0,0X0C,0X1C,0XE7,0X8E,0X30,0X07,0X8F,0X00,0X3C,0X00, 0X1F,0XF8,0X7F,0X8C,0X1C,0XE3,0XFE,0X30,0X03,0XFE,0X1F,0XF8,0X00,0X1F,0XE0,0X3F, 0X8C,0X18,0XC1,0XF8,0X30,0X00,0XF8,0X1F,0XE0,0X00,0X00,0X00,0X00,0X00,0X00,0X00, 0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00, 0X00,0X00,0X00,0X00,]), 98, 20, 1)
        version = 'V' + eval("[/Const('version')/]")
        DayLight.Text(version, DayLight.AutoCenter(version), 40, 2)
        oled.show()
        if eval("[/GetButtonExpr('on')/]"):
            DayLight.VastSea.Transition()
            FTReader.Textreader(Core.Data.GetOriginal('Hello_World')).Main()
            DayLight.VastSea.Transition(False)

Wlanscan = lambda: [i[0].decode() for i in wifi().sta.scan()]

def Choosewifi() -> bool:
    while not button_a.is_pressed():
        oled.fill(0)
        wifiList = Wlanscan()
        num = DayLight.Select.Style4(wifiList, False, "请选择")
        if num == None:
            DayLight.VastSea.Transition(False)
            return
        wifiName = wifiList[num]
        import SeniorOS.system.typer as Typer
        wifiPassword = Typer.main()
        del Typer;gc.collect()
        Quit = Core.SharedVar.LoadQuit()
        Quit.value = False
        _thread.start_new_thread(LoadWait,(Quit, "正在尝试建立连接", True))
        try:
            wifi.connectWiFi(wifiName, wifiPassword)
            Core.Data.Write('list', 'wifiName', wifiName)
            Core.Data.Write('list', 'wifiPassword', wifiPassword)
            Quit.value = True
            Message('好耶，添加成功')
            return True
        except:
            Quit.value = True
            Message('添加失败')
            return False

def WaitMod(func):
    oled.fill(0)
    DayLight.UITools()
    try:
        oled.DispChar(eval("[/Language('请稍等')/]"), 5, 5, 1)
        oled.DispChar(eval("[/Language('正在进行操作')/]"), 5, 18, 1)
        oled.show()
        eval("func",{"func":func})
        oled.DispChar(eval("[/Language('加载成功')/]"), 5, 45, 1)
        oled.show()
        time.sleep(1)
        return True
    except:
        oled.DispChar(eval("[/Language('加载失败')/]"), 5, 45, 1)
        oled.show()
        time.sleep(1)
        return False
def Collect():WaitMod("Core.FullCollect()")
def Time():WaitMod("""ntptime.settime(8, Core.Data.Get("text", "timingServer"))""")

def ConnectWiFiMode():
    mode = ['预配置选择','自动连接预配置','SmartWiFi']
    oled.fill(0)
    while not button_a.is_pressed():
        options = DayLight.Select.Style4(mode, False, '网络连接方式')
        if options != None:
            Core.Data.Write('text', 'connectWifiMode', options)
            Message('好耶，设置成功')
        else:
            DayLight.VastSea.Transition(False)
            return

def LoadWait(WhetherToQuit:Core.SharedVar.LoadQuit, text:str="None", fill:bool=False):
    if fill:oled.fill(0)
    while not WhetherToQuit:
        if text != "None":DayLight.Text(text, DayLight.AutoCenter(text), 28, 2)
        DayLight.VastSea.SeniorMove.Line(0,63,0,63,0,63,128,63,False)
        DayLight.VastSea.SeniorMove.Line(0,63,128,63,128,63,128,63,False)
        oled.show()
    oled.fill(0)

def Message(text, center=False) -> bool:
    DayLight.Box(1, 1, 126, 62, True)
    oled.DispChar('消息', DayLight.AutoCenter('消息'), 5)
    DayLight.Text(text, (DayLight.AutoCenter(text) if center else 8), 26, 2)
    Log.Message(text)
    oled.show()
    time.sleep(3)
    return True
def ShutDown():
    options = DayLight.Select.Style4(['关机','重启','睡眠','取消'], False, '电源设置')
    if options == 0:
        oled.poweroff()
        machine.deepsleep()
    elif options == 1:machine.reset()
    elif options == 2:
        import esp32
        oled.poweroff()
        esp32.wake_on_touch(True)
        print("[INFO] Sleep now")
        time.sleep_ms(100)
        machine.lightsleep()
    else:
        return
def WiFiConfig():
    IP,netmask,gateway,DNS = wifi.sta.ifconfig()
    FTReader.Textreader('是否连接: ' + "是" if wifi.sta.isconnected() else "否" + "\n" + "状态码: "  + str(wifi.sta.status()) + '\n' + 'IP: ' + IP +'\n' + 'Netmask: ' + netmask + '\n' + 'DNS: ' + DNS + '\n' + 'Gateway: ' + gateway).Main()

def DeviceID():
    oled.fill(0)
    DayLight.App.Style1('设备标识符')
    DayLight.Text('ID1 {}'.format(Core.GetDeviceID(mode=0)), 5, 16, 1)
    DayLight.Text('ID2 {}'.format(Core.GetDeviceID(mode=1)), 5, 32, 1)
    oled.show()
    while not button_a.is_pressed():pass