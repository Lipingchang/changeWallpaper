REM ChangeWallpaper.bat
REM Compiles ChangeWallpaper.vb to ChangeWallpaper.exe
C:\Windows\Microsoft.NET\Framework\v4.0.30319\vbc "%~dp0\ChangeWallpaper.vb" /out:"%~dp0\ChangeWallpaper.exe" /target:winexe
pause
start %~dp0\ChangeWallpaper.exe