# 开发指南

本文档为项目开发者提供详细的开发指南和最佳实践。

## 🏗️ 项目架构

### 总体架构
```
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
```

### 模块职责

#### `main.py`
- 程序入口点
- 协调各模块工作流程
- 错误处理和日志记录

#### `arxiv_fetcher.py`
- ArXiv API集成
- 论文数据抓取
- 数据清洗和验证

#### `llm_analyzer.py`
- 多LLM服务支持
- 论文内容分析
- 结果后处理

#### `data_processor.py`
- 数据存储管理
- 统计分析
- 报告生成

#### `utils.py`
- 通用工具函数
- 配置管理
- 日志设置

## 🛠️ 开发环境设置

### 1. 环境要求
- Python 3.8+
- Git
- 文本编辑器/IDE (推荐VS Code)

### 2. 克隆和设置
```bash
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
```

### 3. 开发工具配置

#### VS Code设置
推荐的VS Code扩展：
- Python
- Pylance
- Python Docstring Generator
- GitLens
- Black Formatter

#### `.vscode/settings.json`
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## 📝 代码规范

### 代码风格
- 遵循PEP 8
- 使用Black进行代码格式化
- 使用isort进行import排序
- 行长度限制为88字符

### 命名约定
- **类名**: PascalCase (`ArXivFetcher`)
- **函数/变量**: snake_case (`fetch_papers`)
- **常量**: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **私有方法**: 前缀下划线 (`_parse_response`)

### 文档字符串
使用Google风格的文档字符串：

```python
def fetch_papers(self, days_back: int = 1) -> List[Dict]:
    """抓取最近的论文数据.
    
    Args:
        days_back: 回溯天数，默认为1天
        
    Returns:
        包含论文信息的字典列表
        
    Raises:
        APIError: 当API调用失败时
        ValidationError: 当数据验证失败时
        
    Example:
        >>> fetcher = ArXivFetcher(config)
        >>> papers = await fetcher.fetch_papers(2)
        >>> len(papers)
        15
    """
```

### 类型提示
所有函数都应该有类型提示：

```python
from typing import Dict, List, Optional, Union, Any
import asyncio

async def process_papers(
    papers: List[Dict[str, Any]], 
    config: Dict[str, Union[str, int]]
) -> Optional[Dict[str, Any]]:
    """处理论文数据."""
    pass
```

## 🧪 测试

### 测试结构
```
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
```

### 单元测试示例
```python
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.arxiv_fetcher import ArXivFetcher

class TestArXivFetcher:
    """ArXivFetcher测试类."""
    
    @pytest.fixture
    def config(self):
        """测试配置."""
        return {
            "max_papers_per_day": 10,
            "category": "physics.acc-ph"
        }
    
    @pytest.fixture
    def fetcher(self, config):
        """ArXivFetcher实例."""
        return ArXivFetcher(config)
    
    @pytest.mark.asyncio
    async def test_fetch_papers_success(self, fetcher):
        """测试成功抓取论文."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock API响应
            mock_response = Mock()
            mock_response.text.return_value = asyncio.coroutine(
                lambda: self._get_sample_xml()
            )()
            mock_get.return_value.__aenter__.return_value = mock_response
            
            papers = await fetcher.fetch_papers()
            
            assert len(papers) > 0
            assert 'title' in papers[0]
            assert 'abstract' in papers[0]
    
    def _get_sample_xml(self):
        """返回示例XML响应."""
        return """<?xml version="1.0" encoding="UTF-8"?>
        <feed>
            <entry>
                <title>Sample Paper</title>
                <summary>Sample abstract</summary>
            </entry>
        </feed>"""
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_arxiv_fetcher.py

# 运行覆盖率测试
pytest --cov=src --cov-report=html

# 运行特定标记的测试
pytest -m "not slow"
```

## 🔄 异步编程

### 异步最佳实践
```python
import asyncio
import aiohttp
from typing import List, Dict

class AsyncProcessor:
    """异步处理器示例."""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        """异步上下文管理器入口."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口."""
        if self.session:
            await self.session.close()
    
    async def process_batch(self, items: List[Dict]) -> List[Dict]:
        """并发处理批次数据."""
        tasks = [self._process_item(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"处理失败: {result}")
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _process_item(self, item: Dict) -> Dict:
        """处理单个项目."""
        # 模拟异步处理
        await asyncio.sleep(0.1)
        return {"processed": item}

# 使用示例
async def main():
    async with AsyncProcessor() as processor:
        results = await processor.process_batch(items)
    return results
```

## 🔧 配置管理

### 配置结构
```yaml
# config/settings.yaml
app:
  name: "ArXiv_AcceleratorPhysics"
  version: "1.0.0"
  
arxiv:
  base_url: "http://export.arxiv.org/api/query"
  category: "physics.acc-ph"
  max_papers_per_day: 20
  retry_count: 3
  timeout: 30

llm:
  providers:
    - name: "deepseek"
      enabled: true
      model: "deepseek-chat"
      max_tokens: 4096
    - name: "openai"
      enabled: false
      model: "gpt-4"
      max_tokens: 4096

storage:
  base_path: "data"
  compression: true
  backup_count: 7

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/arxiv_analysis.log"
```

