安装指南
========

系统要求
--------

* Python 3.8 或更高版本
* 互联网连接（用于访问 ArXiv API 和 LLM 服务）

安装步骤
--------

1. 克隆仓库::

    git clone https://github.com/iuming/ArXiv_AcceleratorPhysics.git
    cd ArXiv_AcceleratorPhysics

2. 创建虚拟环境（推荐）::

    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Linux/macOS
    source venv/bin/activate

3. 安装依赖::

    pip install -r requirements.txt

4. 配置环境变量::

    # 复制配置文件
    cp config/settings.yaml.example config/settings.yaml
    
    # 编辑配置文件，添加你的 API 密钥
    # OPENAI_API_KEY 或 DEEPSEEK_API_KEY

验证安装
--------

运行健康检查脚本验证安装是否成功::

    python health_check.py

如果一切正常，你应该看到系统状态检查通过的消息。
