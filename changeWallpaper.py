import ctypes
from ctypes import c_int, byref
import win32con
import win32api
import os
import shutil
import sys
import psutil
import requests


def kill_process_by_name(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            process.kill()


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


# 调用后 要再调用下 set_wallpaper 让系统刷新下 不然不会起效的！
def set_wallpaper_mode(mode_str):
    """
    2：拉伸   6：适应  10：填充  0:平铺 0：居中 TileWallpaper=1=>平铺 0=>居中   22:跨区
    """
    modetable = {
        'fit': '6',
        'center': '0',
        'stretched': '2',
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
        modetable[mode_str]
    )
    # win32api.RegSetValueEx(
    #     reg_key,
    #     "TileWallpaper",
    #     0,
    #     win32con.REG_SZ,
    #     "0"
    # )
    win32api.RegCloseKey(reg_key)


#
def set_wallpaper_changeable(path, mode_str, able=False):
    """        0=Center 1=Tiled 2=Stretched 3=Fit 4–Fill 5=Span   和之前的有点不一样 """
    mode_table = {
        'fit': '3',
        'center': '0',
        'stretched': '2',
        'fill': '5',
    }
    reg_key_system, flag_1 = win32api.RegCreateKeyEx(
        win32con.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
        win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY
    )
    reg_key_desktop, flag_2 = win32api.RegCreateKeyEx(
        win32con.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\ActiveDesktop",
        win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY
    )
    if not able:
        # 设置死 桌面图片/样式, 设置后不会自动刷新桌面; 会在注销重新登录后刷新,win10会在切换桌面的时候刷新
        # windows10中 此项的优先级高于 "Control Panel\\Desktop" 中的内容
        win32api.RegSetValueEx(
            reg_key_system,
            "WallpaperStyle",
            0,
            win32con.REG_SZ,
            '3'
            # mode_table[mode_str]
        )
        win32api.RegSetValueEx(
            reg_key_system,
            "Wallpaper",
            0,
            win32con.REG_SZ,
            path
        )
        # 只设置 防止修改 = 打开个性化页面的时候 显示被组织接管隐藏
        win32api.RegSetValueEx(
            reg_key_desktop,
            "NoChangingWallPaper",
            0,
            win32con.REG_DWORD,
            1
        )
    else:
        try:
            win32api.RegDeleteValue(
                reg_key_system,
                "WallpaperStyle",
            )
            win32api.RegDeleteValue(
                reg_key_system,
                "Wallpaper",
            )
        except win32api.error as exc:
            import winerror
            if exc.winerror != winerror.ERROR_FILE_NOT_FOUND:
                raise

        win32api.RegSetValueEx(  # 设置为0时 不起效
            reg_key_desktop,
            "NoChangingWallPaper",
            0,
            win32con.REG_DWORD,
            0
        )
    win32api.RegCloseKey(reg_key_system)
    win32api.RegCloseKey(reg_key_desktop)



def main_wallpaper(absP, r,g,b, filename, changeAble):
    # get_wallpaper()
    # absP = os.path.abspath('桌面-py.jpg')
    # set_wallpaper(absP)
    # get_wallpaper()
    # set_wallpaper_color(r=255, g=0, b=0)
    # absP = "C:\\Windows\\showshow\\"
    os.makedirs(absP, exist_ok=True)
    picAbsP = os.path.join(absP, "桌面.jpg")
    shutil.copyfile(filename, picAbsP)
    set_wallpaper_mode('fit')
    set_wallpaper(picAbsP)
    set_wallpaper_color(r=r, g=g, b=b)
    set_wallpaper_changeable(picAbsP, 'fit', changeAble)


def get_screensaver():
    reg_key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER,
        "Control Panel\\Desktop",
        0,
        win32con.KEY_READ | win32con.KEY_WOW64_64KEY
    )
    value, key_type = win32api.RegQueryValueEx(reg_key, "SCRNSAVE.EXE")
    win32api.RegCloseKey(reg_key)
    print(value, key_type)


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


def main_screensaver(absP):
    # get_screensaver()
    # absP = "C:\\Windows\\showshow\\screensaver"
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


configs = []
with open('./config.ini', 'r') as f:
    configs = ''.join(f.readlines()).split('\n')
[R, G, B, wallpaperSrc, changeAble, logserverIP, logserverPort] = configs
R = int(R)
G = int(G)
B = int(B)
logserverPort = int(logserverPort)
if changeAble == 'False':
    changeAble = False
elif changeAble == 'True':
    changeAble = True
else:
    assert False, "changeAble illegal"
assert os.path.exists(wallpaperSrc) == True, "wallpaper file name not exist"

# 终端已经在屏保界面 需要先杀屏保进程
kill_process_by_name("screenSaverTest.exe")
kill_process_by_name("screenSaverTest.src")

homePath = "C:\\Windows\\showshow\\"
shutil.rmtree(homePath, ignore_errors=True)
main_wallpaper(os.path.join(homePath, "wallpaper"), R,G,B, wallpaperSrc, changeAble)
main_screensaver(os.path.join(homePath, "screensaver"))

try:
    # TODO 收集执行信息 发到服务器
    r = requests.post(f"http://{logserverIP}:{logserverPort}", data={'done': True})
    # print(r.text)
except:
    pass