### 配置加载
```python
import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """加载配置文件."""
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 环境变量覆盖
    config = _apply_env_overrides(config)
    
    return config

def _apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """应用环境变量覆盖."""
    import os
    
    # 示例：ARXIV_MAX_PAPERS -> config.arxiv.max_papers_per_day
    env_mappings = {
        'ARXIV_MAX_PAPERS': ('arxiv', 'max_papers_per_day'),
        'LLM_PROVIDER': ('llm', 'default_provider'),
    }
    
    for env_key, (section, key) in env_mappings.items():
        if env_value := os.getenv(env_key):
            config[section][key] = env_value
    
    return config
```

## 🚦 错误处理

### 自定义异常
```python
class ArXivError(Exception):
    """ArXiv相关错误基类."""
    pass

class APIError(ArXivError):
    """API调用错误."""
    
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class ValidationError(ArXivError):
    """数据验证错误."""
    pass

class ProcessingError(ArXivError):
    """数据处理错误."""
    pass
```

### 错误处理模式
```python
import logging
from typing import Optional, Dict, Any
from functools import wraps

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """重试装饰器."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"第{attempt + 1}次尝试失败: {e}, "
                            f"{delay}秒后重试..."
                        )
                        await asyncio.sleep(delay * (2 ** attempt))
                    else:
                        logger.error(f"所有重试都失败了: {e}")
            
            raise last_exception
        return wrapper
    return decorator

# 使用示例
@retry_on_failure(max_retries=3, delay=2.0)
async def fetch_with_retry(url: str) -> Dict[str, Any]:
    """带重试的数据抓取."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise APIError(f"HTTP {response.status}", response.status)
            return await response.json()
```

## 📊 日志记录

### 日志配置
```python
import logging
import logging.handlers
from pathlib import Path

def setup_logging(
    level: str = "INFO",
    log_file: str = "logs/arxiv_analysis.log",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """设置日志记录."""
    
    # 创建日志目录
    log_path = Path(log_file)
    log_path.parent.mkdir(exist_ok=True)
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(message)s'
    )
    
    # 根日志器
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # 文件处理器（轮转）
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# 使用示例
logger = setup_logging()

class Component:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def process(self):
        self.logger.info("开始处理...")
        try:
            # 处理逻辑
            self.logger.debug("处理详细信息...")
            result = self._do_work()
            self.logger.info(f"处理完成，结果: {result}")
            return result
        except Exception as e:
            self.logger.error(f"处理失败: {e}", exc_info=True)
            raise
```

## 🔄 Git工作流程

### 分支策略
- `main`: 稳定的生产代码
- `develop`: 开发分支
- `feature/feature-name`: 功能分支
- `hotfix/issue-description`: 紧急修复

### 提交规范
```bash
# 功能提交
git commit -m "feat(analyzer): add DeepSeek API support"

# Bug修复
git commit -m "fix(fetcher): handle rate limit errors"

# 文档更新
git commit -m "docs: update API setup guide"

# 重构
git commit -m "refactor(processor): optimize data storage"
```

### 发布流程
```bash
# 1. 确保在develop分支
git checkout develop
git pull origin develop

# 2. 创建发布分支
git checkout -b release/1.1.0

# 3. 更新版本号和文档
# 编辑setup.py, __init__.py等文件

# 4. 提交发布准备
git commit -m "chore: prepare release 1.1.0"

# 5. 合并到main
git checkout main
git merge release/1.1.0

# 6. 创建标签
git tag -a v1.1.0 -m "Release version 1.1.0"

# 7. 推送
git push origin main --tags

# 8. 合并回develop
git checkout develop
git merge main
git push origin develop
```

## 📦 部署和发布

### GitHub Actions
项目使用GitHub Actions进行CI/CD：

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 src tests --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Test with pytest
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

### 版本管理
使用`semantic-release`自动化版本管理：

```json
// package.json
{
  "release": {
    "branches": ["main"],
    "plugins": [
      "@semantic-release/commit-analyzer",
      "@semantic-release/release-notes-generator",
      "@semantic-release/changelog",
      "@semantic-release/github"
    ]
  }
}
```

## 🧩 扩展开发

### 添加新的LLM提供商
1. 在`llm_analyzer.py`中添加新的client类
2. 实现标准接口
3. 更新配置支持
4. 添加测试

### 添加新的数据源
1. 创建新的fetcher模块
2. 实现统一的数据接口
3. 更新数据处理流程
4. 添加配置选项

### 添加新的分析功能
1. 扩展分析提示模板
2. 更新分析结果结构
3. 添加新的统计指标
4. 更新可视化组件

## 📚 学习资源

### Python异步编程
- [Python asyncio官方文档](https://docs.python.org/3/library/asyncio.html)
- [Real Python: Async IO in Python](https://realpython.com/async-io-python/)

### 测试
- [pytest官方文档](https://docs.pytest.org/)
- [Python Testing 101](https://realpython.com/python-testing/)

### 类型提示
- [mypy官方文档](https://mypy.readthedocs.io/)
- [Python Type Checking Guide](https://realpython.com/python-type-checking/)

---

这个开发指南会持续更新。如果您有任何问题或建议，请通过GitHub Issues联系我们。
