# ChangeWallpaper

修改注册表项`HKEY_CURRENT_USER\Control Panel\Desktop\WallPaper`的值为 图片路径后，再cmd运行 `RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters `，能否刷新成功 是看运气的。

但是用vb调用user32中的 `SystemParametersInfoW` 就能立即生效。 


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

### python打包到exe
`pyinstaller -F -w -i x.ico xxx.py`
生成spec后
`pyinstaller xxx.spec`