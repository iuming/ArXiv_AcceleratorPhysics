ArXiv 加速器物理分析系统
=======================

欢迎使用 ArXiv 加速器物理分析系统！这是一个用于自动获取、分析和处理 ArXiv 上加速器物理相关论文的智能系统。

.. toctree::
   :maxdepth: 2
   :caption: 目录:

   installation
   usage
   api_reference
   development
   faq

系统概述
--------

本系统提供以下主要功能：

* 自动从 ArXiv 获取加速器物理相关论文
* 使用 LLM 进行论文内容分析和分类
* 生成详细的分析报告和统计数据
* 支持多种数据输出格式

快速开始
--------

1. 安装依赖::

    pip install -r requirements.txt

2. 配置 API 密钥::

    export OPENAI_API_KEY=your_openai_api_key
    # 或者
    export DEEPSEEK_API_KEY=your_deepseek_api_key

3. 运行系统::

    python src/main.py

索引和表格
==========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
