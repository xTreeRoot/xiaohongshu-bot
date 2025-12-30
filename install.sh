#!/bin/bash
# 小红书自动化工具 - 安装脚本

echo "================================"
echo "  小红书自动化工具 - 快速安装"
echo "================================"
echo ""

# 检查 Python 版本
echo "[1/4] 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✓ Python 版本符合要求: $(python3 --version)"
else
    echo "✗ Python 版本过低，需要 3.7+，当前版本: $python_version"
    exit 1
fi

# 检查是否有虚拟环境
echo ""
echo "[2/4] 设置虚拟环境..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建成功"
else
    echo "✓ 虚拟环境已存在"
fi

# 激活虚拟环境
echo ""
echo "[3/4] 激活虚拟环境并安装依赖..."
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo " 依赖安装成功"
else
    echo " 依赖安装失败"
    exit 1
fi

# 提醒配置
echo ""
echo "[4/4] 配置提醒..."
echo "  请创建并配置个人配置文件："
echo "    1. 复制配置模板:"
echo "       cp config_personal.py.copy config_personal.py"
echo ""
echo "    2. 编辑 config_personal.py，填写你的个人信息"
echo "       - 替换 YOUR_USER_ID 为你的小红书用户ID"
echo ""
echo "你的小红书用户ID可以从个人主页URL获取："
echo "    https://www.xiaohongshu.com/user/profile/YOUR_USER_ID"
echo ""
echo "提示：config_personal.py 不会被提交到Git仓库"
echo ""

echo "================================"
echo "✓ 安装完成！"
echo "================================"
echo ""
echo "使用方法："
echo "  1. 激活虚拟环境: source venv/bin/activate"
echo "  2. 运行测试: python test_xhs.py"
echo ""
echo "首次运行需要手动登录小红书账号"
echo "================================"
