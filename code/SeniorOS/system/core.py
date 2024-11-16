import time
import os
import network
import gc
import time
import SeniorOS.lib.toml as toml
from machine import unique_id
from SeniorOS.lib.devlib import *
import SeniorOS.lib.log_manager as LogManager
LogManager.Output("system/core.mpy", "INFO")

class SharedVar:
    class LoadQuit:
        def __init__(self):
            self.value = None
            self.text = None
        def __bool__(self):
            return bool(self.value)
        def __str__(self):
            return str(self.text)

class DataCtrl:
    # 初始化函数，传入文件夹路径
    def __init__(self,dataFolderPath): # 文件夹传参结尾必须要有反斜杠！！！
        self.data={}
        self.dataFolderPath=dataFolderPath
        LogManager.Output("SystemData initial", "INFO")
        self.toml = toml.toml()
        for i in [f for f in os.listdir(dataFolderPath) if f.endswith('.toml')]:
            with open(dataFolderPath+i,'r',encoding='utf-8')as f:self.data[i.replace('.toml','')]=self.toml.toml2dict(f)
    # 获取数据
    def GetOriginal(self,FileName,end="sros"):
        with open("%s/%s.%s"%(self.dataFolderPath,FileName,end),"r") as f:return f.read()
    def Get(self, controls, dataName):
        ConfigRead = self.data[controls]
        try:return eval(eval("ConfigRead[dataName]",{"ConfigRead":ConfigRead,"dataName":dataName}))
        except:return ConfigRead[dataName]
    def Write(self, controls, dataName, dataValue):
        self.data[controls][dataName] = dataValue
        with open(self.dataFolderPath+controls+'.toml',"w") as f:f.write(self.toml.dict2toml(self.data[controls]))
        return dataValue

Data = DataCtrl("/SeniorOS/data/")
VitalData = lambda nothing:Data.Get("text","touchPadValue")

class AppSetup:
    def __init__(self,filePath):
        import SeniorOS.apps.Logo as Logo
        self.sl = Logo
        #logo.GetLogo("/SeniorOS/data/Logo.sros").Logo(1)
        self.logo = "Normal"
        self.filePath=filePath
    def SetLogo(self,logo:bytearray):
        self.logo=logo
    def Main(self):
        #安装文件格式:
        #------------------------------(安装example.py)
        # #示例应用(名称)
        # #example.py
        # //以下都是文件数据
        #---------------------------------------------
        with open(self.filePath,"r") as f:
            f.seek(0)
            Data.Write("list","localAppName",Data.Get("list","localAppName").append((f.readline()).strip("\n").strip("\r")))#写入应用名称
            with open("/SeniorOS/apps/{}".format(f.readline().strip("\n").strip("\r")),"w") as f2:f2.write(f.read())#写入文件数据
            if self.logo!="Normal":self.logo = self.sl.GetLogo("/SeniorOS/data/Logo.sros").Logo(1)
            with open("/SeniorOS/data/Logo.sros","a+") as f2:f2.write(self.logo)
        return
# Core.AppSetup("/SeniorOS/download/test.spk").setup()
    
# 文件/路径 格式工厂
class File_Path_Factory:

    # 将所有的斜杠替换为反斜杠 便于统一路径
    Replace2Backslash = lambda path: path.replace("/", "\\")
    #def Replace2Backslash(path):
    #    return path.replace("\\","/")

    # 判断文件是否存在
    # 传入一绝对路径 返回1布尔值
    def FileIsExist(filePath:str)->bool:
        filePath=File_Path_Factory.Replace2Backslash(filePath)
        if filePath[-1] in os.listdir("/"+filePath[:-1]):return True
        else:return False

    # 判断路径指向的文件对象是否是目录
    # 传入一绝对路径 返回1布尔值
    def IsDir(filePath:str)->bool:
        # 检查st_mode(第一项)中文件类型位
        try:return os.stat(filePath)[0] & 0o170000 == 0o040000
        # 如异常代表路径无效或不是目录
        except:return False

