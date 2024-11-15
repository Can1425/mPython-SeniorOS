# 关于DiskRam(Virtual Memory)
## 简介
DiskRam是一个基于I/O文件读写的虚拟内存库，它将变量信息存储于文件中，通过文件读写实现内存操作。它支持Python3.6+，并且可以跨平台使用。

## 类

### DiskRamError
继承自OSError，用于表示DiskRam库中的错误。

### DiskRam

#### __init__(self, RamPath)
DiskRam的初始化函数,RamPath为虚拟内存文件路径。

#### GetItem(self, var, offset = None)
获取存储在DiskRam中的变量值
var为变量名
offset为偏移量，默认为None，当var为数组变量时，offset为偏移量

#### SetItem(self, varclass, var, value, length=False)
设置存储在DiskRam中的变量值
varclass为变量类型，var为变量名，value为变量值，length为数组长度，默认为False(此时不创建数组变量,若强行创建会引发报错)

#### Collect(self)
删除垃圾数据

## 使用

### 初始化DiskRam
```python
from DiskRam import DiskRam
diskRam = DiskRam("path")#path为虚拟内存文件路径
```

### 定义变量
1.定义变量
```python
diskRam.SetItem("int","varname",value) 
#int为变量类型，varname为变量名，value为变量值
```
2.定义数组变量
```python
diskRam.SetItem("int","varname",value,length)
#length为数组长度
```

### 获取变量
```python
diskRam.GetItem("varname", offset = n)
#offset默认为None,当varname为数组变量时,n为此数组的偏移量
```

### 删除垃圾数据
```python
diskRam.Collect()
```
