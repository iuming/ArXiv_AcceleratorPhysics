@echo off
REM ArXiv加速器物理论文分析系统 - Web界面启动脚本
REM Windows批处理版本

echo ======================================================================
echo ArXiv加速器物理论文分析系统 - Web界面
echo ======================================================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 检查Python版本...
python --version

REM 检查必要文件
if not exist "config\settings.yaml" (
    echo 错误: 配置文件不存在，请先运行初始化脚本
    pause
    exit /b 1
)

if not exist "src\web_app.py" (
    echo 错误: Web应用文件不存在
    pause
    exit /b 1
)

REM 检查依赖包
echo 检查依赖包...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 安装Web界面依赖包...
    pip install Flask>=2.3.0 Werkzeug>=2.3.0 Jinja2>=3.1.0 MarkupSafe>=2.1.0
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

REM 创建必要目录
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "templates\web" mkdir templates\web
if not exist "static" mkdir static

echo ----------------------------------------------------------------------
echo 启动Web界面...
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo ----------------------------------------------------------------------

REM 启动Web应用
python start_web.py --host 0.0.0.0 --port 5000

echo.
echo Web服务器已停止
pause
