常见问题
========

快速开始
--------

我需要什么API密钥？
~~~~~~~~~~~~~~~~~

项目支持多种LLM服务，您至少需要以下其中一个API密钥：

- **OpenAI API密钥** (推荐)
- **DeepSeek API密钥** (推荐，成本较低)
- **HEPAI API密钥** (可选)
- **Anthropic API密钥** (可选)

如何获取API密钥？
~~~~~~~~~~~~~~~

- **OpenAI**: 访问 https://platform.openai.com/api-keys
- **DeepSeek**: 访问 https://platform.deepseek.com/api-keys
- **Anthropic**: 访问 https://console.anthropic.com/

项目运行需要多少费用？
~~~~~~~~~~~~~~~~~~~

费用主要来自LLM API调用：

- **DeepSeek**: 约 $0.001-0.003 每篇论文
- **OpenAI GPT-4**: 约 $0.01-0.03 每篇论文
- 每日20篇论文，月费用大约 $0.6-18（取决于选择的服务）

安装和配置
----------

支持哪些Python版本？
~~~~~~~~~~~~~~~~~

项目要求Python 3.8或更高版本。推荐使用Python 3.9+。

如何在Windows上运行？
~~~~~~~~~~~~~~~~~~~

1. 安装Python 3.8+
2. 打开PowerShell或命令提示符
3. 运行安装命令::

    pip install -r requirements.txt
    python setup.py

如何本地测试API连接？
~~~~~~~~~~~~~~~~~~~

使用提供的测试脚本::

    python test_api.py

使用相关
--------

为什么抓取的论文数量少于预期？
~~~~~~~~~~~~~~~~~~~~~~~~~

可能的原因：

1. **ArXiv发布时间**: 加速器物理领域每日发布论文数量有限
2. **查询范围**: 项目专门针对 ``physics.acc-ph`` 分类
3. **去重机制**: 自动过滤重复或已处理的论文
4. **配置限制**: 检查 ``config/settings.yaml`` 中的 ``max_papers_per_day`` 设置

如何修改分析提示？
~~~~~~~~~~~~~~~

编辑以下模板文件：

- ``templates/analysis_prompt.txt`` - 主要分析提示
- ``templates/classification_prompt.txt`` - 分类提示

分析结果存储在哪里？
~~~~~~~~~~~~~~~~~

- **论文数据**: ``data/papers/YYYY-MM-DD/``
- **分析结果**: ``data/analysis/YYYY-MM-DD/``
- **统计信息**: ``data/statistics/``

故障排除
--------

出现 "API密钥无效" 错误
~~~~~~~~~~~~~~~~~~~~

1. 确认API密钥正确复制（没有额外空格）
2. 检查API密钥是否有足够的配额
3. 验证API密钥对应的服务是否可用
4. 检查网络连接

程序运行中断怎么办？
~~~~~~~~~~~~~~~~~

1. 检查日志文件 ``logs/arxiv_analysis.log``
2. 确认API配额是否用完
3. 检查网络连接稳定性
4. 重新运行通常会自动跳过已处理的论文

内存使用过高
~~~~~~~~~~~

1. 减少 ``max_papers_per_day`` 设置
2. 确保系统有足够的可用内存
3. 考虑分批处理大量论文

更多详细信息请参考项目中的 ``FAQ.md`` 文件。
