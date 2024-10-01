# FTReader - by LP_OVER
# Copyright (c) 2024 LP_OVER
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from SeniorOS.lib.devlib import *
import SeniorOS.system.core as Core
import SeniorOS.system.daylight as DayLight
import SeniorOS.apps.logo as Logo
import os
import gc
import SeniorOS.lib.log_manager as LogManager
import framebuf,time
Log = LogManager.Log

img = Logo.GetLogo("/SeniorOS/data/ftreader.sros")
class Animations:
    def ClearFromLeftSide(mode:bool = True):
        if mode:
            for i in range(13):
                times = i * i
                oled.vline(times, 0, 64, 1)
                oled.vline(times+1, 0, 64, 0)
                oled.fill_rect(0, 0, times, 64, 0)
                oled.show()
        else:
            for i in range(13):
                times = 13 - i
                times_squared = times * times
                oled.fill_rect(0, 0, 128, 64, 0)
                oled.vline(times_squared, 0, 64, 1)
                oled.vline(times_squared + 1, 0, 64, 0)
                oled.show()
    def textMove(text):
        Core.FullCollect()
        total=156
        movText=framebuf.FrameBuffer(bytearray(16*DayLight.GetCharWidth(text)),DayLight.GetCharWidth(text),16,framebuf.MONO_VLSB)
        oled.DispChar(text,0,0,buffer=movText)
        for i in range(7):
            oled.fill_rect(total,12,128,16,0)
            oled.vline(total-1,14,12,1)
            oled.blit(movText,total+1,12)
            total=total-((7-i)**2)
            oled.show()
            time.sleep(0.01)
    def lineMove():
        i=0
        for _ in range(7):
            oled.fill_rect(0,(64-i),128,64,0)
            oled.hline(49,(66-i),30,1)
            oled.show()
            i+=(64-i)//2
        oled.fill_rect(0,0,128,64,0)
        oled.hline(49,2,30,1)
        oled.show()
    def boxMove(text):
        boxlong=17+(len(text)*8)
        xb=128-boxlong
        yb=48
        for _ in range(7):
            oled.fill_rect(0,0,xb,yb,0)
            oled.rect(0,0,xb,yb,1)
            oled.show()
            xb=(128-xb)//2+xb
            yb=(64-yb)//2+yb
        oled.fill_rect(0,0,128,64,0)
        oled.rect(0,0,128,64,1)
        oled.show()
class picture:
    #fileviewer_images
    pathpic=img.Logo(0)
    filepic=img.Logo(1)
    runpic=filepic
    picpic=img.Logo(2)
    #DiskManager_images
    Flash = img.Logo(3)
    SDCard = img.Logo(4)
    EXIT = img.Logo(5)
class Textreader:
    def __init__(self, text, splitCfg="\n"):
        self.text = text.split(splitCfg)
    def showText(self,lines=0,offset=0,y=0):
        for i in [0,1,2]:
            try:oled.DispChar(self.text[i+lines],0-offset,i*16+y)
            except:continue
        return
    def text_info(self,info):
        if info:return int(len(self.text)/3)
        else:return len(self.text)%3
    
    def test2(self):
        self.showText()
        Animations.ClearFromLeftSide()
            
    def Main(self):
        page_num=self.text_info(True)+self.text_info(False)
        n=0;offset=0
        while not (touchpad_t.is_pressed() or touchpad_h.is_pressed()):
            Core.FullCollect()
            oled.fill(0)
            self.showText(n,offset)
            oled.DispChar("<PY",0,48);oled.DispChar("ON>",104,48)
            oled.DispChar("{}/{}".format(int(n/3)+1,int(page_num)+1),52,48)
            oled.hline(0,48,128,1)
            oled.show()
            while not (touchpad_t.is_pressed() or touchpad_h.is_pressed()):
                if touchpad_p.is_pressed() or touchpad_y.is_pressed():
                    time.sleep_ms(100)
                    if n-3<0:n=0
                    else:n-=3
                    break
                elif touchpad_n.is_pressed() or touchpad_o.is_pressed():
                    time.sleep_ms(100)
                    if n+3>page_num*3:n=page_num*3
                    else:n+=3
                    break
                if button_b.is_pressed():
                    offset+=8
                    break
                elif button_a.is_pressed():
                    offset-=8
                    break
