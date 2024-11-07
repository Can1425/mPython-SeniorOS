import SeniorOS.system.core as Core
import math
import gc
import time
from SeniorOS.lib.devlib import *
import SeniorOS.lib.log_manager as LogManager
import SeniorOS.lib.pages_manager as PagesManager
from SeniorOS.system.ftreader import Animations
import framebuf
LogManager.Output("system/daylight.mpy", "INFO")

# 缓存时间相关的字符串
def UITime(pages=True):
    h = str(Core.GetTime.Hour())
    m = str(Core.GetTime.Min())
    return ('0%s'%(h) if not (bool(len(h)-1)) else h)+(':' if pages else "")+('0%s'%(m) if not (bool(len(m)-1)) else m)

GetCharWidth = lambda s: oled.DispChar(s, 0, 0, Colormode.noshow)[0][0] + int(len(s)/2)
AutoCenter = lambda string: 64 - GetCharWidth(string) // 2
HomeTimeAutoCenter = AutoCenter
def Box(x1, y1, x2, y2, fill = False):
    UITools()
    if fill:oled.fill_rect(x1 + 1, y1 + 1, x2 - 2, y2 - 2, 0)
    oled.rect(x1, y1, x2, y2, 1)

def ProgressBoxMove(x,y,w,h,progress,step=8):
    #progress使用百分制%
    now,OurUI = 0,UI(oled)#我们的 UI (苏里苏气)
    for _ in range(step):
        OurUI.ProgressBar(x, y, w, h, ((w - 0) / (100 - 0)) * (now - 0) + 0)
        oled.show()
        now+=(progress-now)//2
        time.sleep_ms(25)
    del OurUI;now;gc.collect()#苏联解体力(悲)
class App:
    def Style1(appTitle:str, window = False):
        App.Style2(appTitle, window , True)
        Text(appTitle, 5, 0, 3, 1, 100)
        oled.DispChar(UITime(True), 93, 0, 1)

    def Style2(appTitle:str, window = False, test = False):
        oled.fill_rect(0,0,128,16,0)
        UITools()
        if window:Box(1, 1, 126, 62)
        if test:return
        Text(appTitle, 5, 5, 3, 1, 90)

class Select:
    @staticmethod
    def Style1(dispContent:list, y:int, window:bool = False, appTitle = None):
        oled.fill(0)
        UITools()
        selectNum = 0
        if appTitle:App.Style1(appTitle, window)
        elif window:Box(1,1,126,62)
        oled.show()
        while not button_a.is_pressed():
            oled.fill_rect(0, 20, 128, 45, 0)
            oled.DispChar(dispContent[selectNum], AutoCenter(dispContent[selectNum]), y, 1)
            oled.DispChar(Core.ListState(dispContent, selectNum), 105, 40, 1)
            oled.show()
            if eval("[/GetButtonExpr('on')/]"):
                selectNum = min(selectNum + 1, len(dispContent) - 1)
            if eval("[/GetButtonExpr('py')/]"):
                selectNum = max(selectNum - 1, 0)
            if eval("[/GetButtonExpr('th')/]"):
                return selectNum
            time.sleep_ms(int(eval("[/Const('interval')/]")))
        return

    @staticmethod
    def Style2(dispContent:list, tip:list, y:int, window:bool = False, appTitle = None):
        oled.fill(0)
        UITools()
        selectNum = 0
        if appTitle:App.Style1(appTitle,window)
        if window:Box(1,1,126,62)
        oled.show()
        while not button_a.is_pressed():
            if window:
                oled.RoundRect(2, y - 18, 124, 55, 2, 1)
            oled.show()
            if eval("[/GetButtonExpr('on')/]"):
                selectNum = min(selectNum + 1, len(dispContent) - 1)
            if eval("[/GetButtonExpr('py')/]"):
                selectNum = max(selectNum - 1, 0)
            if eval("[/GetButtonExpr('th')/]"):
                return selectNum
            time.sleep_ms(int(eval("[/Const('interval')/]")))
            Text(tip[selectNum], 5, y, 2)
            Text(dispContent[selectNum], 5, y + 27, 3)
            oled.DispChar(Core.ListState(dispContent, selectNum), 105, 45, 1)
            oled.show()

    @staticmethod
    def Style3():
        #UITools()
        while not button_a.is_pressed():
            if eval("[/GetButtonExpr('on')/]"):return 1
            elif eval("[/GetButtonExpr('py')/]"):return 0
            time.sleep_ms(int(eval("[/Const('interval')/]")))

    @staticmethod        
    def Style4(dispContent:list, window:False, appTitle:str = False, x = 5, images = None):
        lendispcontext = len(dispContent)
        maxdispcontextindex = lendispcontext - 1
        listNum = 0
        if images!=None and x < 16:x=16
        while True:
            gc.collect()
            oled.fill(0)
            start = max(0, min(len(dispContent) - 3, listNum - 1))
            displayItems = dispContent[start:start + 3]
            for i, item in enumerate(displayItems):
                if images!=None:
                    try:oled.Bitmap(0,16*(i+1),images[i+start],16,16,0)
                    except:pass
                if listNum == i + start:continue
                Text(item, x, 16 * (i + 1), 2, showMode=1)
            if len(displayItems) > 0:
                oled.fill_rect(x, 16 + 16 * (listNum - start), GetCharWidth(displayItems[listNum - start]), 16, 1)
                Text(displayItems[listNum - start], x, 16 + 16 * (listNum - start), 2, showMode = 2)
            if appTitle:
                App.Style1(appTitle,window)
            oled.show()
            while not button_a.is_pressed():
                if eval("[/GetButtonExpr('on')/]"):
                    if listNum < maxdispcontextindex:
                        VastSea.SelsetBoxMove(x, 16+16*(listNum-start),displayItems[listNum - start],
                                              x,16+16*(listNum-start+1),displayItems[listNum - start+1],
                                              MODE="fill_rect")
                        listNum += 1
                        break
                elif eval("[/GetButtonExpr('py')/]"):
                    if listNum > 0:
                        VastSea.SelsetBoxMove(x,16+16*(listNum-start),displayItems[listNum - start],
                                              x,16+16*(listNum-start-1),displayItems[listNum - start-1],
                                              MODE="fill_rect")
                        listNum -= 1
                        break
                elif eval("[/GetButtonExpr('th')/]"):
                    return listNum
                elif button_a.is_pressed():return None

