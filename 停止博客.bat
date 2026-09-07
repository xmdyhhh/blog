@echo off
chcp 65001 >nul
title 停止博客
color 0C

echo ============================================
echo    停止开源软件实验博客
echo ============================================
echo.

cd /d "%~dp0"

:: 查找并停止占用 2368 端口的进程
echo [信息] 正在查找 Ghost 进程...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":2368"') do (
    echo [信息] 找到进程 PID: %%a，正在停止...
    taskkill /F /PID %%a >nul 2>&1
)

:: 也停止所有 node 进程（谨慎，可能影响其他 node 程序）
:: taskkill /F /IM node.exe >nul 2>&1

timeout /t 2 /nobreak >nul

:: 验证是否停止
netstat -ano | findstr ":2368" >nul
if %errorlevel%==0 (
    echo [警告] 端口 2368 仍被占用
) else (
    echo [成功] Ghost 已停止，端口 2368 已释放
)

echo.
pause
