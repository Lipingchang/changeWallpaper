import ctypes
u32 = ctypes.windll.LoadLibrary("user32.dll")
print(u32)
u32.MessageBoxW(0, u'hhh',u'title', 0)