# 贡献指南

感谢您对ArXiv加速器物理论文自动解读系统的关注！我们欢迎并鼓励社区贡献。

## 如何贡献

### 报告Bug

在报告Bug之前，请：

1. 检查[已知问题](https://github.com/iuming/ArXiv_AcceleratorPhysics/issues)确保该问题尚未被报告
2. 确保您使用的是最新版本
3. 在沙盒环境中重现该问题

提交Bug报告时，请包含：

- 清晰的问题描述
- 重现步骤
- 预期行为vs实际行为
- 环境信息（操作系统、Python版本等）
- 相关日志和错误消息

### 功能请求

我们欢迎新功能建议！请：

1. 在提交功能请求前搜索现有issue
2. 清楚描述功能的用途和价值
3. 如果可能，提供实现建议

### 代码贡献

#### 开发环境设置

1. Fork仓库
2. 克隆您的fork：
   ```bash
   git clone https://github.com/YOUR_USERNAME/ArXiv_AcceleratorPhysics.git
   cd ArXiv_AcceleratorPhysics
   ```

3. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

4. 安装开发依赖：
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # 如果存在
   ```

5. 运行测试确保环境正常：
   ```bash
   python test_api.py
   ```

#### 代码标准

- 使用Python 3.8+
- 遵循PEP 8代码风格
- 使用类型提示
- 编写清晰的文档字符串
- 添加必要的单元测试

#### 提交流程

1. 创建功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 进行更改，确保：
   - 代码符合项目标准
   - 添加或更新相关测试
   - 更新文档（如需要）

3. 提交更改：
   ```bash
   git add .
   git commit -m "Add: clear description of changes"
   ```

4. 推送到您的fork：
   ```bash
   git push origin feature/your-feature-name
   ```

5. 创建Pull Request

#### Pull Request指南

- 使用清晰描述性的标题
- 在PR描述中解释更改的原因和内容
- 链接相关的issue（如果有）
- 确保所有测试通过
- 保持PR专注于单一功能或修复

## 代码风格

### Python代码规范

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: example.py
Author: Your Name
Email: your.email@example.com
Institution: Your Institution
Created: Date
Description: Brief description of the file's purpose

Modification History:
- Date: Initial creation
- Date: Description of changes
"""

import asyncio
from typing import Dict, List, Optional

class ExampleClass:
    """Example class with proper documentation."""
    
    def __init__(self, config: Dict):
        """Initialize the class.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    async def example_method(self, param: str) -> Optional[str]:
        """Example async method.
        
        Args:
            param: Input parameter
            
        Returns:
            Processed result or None
            
        Raises:
            ValueError: If param is invalid
        """
        if not param:
            raise ValueError("Parameter cannot be empty")
        
        return f"Processed: {param}"
```

### 文档字符串

使用Google风格的文档字符串：

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of the function.
    
    Longer description if needed, explaining the function's
    behavior, algorithms used, etc.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        TypeError: When param2 is not an integer
        
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

## 测试

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_arxiv_fetcher.py

# 运行覆盖率测试
python -m pytest --cov=src
```

### 编写测试

- 为新功能编写单元测试
- 测试文件命名：`test_*.py`
- 测试函数命名：`test_*`
- 使用descriptive测试名称

```python
import pytest
from src.arxiv_fetcher import ArXivFetcher

class TestArXivFetcher:
    """Test cases for ArXivFetcher class."""
    
    def test_fetch_papers_valid_response(self):
        """Test fetching papers with valid API response."""
        # Test implementation
        pass
    
    def test_fetch_papers_invalid_api_key(self):
        """Test handling of invalid API key."""
        # Test implementation
        pass
```

## 版本控制

### 分支策略

- `main`: 稳定的生产代码
- `develop`: 开发分支
- `feature/feature-name`: 功能分支
- `hotfix/issue-description`: 紧急修复分支

### 提交消息格式

使用传统的提交消息格式：

```
type(scope): description

[optional body]

[optional footer]
```

类型：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 添加测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(analyzer): add support for multiple LLM providers

- Added DeepSeek API integration
- Implemented fallback mechanism for API failures
- Updated configuration schema

Closes #123
```

## 发布流程

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建发布标签
4. 创建GitHub发布

## 社区准则

### 行为准则

我们承诺为每个人提供友好、安全和欢迎的环境。请：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 专注于对社区最有益的事情
- 对其他社区成员表现出同理心

### 获取帮助

- 📧 邮件：ming-1018@foxmail.com
- 💬 Issues：[GitHub Issues](https://github.com/iuming/ArXiv_AcceleratorPhysics/issues)
- 📚 文档：[项目文档](docs/)

## 致谢

感谢所有贡献者的努力！您的贡献使这个项目变得更好。

---

再次感谢您的贡献！🎉
