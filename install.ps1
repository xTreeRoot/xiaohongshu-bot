# 小红书自动化工具 - Windows 安装脚本

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  小红书自动化工具 - 快速安装" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 版本
Write-Host "[1/4] 检查 Python 版本..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python 已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未找到 Python，请先安装 Python 3.7+" -ForegroundColor Red
    exit 1
}

# 创建虚拟环境
Write-Host ""
Write-Host "[2/4] 设置虚拟环境..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境..."
    python -m venv venv
    Write-Host "✓ 虚拟环境创建成功" -ForegroundColor Green
} else {
    Write-Host "✓ 虚拟环境已存在" -ForegroundColor Green
}

# 激活虚拟环境并安装依赖
Write-Host ""
Write-Host "[3/4] 激活虚拟环境并安装依赖..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# 安装依赖
python -m pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 依赖安装成功" -ForegroundColor Green
} else {
    Write-Host "✗ 依赖安装失败" -ForegroundColor Red
    exit 1
}

# 提醒配置
Write-Host ""
Write-Host "[4/4] 配置提醒..." -ForegroundColor Yellow
Write-Host "  请创建并配置个人配置文件：" -ForegroundColor Yellow
Write-Host "    1. 复制配置模板:"
Write-Host "       Copy-Item config_personal.py.copy config_personal.py"
Write-Host ""
Write-Host "    2. 编辑 config_personal.py，填写你的个人信息"
Write-Host "       - 替换 YOUR_USER_ID 为你的小红书用户ID"
Write-Host ""
Write-Host "你的小红书用户ID可以从个人主页URL获取："
Write-Host "    https://www.xiaohongshu.com/user/profile/YOUR_USER_ID"
Write-Host ""
Write-Host "提示：config_personal.py 不会被提交到Git仓库"
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "✓ 安装完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "使用方法："
Write-Host "  1. 激活虚拟环境: .\venv\Scripts\Activate.ps1"
Write-Host "  2. 运行测试: python test_xhs.py"
Write-Host ""
Write-Host "首次运行需要手动登录小红书账号"
Write-Host "================================" -ForegroundColor Cyan
