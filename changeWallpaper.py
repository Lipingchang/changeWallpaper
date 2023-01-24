import ctypes
from ctypes import c_int, byref
import win32con
import win32api
import os
import shutil
import sys


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
        1,                                          # 颜色列表的长度
        byref(c_int(win32con.COLOR_BACKGROUND)),    # 被改变颜色的控件列表
        byref(c_int(cc))                            # 颜色列表
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


def main_wallpaper():
    # get_wallpaper()
    # absP = os.path.abspath('桌面-py.jpg')
    # set_wallpaper(absP)
    # set_wallpaper_mode('fit')
    # get_wallpaper()
    # set_wallpaper_color(r=255, g=0, b=0)
    absP = "C:\\Windows\\showshow\\"
    os.makedirs(absP, exist_ok=True)
    shutil.copyfile("./桌面-py.jpg", os.path.join(absP,"桌面.jpg") )
    set_wallpaper(os.path.join(absP,"桌面.jpg"))


def get_screensaver():
    reg_key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER,
        "Control Panel\\Desktop",
        0,
        win32con.KEY_READ | win32con.KEY_WOW64_64KEY
    )
    value, key_type = win32api.RegQueryValueEx(reg_key, "SCRNSAVE.EXE")
    win32api.RegCloseKey(reg_key)
    print(value,key_type)


# 需要管理员权限
def set_screensaver(path):
    """ 1. 先关掉policy 组策略的设置 删除 \HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop 中有关screensaver的项目
    # 这个path可以带空格 不需要双引号 可能是向系统调用 传递参数的时候 是一个字符串?
    #r = os.system("rundll32.exe desk.cpl,InstallScreenSaver " + path) # 异步? 然后杀死弹出窗口?
    """

    regkey_policy_desktop, flag_policy_desktop = win32api.RegCreateKeyEx(  # 这个是管 能不能在ui界面修改, 不存在的话 就创建一个
        win32con.HKEY_CURRENT_USER,
        "SOFTWARE\\Policies\\Microsoft\\Windows\\Control Panel\\Desktop",
        win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY
    )
    regkey_desktop, flag_desktop = win32api.RegCreateKeyEx(
        win32con.HKEY_CURRENT_USER,
        "Control Panel\\Desktop",
        win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY
    )
    # print(flag_policy_desktop, flag_desktop, "REG_CREATED_NEW_KEY", "REG_OPENED_EXISTING_KEY")
    for rkey in [regkey_policy_desktop, regkey_desktop]:
        win32api.RegSetValueEx(
            rkey,
            "SCRNSAVE.EXE",
            0,
            win32con.REG_SZ,
            path
        )
        win32api.RegSetValueEx(
            rkey,
            "ScreenSaveTimeOut",
            0,
            win32con.REG_SZ,
            "300"                   # minutes
        )
        win32api.RegSetValueEx(
            rkey,
            "ScreenSaveActive",     # 这个看不出来啥区别
            0,
            win32con.REG_SZ,
            "1"
        )
        win32api.RegSetValueEx(
            rkey,
            "ScreenSaverIsSecure",     # 恢复后 是否 显示登录界面
            0,
            win32con.REG_SZ,
            "1"
        )
        win32api.RegCloseKey(rkey)


def main_screensaver():
    # get_screensaver()
    absP = "C:\\Windows\\showshow\\screensaver"
    srcPath = "screenSaverTest"
    if getattr(sys, 'frozen', False):
        # 打包后 可执行文件都放在 dist目录中 两个处于同级
        srcPath = os.path.join("./", srcPath)
    else:  # ide中 可执行文件放在 dist 目录中
        srcPath = os.path.join("./dist", srcPath)
    shutil.copytree(srcPath, absP)
    # 把文件名改成 scr 后缀
    if os.path.exists(os.path.join(absP, "screenSaverTest.exe")):
        shutil.move(
            os.path.join(absP, "screenSaverTest.exe"),
            os.path.join(absP, "screenSaverTest.scr")
        )
    set_screensaver(os.path.join(absP, "screenSaverTest.scr"))


shutil.rmtree("C:\\Windows\\showshow\\", ignore_errors=True)
main_wallpaper()
main_screensaver()
# TODO 收集执行信息 发到服务器