ListOptions = Select.Style4

class VastSea:
    @staticmethod   
    def Switch():
        while not button_a.is_pressed():
            oled.fill(0)
            UITools()
            App.Style2(eval("[/Language('动效开关')/]"))
            get = int(Core.Data.Get("text", "VastSeaSwitch"))
            oled.DispChar([eval("[/Language('关闭')/]"), eval("[/Language('开启')/]")][get], 5, 18, 1)
            oled.show()
            get = Select.Style3()
            Core.Data.Write("text", 'VastSeaSwitch', str(get))
        return
    def SpeedSet():
        presuppose = lambda num:str((num+1)*100)
        while not button_a.is_pressed():
            options = Select.Style4(["高效", "优雅", "柔和"], False, "动画速率")
            if options != None:
                VastSea.Transition()
                Core.Data.Write("text", "VastSeaSpeed", presuppose(options))
                PagesManager.Main.Import('SeniorOS.system.pages', 'Message', True, "设置成功\n{}".format(["故事半古之人，功必倍之", "用心聆听，深深呼吸", "松风吹解带，山月照弹琴"][options]))
                VastSea.Transition(False)
            VastSea.Transition(False)
    @staticmethod
    def SelsetBoxMove(x,y,char,ToX,ToY,NewChar,MODE="rect"):
        sx=x;sy=y
        NowWidth = GetCharWidth(char)
        ToWidth = GetCharWidth(NewChar)
        gc.collect()
        if gc.mem_free() < (5 * (16 * NowWidth + 16 * ToWidth)):
            print("内存不足,停止运行!")
            return
        if MODE == "rect":
            char1FB=framebuf.FrameBuffer(bytearray(16*NowWidth),NowWidth,16,framebuf.MONO_VLSB)
            char2FB=framebuf.FrameBuffer(bytearray(16*ToWidth),ToWidth,16,framebuf.MONO_VLSB)
            oled.DispChar(char,0,0,buffer=char1FB)
            oled.DispChar(NewChar,0,0,buffer=char2FB)
        else:
            char1FB_FILL=framebuf.FrameBuffer(bytearray(16*NowWidth),NowWidth,16,framebuf.MONO_VLSB)
            char2FB_FILL=framebuf.FrameBuffer(bytearray(16*ToWidth),ToWidth,16,framebuf.MONO_VLSB)
            char1FB_FILL.fill(1)
            char2FB_FILL.fill(1)
            oled.DispChar(char,0,0,mode=2,buffer=char1FB_FILL)
            oled.DispChar(NewChar,0,0,mode=2,buffer=char2FB_FILL)
        if ToWidth > 0:
            NowW=GetCharWidth(char)
            for _ in range(6):
                if MODE == "rect":
                    oled.rect(x,y,NowW,16,1)
                    oled.blit(char1FB,sx,sy)
                    oled.blit(char2FB,ToX,ToY)
                    oled.show()
                    oled.rect(x,y,NowW,16,0)
                else:
                    oled.blit(char1FB_FILL,sx,sy)
                    oled.fill_rect(x,y,NowW,16,1)
                    oled.blit(char2FB_FILL,ToX,ToY)
                    oled.show()
                    oled.fill_rect(x,y,NowW,16,0)
                NowW+=(ToWidth-NowW)//2
                x+=(ToX-x)//2
                y+=(ToY-y)//2
                time.sleep_ms(25)
            '''
            if MODE == "rect":
                for i in range(6):
                    oled.rect(x,y,NowW,16,1)
                    oled.blit(char1FB,sx,sy)
                    oled.blit(char2FB,ToX,ToY)
                    oled.show()
                    oled.rect(x,y,NowW,16,1)
                    NowW+=(ToWidth-NowW)//2
                    x+=(ToX-x)//2
                    y+=(ToY-y)//2
                    time.sleep_ms(25)
            else:
                for i in range(6):
                    oled.blit(char1FB_FILL,sx,sy)
                    oled.fill_rect(x,y,NowW,16,1)
                    oled.blit(char2FB_FILL,ToX,ToY)
                    oled.show()
                    oled.fill_rect(x,y,NowW,16,0)
                    NowW+=(ToWidth-NowW)//2
                    x+=(ToX-x)//2
                    y+=(ToY-y)//2
                    time.sleep_ms(25)'''
        gc.collect()
        return
    @staticmethod   
    def Off():
        oled.fill(0)
        oled.show()
        time.sleep_ms(int(eval("[/Const('interval')/]")))
        return
    @staticmethod   
    def Transition(mode:bool = True):
        if int(Core.Data.Get("text", "VastSeaSwitch")):Animations.ClearFromLeftSide(mode)
        else:VastSea.Off()
        
    
    class SeniorMove:
        @staticmethod
        def Box(text, x=0, y=0, h=16):
            w = GetCharWidth(text)
            target_w = 128
            target_h = 64
            remaining_steps = 12
            step_x_total = x
            step_y_total = y
            step_w_total = target_w - w
            step_h_total = target_h - h
            step_x = step_x_total / remaining_steps
            step_y = step_y_total / remaining_steps
            step_w = step_w_total / remaining_steps
            step_h = step_h_total / remaining_steps
            oled.fill_rect(x, y, w, h, 0)
            oled.DispChar(text, x, y)
            oled.rect(x, y, w, h, 1)
            oled.show()
            time.sleep_ms(100)
            for i in range(12):
                oled.fill_rect(x, y, w, h, 0)
                oled.rect(x, y, w, h, 1)
                oled.show()
                oled.rect(x, y, w, h, 0)
                x -= int(step_x)
                y -= int(step_y)
                w += int(step_w)
                h += int(step_h)
                remaining_steps -= 1
                if remaining_steps > 0:
                    step_x = (x / remaining_steps) if remaining_steps > 0 else 0
                    step_y = (y / remaining_steps) if remaining_steps > 0 else 0
                    step_w = ((target_w - w) / remaining_steps) if remaining_steps > 0 else 0
                    step_h = ((target_h - h) / remaining_steps) if remaining_steps > 0 else 0
            oled.fill(0)
            time.sleep_ms(100)

        def Text(text, startX, startY, endX, endY, font = None) -> bool:
            speed = int(Core.Data.Get("text", "VastSeaSpeed"))
            if int(Core.Data.Get("text", "VastSeaSwitch")) == 1:
                elapsedTime = 0  # 已过去的时间
                timer = 10  # 定时器间隔（毫秒）
                oled.fill(0)
                while elapsedTime < speed:
                    elapsedTime += timer
                    t = elapsedTime / speed
                    factor = -(math.cos(math.pi * t) - 1) / 2
                    currentX= startX + (endX - startX) * factor
                    currentY = startY + (endY - startY) * factor
                    # 根据计算出的 currentX 和 currentY 更新位置
                    oled.fill(0)
                    # 是否自定义字体
                    if font != None:oled.DispChar_font(font, text, int(currentX), int(currentY))
                    oled.DispChar(text, int(currentX), int(currentY))
                    oled.show()
                return True
            else:
                VastSea.Off()
                return False

        def Line(startX, startY, startX2,startY2, endX, endY, endX2, endY2, fill:bool = True):
            speed = int(Core.Data.Get("text", "VastSeaSpeed"))
            if int(Core.Data.Get("text", "VastSeaSwitch")) == 1:
                elapsedTime = 0  # 已过去的时间
                timer = 10  # 定时器间隔（毫秒）
                while elapsedTime < speed:
                    elapsedTime += timer
                    t = elapsedTime / speed
                    factor = -(math.cos(math.pi * t) - 1) / 2
                    currentX = startX + (endX - startX) * factor
                    currentY = startY + (endY - startY) * factor
                    currentX2 = startX2 + (endX2 - startX2) * factor
                    currentY2 = startY2 + (endY2 - startY2) * factor
                    # 根据计算出的 currentX、currentY、currentX2 和 currentY2 更新线条的位置
                    if fill:oled.fill(0)
                    else:oled.fill_rect(startX, startY, 128, 3, 0)
                    oled.line(int(currentX), int(currentY), int(currentX2), int(currentY2), 1)
                    oled.show()
            else:
                VastSea.Off()

        def Bitmap(bitMap, startX, startY, endX, endY, h, w):
            speed = int(Core.Data.Get("text", "VastSeaSpeed"))
            if int(Core.Data.Get("text", "VastSeaSwitch")) == 1:
                elapsedTime = 0  # 已过去的时间
                timer = 10  # 定时器间隔（毫秒）
                while elapsedTime < speed:
                    elapsedTime += timer
                    t = elapsedTime / speed
                    factor = -(math.cos(math.pi * t) - 1) / 2
                    currentX = startX + (endX - startX) * factor
                    currentY = startY + (endY - startY) * factor
                    # 根据计算出的 current_x 和 current_y 更新位置
                    oled.Bitmap(int(currentX), int(currentY), bitMap, w, h, 1)
                    oled.show()
                    oled.Bitmap(int(currentX), int(currentY), bitMap, w, h, 0)
            else:VastSea.Off()
            
