使用指南
========

基本用法
--------

系统可以通过多种方式运行：

命令行界面
~~~~~~~~~~

直接运行主程序::

    python src/main.py

这将启动默认的论文获取和分析流程。

配置选项
--------

系统配置通过 `config/settings.yaml` 文件进行管理。主要配置项包括：

API 设置
~~~~~~~~

* `openai_api_key`: OpenAI API 密钥
* `deepseek_api_key`: DeepSeek API 密钥  
* `model_name`: 使用的 LLM 模型名称

ArXiv 设置
~~~~~~~~~~

* `categories`: 要检索的 ArXiv 分类
* `max_results`: 每次查询的最大结果数
* `date_range`: 检索的日期范围

输出设置
~~~~~~~~

* `output_format`: 输出格式（json, markdown）
* `save_raw_data`: 是否保存原始数据
* `generate_summary`: 是否生成摘要报告

高级功能
--------

批量处理
~~~~~~~~

可以使用脚本进行批量处理::

    python src/main.py --batch --config custom_config.yaml

API 测试
~~~~~~~~

使用测试脚本验证 API 连接::

    python test_api.py

数据分析
~~~~~~~~

查看项目统计信息::

    python project_stats.py

故障排除
--------

常见问题及解决方案请参考 :doc:`faq` 部分。
