@echo off
echo 🚀 ArXiv 加速器物理分析系统启动脚本
echo ===============================================

echo 📋 检查Python环境...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 📦 检查虚拟环境...
if not exist "venv" (
    echo 🔧 创建虚拟环境...
    python -m venv venv
)

echo 🔌 激活虚拟环境...
call venv\Scripts\activate.bat

echo 📥 安装依赖包...
pip install -r requirements.txt

echo 🔑 检查环境变量...
if "%OPENAI_API_KEY%"=="" (
    echo ⚠️  警告: OPENAI_API_KEY 环境变量未设置
    echo 请在运行前设置: set OPENAI_API_KEY=your_api_key_here
)

echo 📁 创建必要目录...
if not exist "data" mkdir data
if not exist "data\papers" mkdir data\papers
if not exist "data\analysis" mkdir data\analysis
if not exist "data\statistics" mkdir data\statistics
if not exist "logs" mkdir logs

echo ✅ 环境准备完成！

echo 💡 使用说明:
echo 1. 设置API密钥: set OPENAI_API_KEY=your_key
echo 2. 运行分析: python src\main.py
echo 3. 查看日志: type logs\arxiv_analysis.log

echo.
echo 🎯 现在可以运行分析程序了！
echo 按任意键继续...
pause