def UITools():
    if Core.Data.Get("text", "lightMode") == "1":oled.invert(1)
    oled.contrast(int(Core.Data.Get("text", "luminance")))

def LightModeSet():
    mode = [eval("[/Language('关闭')/]"),eval("[/Language('开启')/]")]
    while not button_a.is_pressed():
        oled.fill(0)
        UITools()
        App.Style2(eval("[/Language('日光模式')/]"))
        get = int(Core.Data.Get("text", "lightMode"))
        oled.DispChar(mode[get], 5, 18, 1)
        oled.show()
        get = Select.Style3()
        Core.Data.Write("text",'lightMode', str(get))

def LuminanceSet():
    luminance = int(Core.Data.Get("text", "luminance"))
    oled.contrast(luminance)
    UITools()
    while not button_a.is_pressed():
        oled.fill(0)
        App.Style2(eval("[/Language('亮度调节')/]"))
        oled.DispChar(eval("[/Language('当前值')/]") + str(luminance), 5, 18, 1)
        oled.show()
        if eval("[/GetButtonExpr('on')/]"):
            luminance = 255 if luminance > 250 else luminance + 5
        if eval("[/GetButtonExpr('py')/]"):
            luminance = 0 if luminance - 5 < 0 else luminance - 5
        oled.contrast(luminance)
    oled.contrast(luminance)
    Core.Data.Write("text",'luminance',str(luminance))
    return luminance

def TouchPadValueSet():
    sensitivity = int(Core.Data.Get("text", "touchPadValue"))
    while not button_A.is_pressed():
        oled.fill(0)
        App.Style2(eval("[/Language('触摸键灵敏度')/]"))
        oled.DispChar("{}:{}".format(eval("[/Language('当前值')/]"),str(sensitivity)), 5, 18, 1)
        oled.show()
        if eval("[/GetButtonExpr('on')/]"):
            sensitivity = (sensitivity + 5 if sensitivity + 5 <= 800 else 800)
        if eval("[/GetButtonExpr('py')/]"):
            sensitivity = (sensitivity - 5 if sensitivity - 5 >= -100 else -100)
        TouchPad.config(sensitivity)
    TouchPad.config(sensitivity)
    return Core.Data.Write("text","touchPadValue",sensitivity)

mode={0:Outmode.stop,1:Outmode.autoreturn,2:Outmode.ellipsis}
Text = lambda text,x,y,outMode,space = 1,maximum_x=126,returnX=5,returnAddy=16,showMode=1:oled.DispChar(text, x, y, showMode, mode.get(outMode), maximum_x, space, return_x = returnX, return_addy = returnAddy)