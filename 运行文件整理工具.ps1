# 文件整理工具启动脚本
# PowerShell版本

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "正在启动文件整理工具..." -ForegroundColor Green
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python版本检查通过: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python未正确安装"
    }
} catch {
    Write-Host "错误：未找到Python，请先安装Python 3.6或更高版本" -ForegroundColor Red
    Write-Host ""
    Write-Host "请访问 https://www.python.org/downloads/ 下载并安装Python" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

# 检查程序文件是否存在
if (-not (Test-Path "file_organizer.py")) {
    Write-Host "错误：未找到 file_organizer.py 文件" -ForegroundColor Red
    Write-Host "请确保PowerShell脚本与Python程序文件在同一目录下" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "程序文件检查通过" -ForegroundColor Green
Write-Host "正在启动程序..." -ForegroundColor Green
Write-Host ""

# 运行Python程序
try {
    python file_organizer.py
} catch {
    Write-Host ""
    Write-Host "程序异常退出，请检查错误信息" -ForegroundColor Red
    Read-Host "按回车键退出"
}