# 获取日期 ByGxxk
class GetTime:
    Year=lambda:time.localtime()[0]
    Month=lambda:time.localtime()[1]
    Week=lambda:time.localtime()[6]
    Day =lambda:time.localtime()[2]
    Hour=lambda:time.localtime()[3]
    Min =lambda:time.localtime()[4]
    Sec =lambda:time.localtime()[5]

def FullCollect():
    # 反复进行collect函数直至达到极限
    # 此代码来自 TaoLiSystem
    m=gc.mem_free()
    while True:
        gc.collect()
        if m != gc.mem_free():
            m = gc.mem_free()
        else:
            return m

# 获取设备ID
def GetDeviceID(wifiStaObj=network.WLAN(network.STA_IF),mode=1):
    return ("".join(str(wifiStaObj.config('mac'))[2:len(str(wifiStaObj.config('mac')))-1].split("\\x")) if not bool(mode) else "".join(str(unique_id())[2:len(str(unique_id()))-1].split("\\x")))
    #if mode==0:return "".join(str(wifiStaObj.config('mac'))[2:len(str(wifiStaObj.config('mac')))-1].split("\\x"))
    #elif mode==1:return "".join(str(unique_id())[2:len(str(unique_id()))-1].split("\\x"))
'''
# 支持2算法的截图
# 分别为 直接复制缓冲区数据(CopyFrameBuf) 和 枚举缓冲区数据(Enumerate)
# 在Enumerate中 又细分为 速度优先(fast) 与 内存占用最小(ram)
# 这里Enumerate部分使用的算法取决于构建阶段 对本代码作EXPR操作时 constData["screenMethod"] 的值是 fast 还是 ram
class Screenshot:
    def CopyFramebuf(path,oledObj=__import__("SeniorOS.lib.devlib")):
        bufb=bytearray(128*64)
        import framebuf
        with open(path,"wb")as f:
            f.write(b"P4\n128 64\n")
            buf=framebuf.FrameBuffer(bufb,128,64,framebuf.MONO_HLSB)
            buf.blit(oledObj.buffer,0,0)
            f.write(bufb)
        del bufb,buf,f;gc.collect()
    def Enumerate(path,oledObj=__import__("SeniorOS.lib.devlib")):# 以「枚举」为核心 的算法
        if eval("[/Const('screenshotMethod')/]")=="fast": # 速度优先
            with open(path, 'wb') as f:
                f.write(b'P4\n128 64\n')
                for y in range(128):
                    row_data = bytearray(8) #缓冲区
                    for x in range(64):row_data[x//8]|=(oledObj.pixel(x, y))<<7-(x%8) #循环 算偏移量 然后转格式 写到缓冲区内
                    f.write(row_data)
        elif eval("[/Const('screenshotMethod')/]")=="ram":# RAM优先
            buffer = bytearray(1024)  # 创建缓冲区
            # 获取屏幕像素状态
            for y in range(64):
                for x in range(128):
                    buffer[x//8+y*16]|=oledObj.pixel(x,y)<<7-(x%8)
            # 保存为PBM文件
            try:
                os.chdir("/SeniorOS/downloads")
            except:
                os.mkdir("/SeniorOS/downloads")
                os.chdir("/SeniorOS/downloads")
            with open('screenshot.pbm', 'wb') as f:
                # 写入PBM文件头
                f.write(b'P4\n128 64\n')
                f.write(buffer)  # 将缓冲区数据写入PBM文件'''
'''
def Tree(path="/",prt=print,_tabs=0):
    lst=os.listdir(path)
    dirs=[]
    files=[]
    l=0
    for i in lst:
        pti=path+'/'+i
        if os.stat(pti)[0] & 0x4000:
            dirs.append(i)
        else:
            files.append(i)
        l+=1
    lk="├"
    ldirs=len(dirs)
    for n,i in enumerate(dirs+files,1):
        if n==l:
            lk="└"
        prt("│"*_tabs+lk+i)
        if n<ldirs:
            Tree(path+'/'+i,prt,_tabs+1)'''
ListState=lambda dispContent,selectNum:"{}/{}".format(selectNum+1,len(dispContent))
#def ListState(dispContent, selectNum):
#    return "{}/{}".format(selectNum+1, len(dispContent))
