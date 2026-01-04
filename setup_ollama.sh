#!/bin/bash
# Ollama 本地大模型安装脚本

echo "================================================"
echo "Ollama 本地大模型快速安装"
echo "================================================"
echo ""

# 检查是否已安装 Ollama
if command -v ollama &> /dev/null; then
    echo " Ollama 已安装"
    ollama --version
else
    echo " Ollama 未安装"
    echo ""
    echo "请选择安装方式："
    echo "1. 使用 Homebrew 安装（推荐）"
    echo "2. 下载安装包"
    echo ""
    read -p "请输入选项 (1-2): " choice
    
    if [ "$choice" = "1" ]; then
        echo "使用 Homebrew 安装 Ollama..."
        brew install ollama
    else
        echo "请访问 https://ollama.ai/download 下载安装包"
        exit 1
    fi
fi

echo ""
echo "================================================"
echo "启动 Ollama 服务"
echo "================================================"

# 在后台启动 Ollama 服务
echo "正在后台启动 Ollama 服务..."
nohup ollama serve > /tmp/ollama.log 2>&1 &
sleep 3

# 检查服务是否启动
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo " Ollama 服务启动成功"
else
    echo " Ollama 服务启动失败，请手动运行: ollama serve"
fi

echo ""
echo "================================================"
echo "下载推荐模型"
echo "================================================"
echo ""
echo "推荐模型："
echo "1. qwen2.5:7b - 通义千问 (中文最佳, ~4.7GB)"
echo "2. glm4:9b - 智谱 GLM-4 (中文友好, ~5.5GB)"
echo "3. llama3.1:8b - Meta Llama (英文为主, ~4.7GB)"
echo ""
read -p "请选择要下载的模型 (1-3): " model_choice

case $model_choice in
    1)
        echo "下载 通义千问 qwen2.5:7b..."
        ollama pull qwen2.5:7b
        ;;
    2)
        echo "下载 智谱 GLM-4 glm4:9b..."
        ollama pull glm4:9b
        ;;
    3)
        echo "下载 Meta Llama llama3.1:8b..."
        ollama pull llama3.1:8b
        ;;
    *)
        echo "无效选项，跳过下载"
        ;;
esac

echo ""
echo "================================================"
echo "安装完成！"
echo "================================================"
echo ""
echo " 配置文件已更新为使用 Ollama"
echo ""
echo "下一步："
echo "1. 确认 Ollama 服务正在运行: curl http://localhost:11434/api/tags"
echo "2. 查看已下载模型: ollama list"
echo "3. 运行测试: python test_ai.py"
echo ""
echo "如果服务未运行，请手动启动: ollama serve"
echo ""
