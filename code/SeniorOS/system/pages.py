import gc
from SeniorOS.lib.devlib import *;gc.collect()
import SeniorOS.system.DayLight as DayLight
import SeniorOS.system.core as Core
import SeniorOS.system.ftreader as FTReader
import SeniorOS.system.radient as Radient
import SeniorOS.lib.log_manager as LogManager
import SeniorOS.lib.pages_manager as PagesManager
gc.collect()
import SeniorOS.lib.VirtualRAM as vRAM
import ntptime
import time
import machine
import _thread
ram = vRAM.DiskRam("vram.ram")
ram.SetItem("str","source","http://%s"%Core.Data.Get("text", "radienPluginsSource"))
#source = "http://" + Core.Data.Get("text", "radienPluginsSource")
Log = LogManager.Log
Log.Info("system/pages.mpy")
wifi=wifi()

def EquipmentPanel():
    __import__("SeniorOS.system.HardwareSettings").EquipmentPanel()
    gc.collect()
def ConfigureWLAN(ssid, password):
    logoImg = None
    with open("/SeniorOS/data/SeniorOS.logo",'rb') as f:logoImg = f.read()
    oled.fill(0)
    oled.Bitmap(16,20,logoImg,98,20,1)
    oled.show()
    del logoImg;gc.collect()
    Quit = Core.SharedVar.LoadQuit()
    Quit.value = False
    Quit.text = False
    _thread.start_new_thread(LoadWait,(Quit,Quit,False))
    try:
        if wifi.connectWiFi(ssid, password):
            ntptime.settime(8,"time.windows.com")
            time.sleep(2)
            Quit.value = True
            return True
    except:
        time.sleep(2)
    Quit.value = True
    return False
def WifiPages():
    oled.fill(0)
    wifiNum = DayLight.ListOptions(Core.Data.Get("list", "wifiName"), False, eval("[/Language('请选择配置')/]"))
    oled.show()
    ConfigureWLAN((Core.Data.Get("list", "wifiName")[wifiNum]), (Core.Data.Get("list", "wifiPassword")[wifiNum]))


def CloudNotification():
    time.sleep_ms(int(eval("[/Const('interval')/]")))
    DayLight.App.Style1(eval("[/Language('云端通知')/]"))
    Quit = Core.SharedVar.LoadQuit()
    Quit.value = False
    Quit.text = eval("[/Language('请稍等')/]")
    _thread.start_new_thread(LoadWait, (Quit, Quit, False))
    oled.show()
    try:
        notifications = Radient.Get(ram.GetItem("source") + '/Notifications.sros')[1].split(';')
        Quit.value = True
    except IndexError as e:
        print(e)
        Quit.value = True
        return
    DayLight.App.Style1(eval("[/Language('云端通知')/]"))
    oled.DispChar(notifications[0], 5, 18)
    oled.DispChar(notifications[1], 5, 32)
    oled.DispChar(notifications[2], 5, 45)
    oled.show()
    while not button_a.is_pressed():pass
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
        logoImg = None
        with open("/SeniorOS/data/SeniorOS.logo",'rb') as f:logoImg = f.read()
        oled.Bitmap(16, 15, logoImg, 98, 20, 1)
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

def LoadWait(WhetherToQuit:Core.SharedVar.LoadQuit, text:Core.ShareVar.LoadQuit=False, fill:bool=False):
    if fill:oled.fill(0)
    while not WhetherToQuit:
        if text != False:DayLight.Text(text, DayLight.AutoCenter(text), 28, 2)
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