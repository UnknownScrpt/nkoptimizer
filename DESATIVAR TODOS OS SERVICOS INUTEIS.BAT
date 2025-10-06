@echo off
color 9
:: Desativa a hibernação do sistema
powercfg -h off
:: Desativa a restauração do sistema
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\SystemRestore" /v "DisableSR" /t REG_DWORD /d "1" /f
:: Desativa a indexação de arquivos (Windows Search)
sc stop "WSearch"
sc config "WSearch" start= disabled
:: Desativa o Windows Defender (Antivírus)
sc stop "WinDefend"
sc config "WinDefend" start= disabled
:: Desativa a compactação de arquivos e pastas (Windows File Compression)
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "UseCompactOnDrive" /t REG_DWORD /d "0" /f
:: Desativa o Windows Update
sc stop "wuauserv"
sc config "wuauserv" start= disabled
:: Desativa a coleta de erros do Windows
sc stop "WerSvc"
sc config "WerSvc" start= disabled
:: Desativa a função de monitoramento remoto
sc stop "RemoteRegistry"
sc config "RemoteRegistry" start= disabled
:: Desativa o serviço de feedback de usuário
sc stop "DiagTrack"
sc config "DiagTrack" start= disabled
:: Desativa a impressão de documentos
sc stop "Spooler"
sc config "Spooler" start= disabled
:: Desativa o serviço de fax
sc stop "Fax"
sc config "Fax" start= disabled
:: Desativa o serviço de rastreamento de links distribuídos
sc stop "TrkWks"
sc config "TrkWks" start= disabled
:: Desativa o serviço de compartilhamento de mídia (Windows Media Player Sharing)
sc stop "WMPNetworkSvc"
sc config "WMPNetworkSvc" start= disabled
:: Desativa o serviço de localização
sc stop "lfsvc"
sc config "lfsvc" start= disabled
:: Desativa o serviço de verificação de compatibilidade de programas
sc stop "PcaSvc"
sc config "PcaSvc" start= disabled
:: Desativa a telemetria da Microsoft
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d "0" /f
:: Desativa a coleta de informações do Windows
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "Start_TrackProgs" /t REG_DWORD /d "0" /f
:: Desativa o Remote Desktop (Serviços de Área de Trabalho Remota)
sc stop "TermService"
sc config "TermService" start= disabled
:: Desativa o serviço de descoberta SSDP (Serviço de Descoberta de Dispositivos)
sc stop "SSDPSRV"
sc config "SSDPSRV" start= disabled
:: Desativa o serviço UPnP (Universal Plug and Play)
sc stop "upnphost"
sc config "upnphost" start= disabled
:: Desativa o serviço de backup do sistema
sc stop "wbengine"
sc config "wbengine" start= disabled
:: Desativa o serviço de sincronização de tempo
sc stop "w32time"
sc config "w32time" start= disabled
:: Desativa a indexação de arquivos para melhorar o desempenho do disco
sc stop "WSearch"
sc config "WSearch" start= disabled
:: Desativa a execução de aplicativos em segundo plano
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" /v "Disabled" /t REG_DWORD /d "1" /f
:: Desativa o Cortana (assistente virtual do Windows)
sc stop "Cortana"
sc config "Cortana" start= disabled
:: Desativa o serviço de dados do OneDrive (se não utilizado)
sc stop "OneDrive"
sc config "OneDrive" start= disabled
:: Desativa o serviço de rede do Bluetooth
sc stop "bthserv"
sc config "bthserv" start= disabled
:: Desativa o serviço de sincronização de contas do Microsoft
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\SettingSync" /v "SyncPolicy" /t REG_DWORD /d "0" /f
:: Desativa a central de ações do Windows (Notificações)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "EnableBalloonTips" /t REG_DWORD /d "0" /f
:: Desativa a barra de tarefas automática
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "TaskbarAutohide" /t REG_DWORD /d "0" /f

echo.
echo As otimizações adicionais foram aplicadas com sucesso!
pause
