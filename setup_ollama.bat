@echo off
chcp 65001 >nul
REM Ollama 本地大模型安装脚本 (Windows 版)

echo ================================================
echo Ollama 本地大模型快速安装 (Windows)
echo ================================================
echo.

REM 检查是否已安装 Ollama
where ollama >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Ollama 已安装
    ollama --version
) else (
    echo ❌ Ollama 未安装
    echo.
    echo 请访问以下网址下载 Windows 安装包:
    echo https://ollama.ai/download/windows
    echo.
    echo 下载完成后双击安装，然后重新运行此脚本
    pause
    exit /b 1
)

echo.
echo ================================================
echo 启动 Ollama 服务
echo ================================================

REM 检查服务是否已在运行
curl -s http://localhost:11434/api/tags >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Ollama 服务已在运行
) else (
    echo 正在启动 Ollama 服务...
    start /B ollama serve
    timeout /t 5 /nobreak >nul
    
    REM 再次检查
    curl -s http://localhost:11434/api/tags >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Ollama 服务启动成功
    ) else (
        echo ⚠️ Ollama 服务启动失败
        echo 请手动打开新终端运行: ollama serve
        echo 然后重新运行此脚本
        pause
        exit /b 1
    )
)

echo.
echo ================================================
echo 下载推荐模型
echo ================================================
echo.
echo 推荐模型:
echo 1. qwen2.5:7b - 通义千问 (中文最佳, ~4.7GB)
echo 2. glm4:9b - 智谱 GLM-4 (中文友好, ~5.5GB)
echo 3. llama3.1:8b - Meta Llama (英文为主, ~4.7GB)
echo 4. 跳过下载
echo.
set /p model_choice="请选择要下载的模型 (1-4): "

if "%model_choice%"=="1" (
    echo 下载 通义千问 qwen2.5:7b...
    ollama pull qwen2.5:7b
) else if "%model_choice%"=="2" (
    echo 下载 智谱 GLM-4 glm4:9b...
    ollama pull glm4:9b
) else if "%model_choice%"=="3" (
    echo 下载 Meta Llama llama3.1:8b...
    ollama pull llama3.1:8b
) else (
    echo 跳过下载模型
)

echo.
echo ================================================
echo 安装完成！
echo ================================================
echo.
echo ✅ 配置文件已更新为使用 Ollama
echo.
echo 下一步:
echo 1. 确认 Ollama 服务正在运行: curl http://localhost:11434/api/tags
echo 2. 查看已下载模型: ollama list
echo 3. 运行测试: python test_ai.py
echo.
echo 如果服务未运行，请手动打开新的 CMD 或 PowerShell 运行: ollama serve
echo.
pause
