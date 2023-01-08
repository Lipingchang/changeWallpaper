Imports System.Runtime.InteropServices

Public Module ChangeWallpaper
	'改桌面图标的系统调用
    Public Declare Unicode Function SystemParametersInfoW Lib "user32" (ByVal uAction As Integer, ByVal uParam As Integer, ByVal lpvParam As String, ByVal fuWinIni As Integer) As Integer
    '改桌面颜色的系统调用
	Public Declare Function SetSysColors Lib "user32.dll" (ByVal one As Integer, ByRef element As Integer, ByRef color As Integer) As Boolean
	Public Const SPI_SETDESKWALLPAPER = 20
    Public Const SPIF_SENDWININICHANGE = &H2
    Public Const SPIF_UPDATEINIFILE = &H1

	Public Sub Main()
		' 操作注册表，设置桌面图片为fit，在分辨率不同的时候，自动缩放图片适应桌面
		Dim rkey As Microsoft.Win32.RegistryKey = Microsoft.Win32.Registry.CurrentUser.OpenSubKey("Control Panel\Desktop", True)
		rkey.SetValue("WallpaperStyle", "6")
		rkey.SetValue("TileWallpaper", "0")
		rkey.Close()
		
		'改桌面颜色，fit后的图片会有留白，留白的颜色要改成红色，用注册表改后，不会生效，换用 系统调用 方法
		'Dim rkey2 As Microsoft.Win32.RegistryKey  = Microsoft.Win32.Registry.CurrentUser.OpenSubKey("Control Panel\Colors", True)
		'rkey2.SetValue("Background", "255 20 20")
		'rkey2.Close()
		Dim bgColor = 165 Or (10 << 8) Or (12 << &H10)
		SetSysColors(1, 1, bgColor)

		'把当前文件夹下的桌面图片 复制覆盖到系统文件夹下
		Dim FileToMove As String
		Dim MoveLocation As String
		FileToMove = ".\桌面.jpg"
		MoveLocation = "C:\Windows\劳动竞赛桌面1.jpg"
		If System.IO.File.Exists( FileToMove ) = True Then
			System.IO.File.Copy( FileToMove, MoveLocation, True )
			'MessageBox.Show("File Moved")
		End If
		
		Dim Ret as Integer
		'Dim FName As String
		'Fname = "C:\Windows\劳动竞赛桌面1.bmp"
		'This below line which is commented out takes a filename on the command line
		'FName = Replace(Command(), """", "")

		'修改桌面图片
		Ret = SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, MoveLocation, SPIF_SENDWININICHANGE + SPIF_UPDATEINIFILE)
		If Ret = 0 Then Msgbox(err.lastdllerror)
	End Sub

End Module