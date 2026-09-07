@echo off
chcp 65001 >nul
title 开源软件实验博客 - 一键启动
color 0A

echo ============================================
echo    开源软件实验博客系统 - 一键启动
echo ============================================
echo.

cd /d "%~dp0"

:: 检查 Node.js 22 便携版
if not exist "tools\node22\node-v22.23.1-win-x64\node.exe" (
    echo [错误] 未找到 Node.js 22 便携版！
    echo 请确保 tools\node22\node-v22.23.1-win-x64\node.exe 存在
    echo.
    pause
    exit /b 1
)

:: 设置 PATH
set "PATH=%~dp0tools\node22\node-v22.23.1-win-x64;%PATH%"
set NODE_TLS_REJECT_UNAUTHORIZED=0

echo [信息] Node.js 版本:
node --version
echo.

:: 检查端口 2368
netstat -ano | findstr ":2368" >nul
if %errorlevel%==0 (
    echo [警告] 端口 2368 已被占用，Ghost 可能已在运行
    echo.
    echo 正在打开浏览器...
    start http://localhost:2368
    echo.
    echo 按任意键退出...
    pause >nul
    exit /b 0
)

:: 检查 runtime 目录
if not exist "runtime\config.development.json" (
    echo [错误] 未找到 Ghost 配置文件！
    echo 请先按照 README.md 完成 Ghost 安装
    echo.
    pause
    exit /b 1
)

echo [信息] 正在启动 Ghost...
echo [信息] 启动后将自动打开浏览器
echo [信息] 前台地址: http://localhost:2368
echo [信息] 管理后台: http://localhost:2368/ghost
echo.
echo [提示] 关闭此窗口将停止 Ghost
echo ============================================
echo.

cd runtime
start "" http://localhost:2368
node "..\node_modules\ghost-cli\bin\ghost" run --development

echo.
echo Ghost 已停止
pause