class DiskManager:
    def __init__(self):
        self.DiskList = ["flash"]
        self.DiskListPoint = ["/"]
        #本来这里可以用json的，但sm dl不给用
        self.SDCard=False
        self.RamDisk = False
        self.sd_read_only = False
    def DiskManager(self):
        while True:
            options = DayLight.ListOptions(["打开存储器","SD卡管理器","退出"],window=False,appTitle = "资源管理",x=16 ,images = [picture.Flash,picture.SDCard,picture.EXIT])
            gc.collect()
            if options == 0:
                FileViewer().fileviewer(self.DiskListPoint[DayLight.ListOptions(self.DiskList,False,appTitle = "选择盘")])
            elif options == 1:
                options = DayLight.ListOptions(["挂载SD卡","卸载SD卡"],False,appTitle = "选择操作")
                if options == 0: #已导入
                    Pages.Message("请将卡插至P13-P16",True)
                    #挂载部分
                    self.sd_read_only = bool(DayLight.ListOptions(["读/写","只读"],False,appTitle = "SD卡权限"))
                    os.mount(SDCard(sck = Pin.P13, miso = Pin.P14, mosi = Pin.P15, cs = Pin.P16), "/sd", readonly = self.sd_read_only)
                    Pages.Message("SD卡已挂载至目录  /sd")#看着有点乱
                    self.SDCard=True
                    self.DiskList.append("SDCard")
                    self.DiskListPoint.append("/sd")
                elif options == 1:
                    if self.SDCard:
                        os.umount(self.sd_fsdir)
                        Pages.Message("SD卡已卸载!",True)
                        self.SDCard = False
                        self.DiskList.remove("SDCard")
                        self.DiskListPoint.remove("/sd")
                    else:
                        Pages.Message("未挂载SD卡!",True)
            elif options == 2:
                return 0
class FileViewer:
    def __init__(self):
        self.Dir=os.listdir("/")
        self.Dir.insert(0,"返回上一层")
        self.DirLen=len(self.Dir)
        self.config={0:"目录",1:"文件",2:"可执行文件",3:"图片"}
        self.PictureConfig={"目录":picture.pathpic,"文件":picture.filepic,
                            "可执行文件":picture.runpic,"图片":picture.picpic,}
    def UseTextReader(self,Path):
        with open(Path,"r") as f:
            readFile=Textreader(f.read())
            Animations.ClearFromLeftSide()
            readFile.Main()
            readFile.test2()
        del readFile;gc.collect()
    def ShowImage(self,Path):
        Animations.boxMove("image")
        oled.fill(0)
        oled.blit(Image().load(Path), 0, 0)
        oled.show()
        while not button_a.is_pressed():pass
        return 0

    def FileConfig(self,filePath:str):#文件类型判断
        if filePath.endswith("返回上一层") or os.stat(filePath)[0]<20000:return 0#上一层是目录(
        else:
            stringEnd=filePath.endswith
            if stringEnd(".py") or stringEnd(".mpy"):return 2
            elif stringEnd(".pbm") or stringEnd(".bmp"):return 3
            else:return 1
    def fileviewer(self,path:str="/"):
        selset_num = 0
        while True:
            print("{}/{}".format(path,self.Dir[selset_num]))
            file_config=self.config[self.FileConfig("{}/{}".format(path,self.Dir[selset_num]))]#获取文件属性
            oled.fill(0)
            oled.text("%s"%(path),4,4)
            oled.DispChar(self.Dir[selset_num],16,12)
            oled.DispChar("TH-打开",0,32)
            oled.DispChar("<PY",0,48);oled.DispChar("ON>",104,48)
            oled.DispChar("{}/{}".format(selset_num+1,self.DirLen),DayLight.AutoCenter("{}/{}".format(selset_num+1,self.DirLen)),48)
            oled.Bitmap(0,12,self.PictureConfig[file_config],16,16,1)
            oled.hline(0,28,130,1)
            oled.rect(2,2,124,12,1)
            oled.show()
            while True:
                if button_a.is_pressed():return 0
                elif touchpad_t.is_pressed() or touchpad_h.is_pressed():
                    RealPath = "{}/{}".format(path,self.Dir[selset_num])
                    if file_config=="目录":
                        if self.Dir[selset_num]=="返回上一层":
                            RealPath = path.replace("/"+path.split("/")[-1],"")
                        else:RealPath = "{}/{}".format(path,self.Dir[selset_num])
                        path=RealPath
                        if path.startswith("//"):path=path[1:]
                        self.Dir=os.listdir(RealPath)
                        self.Dir.insert(0,"返回上一层")
                        self.DirLen=len(self.Dir)
                        selset_num=0
                        Animations.ClearFromLeftSide()
                    elif file_config=="可执行文件":
                        __import__(RealPath[:-3] if RealPath.endswith(".py") else RealPath[:-4])
                    elif file_config=="图片":self.ShowImage("{}/{}".format(path,self.Dir[selset_num]))
                    else:self.UseTextReader("{}/{}".format(path,self.Dir[selset_num]))
                    break
                if touchpad_n.is_pressed() or touchpad_o.is_pressed():
                    try:Animations.textMove(self.Dir[selset_num+1])
                    except:Animations.textMove(self.Dir[0])
                    selset_num+=1
                    if selset_num>=self.DirLen:selset_num=0
                    break
                elif touchpad_p.is_pressed() or touchpad_y.is_pressed():
                    try:Animations.textMove(self.Dir[selset_num-1])
                    except:Animations.textMove(self.Dir[self.DirLen-1])
                    selset_num-=1
                    if selset_num<0:selset_num=self.DirLen-1
                    break

def Main():
    DiskManager().DiskManager()
    return 