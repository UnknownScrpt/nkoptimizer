echo Off
color 6
echo.
echo.
echo.                 --------------------------------------------------------------------------------------------------------
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A 
:::                
:::                   $$$$$$$$\ $$\   $$\ $$\      $$\       $$$$$$$$\ $$\      $$\ $$$$$$$$\  $$$$$$\  $$\   $$\   $$$$$$\  
:::                   $$  _____|$$ |  $$ |$$$\    $$$ |      \__$$  __|$$ | $\  $$ |$$  _____|$$  __$$\ $$ | $$  | $$  __$$\ 
:::                   $$ |      \$$\ $$  |$$$$\  $$$$ |         $$ |   $$ |$$$\ $$ |$$ |      $$ /  $$ |$$ |$$  / $$ /  \__|
:::                   $$$$$\     \$$$$  / $$\$$\$$ $$ |         $$ |   $$ $$ $$\$$ |$$$$$\    $$$$$$$$ |$$$$$  /  \$$$$$$\  
:::                   $$  __|    $$  $$<  $$ \$$$  $$ |         $$ |   $$$$  _$$$$ |$$  __|   $$  __$$ |$$  $$<    \____$$\ 
:::                   $$ |      $$  /\$$\ $$ |\$  /$$ |         $$ |   $$$  / \$$$ |$$ |      $$ |  $$ |$$ |\$$\  $$\   $$ |
:::                   $$$$$$$$\ $$ /  $$ |$$ | \_/ $$ |         $$ |   $$  /   \$$ |$$$$$$$$\ $$ |  $$ |$$ | \$$\  \$$$$$$  |
:::                   \________|\__|  \__|\__|     \__|         \__|   \__/     \__|\________|\__|  \__|\__|  \__|  \______/ 
:::                                                                                                                 	
echo.                ----------------------------------------------------------------------------------------------------------
echo.  
echo.
echo.
echo 
echo.
echo                                                        Press Any Key To Continue...     
pause >nul  

echo.
echo [-] Cleaning Log files
echo.

cd/
@echo
del *.log /a /s /q /f

echo [+] Cleaned Log Files
echo.

echo [-] Cleaning Temp files
echo.

RD /S /Q %temp%
MKDIR %temp%
takeown /f "%temp%" /r /d y
takeown /f "C:\Windows\Temp" /r /d y
RD /S /Q C:\Windows\Temp
MKDIR C:\Windows\Temp
takeown /f "C:\Windows\Temp" /r /d y
takeown /f %temp% /r /d y
echo [+] Cleaned Temp files

echo.
echo [-] Flushing Dns Cache
ipconfig /flushdns
echo. 
echo [-] Windows Update Settings & Cleaning Cache
echo.

net stop wuauserv
net stop UsoSvc
gpupdate /force
rd s q "C:\Windows\SoftwareDistribution"
md "C:\Windows\SoftwareDistribution"
net start wuauserv
net start UsoSvc

echo [+] Deleted Windows Update Cache and useless files

echo.
echo [-] Clean
echo.

cleanmgr



echo.
echo [+] Cleaned All files
echo.

Pause
