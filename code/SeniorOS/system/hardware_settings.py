from SeniorOS.lib.devlib import *
import SeniorOS.system.daylight as DayLight
import SeniorOS.system.pages as Pages
import machine
import os,gc
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
        if eval("[/GetButtonExpr('python')/]"):Pages.Collect()
    return 0
def HS_Flash():
    fileSystemFree=os.statvfs("/")[3] * os.statvfs("/")[1]
    oled.fill(0)
    oled.DispChar("Flash - total: 8MB",5,0)
    oled.DispChar("可用:{} MB".format(fileSystemFree/81920),5,16)
    DayLight.ProgressBoxMove(5,32,100,10,((100 - 0) / (8 - 0)) * ((fileSystemFree / 81920) - 0) + 0)
    oled.show()
    while True:
        if button_a.is_pressed():return 0
def PeripheralPanel():
    PeripheralPin = ["Pin.P0","Pin.P1","Pin.P2","Pin.P3","Pin.P13","Pin.P14","Pin.P15","Pin.P16"]
    while not button_a.is_pressed():
            options = DayLight.Select.Style4(PeripheralPin, False, "选择引脚")
            if options!=None:
                DayLight.VastSea.Transition() 
                selsetPin=PeripheralPin[options]
            else: break
            SS=DayLight.Select.Style4(["输出","输入"], False, "选择模式")
            if SS == 0:
                while not button_a.is_pressed():
                    oled.fill(0)
                    oled.DispChar("引脚 {} 的值为".format(selsetPin),5,0)
                    PIN=eval("Pin({},Pin.IN)".format(selsetPin))
                    oled.DispChar(str(PIN.value()),5,16)
                    oled.show()
                break
            elif SS == 1:
                while not button_a.is_pressed():
                    val=DayLight.Select.Style4(["高","低"], False, "选择{}电平".format(selsetPin))
                    if val != None:
                        DayLight.VastSea.Transition()
                        PIN=eval("Pin({},Pin.OUT)".format(selsetPin))
                        if val == 0:PIN.on()
                        else:PIN.off()
                    else:break
    DayLight.VastSea.Transition(False)
    return

def EquipmentPanel():
    ListOperation = {
    0: HS_CPU,
    1: HS_Ram,
    2: HS_Flash,
    3: PeripheralPanel
    }
    hardwareOptions=["CPU","RAM","Flash","外设控制"]
    while not button_a.is_pressed():
        options = DayLight.Select.Style4(hardwareOptions, False, "设备面板")
        if options != None:
            DayLight.VastSea.Transition()
            ListOperation.get(options)()
            DayLight.VastSea.Transition(False)
        else:
            return