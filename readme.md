# ChangeWallpaper

修改注册表项`HKEY_CURRENT_USER\Control Panel\Desktop\WallPaper`的值为 图片路径后，再cmd运行 `RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters `，能否刷新成功 是看运气的。

但是用vb调用user32中的 `SystemParametersInfoW` 就能立即生效。 


## option1: 使用VB
从这个回答中抄来的：
https://stackoverflow.com/questions/56522110/how-to-fix-rundll32-exe-user32-dll-updateperusersystemparameters-1-true-not-upd

功能:
1. 改桌面图片
2. 改桌面颜色


流程:
1. 编辑vb文件
2. 运行VB_compiles_changewallpaper_vb_exe.bat，把vb编译成exe
3. **管理员**运行 ChangeWallpaper.exe 文件
4. 就会把当前目录下的 桌面.jpg 复制到 c:\windows 目录中，然后修改桌面图片

## option2: 使用 Python
### python打包到exe
`pyinstaller -F -w -i x.ico xxx.py`
生成spec后
`pyinstaller xxx.spec`

用nuitka打包出来的文件和pyinstaller一样？ `nuitka  --standalone --mingw64 --plugin-enable=tk-inter --output-dir=nuitkaout screenSaverTest.py`

加上 --onefile 后 启动速度也没变快。

onefile 和 -F 都会输出一个exe，但启动速度都不快, 可能是我的磁盘太慢了

### 开发环境: py39打包的exe会缺失库!
初始化32位的python虚拟环境: `E:\Python\Python36_32\python.exe -m venv .\venv32`

进入: `.\venv32\Scripts\activate.bat`

安装要用的库: `(venv)  pip install -r requirements.txt`

### 调用关系

changeWallpaper:

1. 把 **桌面-py.jpg** 复制到 c:\windows\showshow 文件夹中，然后设置其为桌面

2. 把 当前文件夹下的 **screensaverTest文件夹** 复制到 C:\windows\showshow 文件夹中，然后设置为屏保



### 配置文件
```
78          // RGB
33
24
desktop-py.jpg  // 桌面图片文件
True            // 用户能不能修改桌面图片
127.0.0.1       // 日志上报地址 和 端口
8810           
True            // 本次运行 只修改桌面
True            // 本次运行 只修改屏保
```