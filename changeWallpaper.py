import ctypes
from ctypes import c_int, byref
import win32con
import win32api
import os


# 获取当前背景桌面壁纸图片路径
def get_wallpaper():
    buff = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_GETDESKWALLPAPER,
        len(buff),
        buff,
        0
    )
    return buff.value


# 设置桌面
def set_wallpaper(path):
    changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
    return ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_SETDESKWALLPAPER,
        0,
        path,
        changed
    )


# 设置桌面背景颜色
def set_wallpaper_color(r, g, b):
    # R G B, 可能是小端系统, 所以G和B 要位移到左边
    cc = r | (g << 8) | (b << 16)
    return ctypes.windll.user32.SetSysColors(
        win32con.COLOR_BACKGROUND,
        byref(c_int(1)),
        byref(c_int(cc))
    )


def set_wallpaper_mode(mode_str):
    """
    2：拉伸  0：居中  6：适应  10：填充  22：平铺
    """
    modetable = {
        'fit': '6',
        'center': '0',
        'extend': '2',
        'fill': '10',
        'pad': '22'
    }
    reg_key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER,
        "Control Panel\\Desktop",
        0,
        win32con.KEY_SET_VALUE
    )
    win32api.RegSetValueEx(
        reg_key,
        "WallpaperStyle",
        0,
        win32con.REG_SZ,
        mode_str
    )


get_wallpaper()
absP = os.path.abspath('桌面-py.jpg')
set_wallpaper(absP)
set_wallpaper_mode('fit')
get_wallpaper()
set_wallpaper_color(r=255, g=0, b=0)

# TODO 收集执行信息 发到服务器