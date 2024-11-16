# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# DiskRam - by LP_OVER
# 参与的贡献者:emofalling
# DiskRam - v1.0.2
import re,struct
import os,gc
class DiskRamError(OSError):
    pass
class DiskRam:
    def __init__(self,RamPath):
        self.RamPath=RamPath
        self.TypeDict = {
                         "bool":'B',  # bool(unsigned char) , 1 byte
                         "int":'q',   # long long, 8 bytes
                         "float":'d', # double   , 8 bytes
                         "str":'s',   # string   , - length,
                         "byte":'y' #byte     , 1 byte
                        }
        self.SizeDict = {
                         "c": 1,   # char
                         "b": 1,   # signed char
                         "B": 1,   # unsigned char
                         "h": 2,   # short
                         "H": 2,   # unsigned short
                         "i": 4,   # int
                         "I": 4,   # unsigned int
                         "l": 4,   # long
                         "L": 4,   # unsigned long
                         "q": 8,   # long long
                         "Q": 8,   # unsigned long long
                         "f": 4,   # float
                         "d": 8,   # double
                         "s":-1,   # string
                         "y":1,    #byte
                        }
        self.var={}
        self.pattern=re.compile(r"'(.*?)'")
        self.file = open(self.RamPath, 'wb+')
    def GetItem(self, var, offset = None):
        f = self.file
        try:
            addr = self.var[var]
        except KeyError:
            raise DiskRamError("GetItem: Variable not found: Undefined")
        try:
            f.seek(addr)
        except (OSError, EOFError):
            raise DiskRamError("GetItem: Variable not found: Address Error")
        typestr = f.read(1).decode('ascii')
        if f.read(1) == b'<':IsArrayB = True
        else:IsArrayB=False
        f.seek(f.tell()-1)
        if typestr == 's':
            length = struct.unpack('I',f.read(4))[0]
            raw = f.read(length)
            return raw.decode('utf-8')
        else:
            if IsArrayB:
                f.read(1)#读到<了
                size = ''
                while True:
                    data = f.read(1)
                    if data == b'>':break
                    size += data.decode('ascii')
                size = int(size)*self.SizeDict[typestr]
                data = []
                for i in range(size//self.SizeDict[typestr]):
                    if offset != None:
                        if i == offset:
                            if typestr == 'y':return f.read(self.SizeDict[typestr])
                            else:return struct.unpack(typestr,f.read(self.SizeDict[typestr]))[0]
                    if typestr == 'y':data.append(f.read(self.SizeDict[typestr]))
                    else:data.append(struct.unpack(typestr,f.read(self.SizeDict[typestr]))[0])
                return data
            else:
                size = self.SizeDict[typestr]
                raw = f.read(size)
                if typestr=='y':return raw
                else:return struct.unpack(typestr,raw)[0]
    def SetItem(self, varclass, var, value, length=False):
        if varclass == "char":varclass = "str"
        f = self.file
        f.seek(0,2)
        try:
            typestr = self.TypeDict[varclass] 
        except KeyError:
            if length!= False:raise DiskRamError("SetItem:This data type is not supported by the DiskRam array")#by bing(((
            else:raise DiskRamError("SetItem: Unknown Type")
        if length != False:
            if typestr == 's':
                data = ''
                for i in range(length):data+=value[i]
                self.SetItem("str",var,data)
            elif typestr == 'y':
                self.var[var]=f.tell()
                f.write(("y<%d>"%length).encode("ascii"))
                for i in range(length):
                    try:f.write(value[i])
                    except:f.write(b'\x00')
            else:
                self.var[var]=f.tell()
                f.write(typestr.encode('ascii'))
                f.write(("<%d>"%length).encode("ascii"))
                for i in range(length):
                    try:f.write(struct.pack(typestr,value[i]))
                    except:f.write(struct.pack(typestr,0))
        else:
            self.var[var]=f.tell()
            f.write(typestr.encode('ascii'))
            if typestr == 's':
                value = value.encode('utf-8')
                f.write(struct.pack('I',len(value)))
                f.write(value)
            elif typestr == 'y':
                f.write(value)#bytes
            else:
                f.write(struct.pack(typestr,value))
            f.flush()
    def Collect(self):
        gc.collect()
        f = self.file
        f.seek(0)
        points = list(self.var.values())
        tmpofindex = {}
        with open("tmp.ram","wb+") as tmp:
            for i in range(len(points)):
                f.seek(points[i])
                typestr = f.read(1).decode('ascii')
                IsArrayB = False
                if f.read(1) == b'<':IsArrayB = True
                f.seek(f.tell()-1)
                if typestr == 's':
                    length = struct.unpack('I',f.read(4))[0]
                    raw = f.read(length)
                    tmpofindex[list(self.var.keys())[i]] = tmp.tell()
                    tmp.write(b's')
                    tmp.write(struct.pack('I',length))
                    tmp.write(raw)
                else:
                    if IsArrayB:
                        f.read(1)#读到<了
                        size = ''
                        while True:
                            data = f.read(1)
                            if data == b'>':break
                            size += data.decode('ascii')
                        size = int(size)*self.SizeDict[typestr]
                        data = f.read(self.SizeDict[typestr]*size)
                        tmpofindex[list(self.var.keys())[i]] = tmp.tell()
                        tmp.write(typestr.encode('ascii'))
                        tmp.write(("<{}>".format(size//self.SizeDict[typestr])).encode("ascii"))
                        tmp.write(data)
                    else:
                        data = f.read(self.SizeDict[typestr])
                        tmpofindex[list(self.var.keys())[i]] = tmp.tell()
                        tmp.write(typestr.encode('ascii'))
                        tmp.write(data)
            tmp.flush()
            f.close()
            self.file = open(self.RamPath,"wb+")
            tmp.seek(0)
            while True:
                data = tmp.read(128)
                if data == b'':break
                self.file.write(data)
                self.file.flush()
        self.var = tmpofindex
        os.remove("tmp.ram")
        gc.collect()
        return 0
    def Delete(self,var):
        if var in self.var:
            self.var.pop(var)
            self.Collect()
            return 0
        else:
            raise DiskRamError("Delete: Variable not found: Undefined")
            

if __name__ == "__main__":
    d = DiskRam("test.ram")
    d.SetItem("byte","a",[b"\x00",b"\x01",b"\x02",b"\x03",b"\x04"],5)
    print(d.GetItem("a",3))
    #d.SetItem("int","a",5)
    #d.SetItem("int","c",[1,2,3,4,5],5)
    #d.SetItem("int","c",[5,4,3,2,1],5)
    #d.SetItem("int","a",16)
    #d.Collect()
    #d.Delete("a")
    #print("a的值为:",d.GetItem("a"))
    #print("c[0]的值为:",d.GetItem("c",0))