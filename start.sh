#!/bin/bash

echo "🚀 ArXiv 加速器物理分析系统启动脚本"
echo "==============================================="

# 检查Python版本
echo "📋 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

python3 --version

# 创建虚拟环境
echo "📦 检查虚拟环境..."
if [ ! -d "venv" ]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 检查环境变量
echo "🔑 检查环境变量..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: OPENAI_API_KEY 环境变量未设置"
    echo "请在运行前设置: export OPENAI_API_KEY='your_api_key_here'"
fi

# 创建目录
echo "📁 创建必要目录..."
mkdir -p data/{papers,analysis,statistics}
mkdir -p logs

echo "✅ 环境准备完成！"

echo "💡 使用说明:"
echo "1. 设置API密钥: export OPENAI_API_KEY='your_key'"
echo "2. 运行分析: python src/main.py"
echo "3. 查看日志: tail -f logs/arxiv_analysis.log"

echo ""
echo "🎯 现在可以运行分析程序了！"
