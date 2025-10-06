@echo Off
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

cd /
@echo
del *.log /a /s /q /f 2>nul

echo [+] Cleaned Log Files
echo.

echo [-] Cleaning Temp files
echo.

:: Limpa %temp%
for /d %%D in ("%temp%\*") do rd /s /q "%%D" 2>nul
del /q /f "%temp%\*" 2>nul

:: Limpa C:\Windows\Temp
takeown /f "C:\Windows\Temp" /r /d y >nul 2>&1
icacls "C:\Windows\Temp" /grant Administrators:F /t >nul 2>&1
for /d %%D in ("C:\Windows\Temp\*") do rd /s /q "%%D" 2>nul
del /q /f "C:\Windows\Temp\*" 2>nul

echo [+] Cleaned Temp files

echo.
echo [-] Flushing DNS Cache
ipconfig /flushdns
echo. 

echo [-] Windows Update Settings & Cleaning Cache
echo.

net stop wuauserv >nul 2>&1
net stop UsoSvc >nul 2>&1
rd /s /q "C:\Windows\SoftwareDistribution" >nul 2>&1
md "C:\Windows\SoftwareDistribution" >nul 2>&1
net start wuauserv >nul 2>&1
net start UsoSvc >nul 2>&1

echo [+] Deleted Windows Update Cache and useless files

echo.
echo [-] Clean
echo.

cleanmgr

echo.
echo [+] Cleaned All files
echo.

pause