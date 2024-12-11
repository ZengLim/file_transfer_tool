@echo off
setlocal enabledelayedexpansion

:: 定义起始端口和需要的端口数量
set start_port=34000
set num_ports=65

:: 使用 for 循环递减端口号并执行对应的 Python 指令
for /L %%i in (0,1,%num_ports%) do (
    set /a port=%start_port% - %%i
    start python E:\work\file_transfer\file_transfer_client.py !port! !num_ports!
)

endlocal
