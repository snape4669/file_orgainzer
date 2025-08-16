@echo off
chcp 65001 >nul
title 文件整理工具
echo 正在启动文件整理工具...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.6或更高版本
    echo.
    echo 请访问 https://www.python.org/downloads/ 下载并安装Python
    echo.
    pause
    exit /b 1
)

REM 检查程序文件是否存在
if not exist "file_organizer.py" (
    echo 错误：未找到 file_organizer.py 文件
    echo 请确保批处理文件与Python程序文件在同一目录下
    echo.
    pause
    exit /b 1
)

echo Python版本检查通过
echo 正在启动程序...
echo.

REM 运行Python程序
python file_organizer.py

REM 如果程序异常退出，暂停显示错误信息
if errorlevel 1 (
    echo.
    echo 程序异常退出，请检查错误信息
    pause
)
