# Code generated by font_to_py.py.
# Font: MiSans Latin VF(1)(1).ttf Char set: /0123456789:
# Cmd: H:\pgs\mpython\g\font\ptm字体文件\font_to_py.py -x -c 0123456789:/ MiSans Latin VF(1)(1).ttf 16 MiSans Latin VF.py
version = '0.33'
def height():
    return 16

def baseline():
    return 16

def max_width():
    return 13

def hmap():
    return True

def reverse():
    return False

def monospaced():
    return False

def min_ch():
    return 47

def max_ch():
    return 63

_font =\
b'\x0b\x00\x1f\x00\x71\x80\x60\xc0\x00\xc0\x00\xc0\x03\x80\x07\x00'\
b'\x0e\x00\x0c\x00\x0c\x00\x0c\x00\x00\x00\x00\x00\x0c\x00\x0c\x00'\
b'\x0c\x00\x08\x00\x02\x06\x06\x06\x0c\x0c\x0c\x18\x18\x18\x30\x30'\
b'\x30\x20\x60\x60\x0d\x00\x0f\x80\x18\xc0\x30\x60\x30\x60\x60\x30'\
b'\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x60\x30\x30\x60'\
b'\x30\x60\x18\xc0\x0f\x80\x08\x00\x0c\x3c\x6c\x4c\x0c\x0c\x0c\x0c'\
b'\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x00\x1f\x00\x31\x80\x60\xc0'\
b'\x00\xc0\x00\xc0\x00\xc0\x01\xc0\x01\x80\x03\x00\x07\x00\x0e\x00'\
b'\x0c\x00\x18\x00\x30\x00\x60\x00\x7f\xe0\x0d\x00\x3f\xe0\x00\xe0'\
b'\x00\xc0\x01\x80\x03\x00\x06\x00\x0f\x80\x0f\xe0\x00\x60\x00\x30'\
b'\x00\x30\x00\x30\x00\x30\x30\x60\x38\xe0\x0f\x80\x0d\x00\x01\xc0'\
b'\x03\xc0\x03\xc0\x06\xc0\x0e\xc0\x0c\xc0\x18\xc0\x18\xc0\x30\xc0'\
b'\x70\xc0\x60\xc0\xff\xf0\x00\xc0\x00\xc0\x00\xc0\x00\xc0\x0d\x00'\
b'\x1f\xe0\x18\x00\x10\x00\x10\x00\x10\x00\x30\x00\x3f\x80\x38\xe0'\
b'\x10\x60\x00\x30\x00\x30\x00\x30\x00\x30\x30\x60\x18\xe0\x0f\x80'\
b'\x0d\x00\x03\x00\x07\x00\x06\x00\x0c\x00\x0c\x00\x18\x00\x3f\x80'\
b'\x38\xe0\x70\x60\x60\x30\x60\x30\x60\x30\x60\x30\x30\x60\x38\xe0'\
b'\x0f\x80\x0b\x00\x7f\xc0\x00\xc0\x01\x80\x01\x80\x01\x80\x03\x00'\
b'\x03\x00\x02\x00\x06\x00\x06\x00\x0c\x00\x0c\x00\x0c\x00\x18\x00'\
b'\x18\x00\x30\x00\x0d\x00\x0f\x80\x30\xc0\x60\x60\x60\x60\x60\x60'\
b'\x60\x60\x30\xc0\x0f\x00\x38\xc0\x70\x60\x60\x30\x60\x30\x60\x30'\
b'\x70\x70\x38\xe0\x0f\x80\x0d\x00\x0f\x80\x38\xe0\x30\x60\x60\x30'\
b'\x60\x30\x60\x30\x60\x30\x30\x70\x38\xe0\x0f\xe0\x00\xc0\x01\x80'\
b'\x01\x80\x03\x00\x07\x00\x06\x00\x06\x00\x00\x00\x00\x00\x30\x30'\
b'\x30\x00\x00\x00\x00\x00\x00\x30\x30\x30'

_index =\
b'\x00\x00\x22\x00\x34\x00\x56\x00\x68\x00\x8a\x00\xac\x00\xce\x00'\
b'\xf0\x00\x12\x01\x34\x01\x56\x01\x78\x01\x00\x00\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x8a\x01'

_mvfont = memoryview(_font)
_mvi = memoryview(_index)
ifb = lambda l : l[0] | (l[1] << 8)
def get_ch(ch):
    oc = ord(ch)
    ioff = 2 * (oc - 47 + 1) if oc >= 47 and oc <= 63 else 0
    doff = ifb(_mvi[ioff : ])
    width = ifb(_mvfont[doff : ])

    next_offs = doff + 2 + ((width - 1)//8 + 1) * 16
    return _mvfont[doff + 2:next_offs], 16, width
 
