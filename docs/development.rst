开发指南
========

本文档为项目开发者提供详细的开发指南和最佳实践。

项目架构
--------

总体架构
~~~~~~~~

::

    ArXiv_AcceleratorPhysics/
    ├── src/                    # 核心源代码
    │   ├── main.py            # 主程序入口
    │   ├── arxiv_fetcher.py   # ArXiv数据抓取
    │   ├── llm_analyzer.py    # LLM分析引擎
    │   ├── data_processor.py  # 数据处理
    │   └── utils.py           # 通用工具
    ├── templates/             # 提示模板
    ├── config/                # 配置文件
    ├── data/                  # 数据存储
    └── tests/                 # 测试代码

模块职责
~~~~~~~~

**main.py**
    - 程序入口点
    - 协调各模块工作流程
    - 错误处理和日志记录

**arxiv_fetcher.py**
    - ArXiv API集成
    - 论文数据抓取
    - 数据清洗和验证

**llm_analyzer.py**
    - 多LLM服务支持
    - 论文内容分析
    - 结果后处理

**data_processor.py**
    - 数据存储管理
    - 统计分析
    - 报告生成

**utils.py**
    - 通用工具函数
    - 配置管理
    - 日志设置

开发环境设置
------------

环境要求
~~~~~~~~

- Python 3.8+
- Git
- 文本编辑器/IDE (推荐VS Code)

克隆和设置
~~~~~~~~~~

.. code-block:: bash

    # 克隆仓库
    git clone https://github.com/iuming/ArXiv_AcceleratorPhysics.git
    cd ArXiv_AcceleratorPhysics

    # 创建虚拟环境
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

    # 安装依赖
    pip install -r requirements.txt
    pip install -r requirements-dev.txt  # 开发依赖

代码规范
--------

代码风格
~~~~~~~~

- 遵循PEP 8
- 使用Black进行代码格式化
- 使用isort进行import排序
- 行长度限制为88字符

命名约定
~~~~~~~~

- **类名**: PascalCase (``ArXivFetcher``)
- **函数/变量**: snake_case (``fetch_papers``)
- **常量**: UPPER_SNAKE_CASE (``MAX_RETRIES``)
- **私有方法**: 前缀下划线 (``_parse_response``)

文档字符串
~~~~~~~~~~

使用Google风格的文档字符串：

.. code-block:: python

    def fetch_papers(self, days_back: int = 1) -> List[Dict]:
        """抓取最近的论文数据.
        
        Args:
            days_back: 回溯天数，默认为1天
            
        Returns:
            包含论文信息的字典列表
            
        Raises:
            APIError: 当API调用失败时
            ValidationError: 当数据验证失败时
        """

测试
----

测试结构
~~~~~~~~

::

    tests/
    ├── __init__.py
    ├── test_arxiv_fetcher.py
    ├── test_llm_analyzer.py
    ├── test_data_processor.py
    ├── test_utils.py
    ├── fixtures/
    │   ├── sample_papers.json
    │   └── sample_config.yaml
    └── integration/
        └── test_full_workflow.py

运行测试
~~~~~~~~

.. code-block:: bash

    # 运行所有测试
    pytest

    # 运行特定测试文件
    pytest tests/test_arxiv_fetcher.py

    # 运行覆盖率测试
    pytest --cov=src --cov-report=html

配置管理
--------

配置文件使用 YAML 格式，位于 ``config/settings.yaml``。

主要配置项包括：

- **app**: 应用基本信息
- **arxiv**: ArXiv API 相关配置
- **llm**: LLM 服务配置
- **storage**: 数据存储配置
- **logging**: 日志配置

Git工作流程
-----------

分支策略
~~~~~~~~

- ``main``: 稳定的生产代码
- ``develop``: 开发分支
- ``feature/feature-name``: 功能分支
- ``hotfix/issue-description``: 紧急修复

提交规范
~~~~~~~~

.. code-block:: bash

    # 功能提交
    git commit -m "feat(analyzer): add DeepSeek API support"

    # Bug修复
    git commit -m "fix(fetcher): handle rate limit errors"

    # 文档更新
    git commit -m "docs: update API setup guide"

    # 重构
    git commit -m "refactor(processor): optimize data storage"

更多详细信息请参考项目中的 ``DEVELOPMENT.md`` 文件。
