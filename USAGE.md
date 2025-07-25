# ArXiv 加速器物理论文自动分析系统 - 使用指南

## 📋 项目简介

这是一个基于GitHub Actions的自动化系统，用于每天抓取ArXiv加速器物理分类(physics.acc-ph)的最新论文，并使用大型语言模型(LLM)进行智能分析和分类。

## 🚀 快速开始

### 1. 环境准备

1. **Fork本仓库**到你的GitHub账户
2. **克隆仓库**到本地（可选，用于本地测试）
3. **配置API密钥**

### 2. 配置API密钥

在你的GitHub仓库中设置以下Secrets：

1. 进入仓库 Settings → Secrets and variables → Actions
2. 添加以下Repository secrets：

| Secret名称 | 描述 | 必需性 |
|-----------|------|--------|
| `OPENAI_API_KEY` | OpenAI API密钥 | 必需 |
| `ANTHROPIC_API_KEY` | Anthropic Claude API密钥 | 可选（备用） |

### 3. 启用GitHub Actions

1. 进入仓库的 **Actions** 标签页
2. 如果Actions被禁用，点击 **"I understand my workflows, go ahead and enable them"**
3. 找到 **"Daily ArXiv Accelerator Physics Analysis"** 工作流程
4. 点击 **"Enable workflow"**

### 4. 手动运行测试

首次设置后，建议手动运行一次测试：

1. 进入 Actions → Daily ArXiv Accelerator Physics Analysis
2. 点击 **"Run workflow"**
3. 选择分支并点击 **"Run workflow"**

## ⚙️ 配置选项

### 基本配置

编辑 `config/settings.yaml` 来自定义行为：

```yaml
# 每天处理的最大论文数量
max_papers_per_day: 20

# LLM模型选择
openai_model: "gpt-3.5-turbo"
anthropic_model: "claude-3-sonnet-20240229"

# 分析超时时间（秒）
analysis_timeout: 300
```

### 工作流程调度

编辑 `.github/workflows/daily_arxiv_analysis.yml` 来修改运行时间：

```yaml
on:
  schedule:
    # 每天UTC时间00:00运行 (北京时间08:00)
    - cron: '0 0 * * *'
```

常用时间设置：
- `'0 0 * * *'` - 每天UTC 00:00（北京时间08:00）
- `'0 12 * * *'` - 每天UTC 12:00（北京时间20:00）
- `'0 */6 * * *'` - 每6小时运行一次

## 📁 数据结构

系统会在 `data/` 目录下生成以下结构：

```
data/
├── papers/           # 原始论文数据
│   └── 2024-01-15/
│       ├── papers.json
│       └── [arxiv_id].json
├── analysis/         # 分析结果
│   └── 2024-01-15/
│       ├── analysis_results.json
│       ├── daily_summary.md
│       └── [arxiv_id]_analysis.json
└── statistics/       # 统计数据
    ├── overall_stats.json
    ├── daily_trend.json
    └── category_distribution.json
```

## 📊 分析结果

### 每日总结报告

每天会生成包含以下内容的总结报告：

- 📈 **概览统计**：论文总数、分析成功率
- 📊 **分类分布**：按技术领域分类的统计
- 📚 **论文详情**：每篇论文的简要信息和分析

### 论文分类

系统会将论文自动分类到以下9个类别：

1. **束流动力学** - 束流轨道、稳定性、非线性动力学
2. **射频技术** - 射频腔体、功率系统、超导射频
3. **磁体技术** - 各类磁铁设计、超导/永磁技术
4. **束流诊断** - 位置监测、剖面测量、损失监测
5. **加速器设计** - 总体设计、格点设计、优化
6. **超导技术** - 超导材料、工艺、低温系统
7. **真空技术** - 真空系统、泵浦、超高真空
8. **控制系统** - 控制软件、实时控制、机器保护
9. **其他** - 不属于以上分类的研究

## 🔧 本地开发

### 环境搭建

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/ArXiv_AcceleratorPhysics.git
cd ArXiv_AcceleratorPhysics

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 设置环境变量
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"  # 可选
```

### 本地运行

```bash
# 运行主程序
python src/main.py

# 查看日志
tail -f logs/arxiv_analysis.log
```

### 测试单独模块

```python
# 测试ArXiv抓取
from src.arxiv_fetcher import ArXivFetcher
from src.utils import load_config

config = load_config()
fetcher = ArXivFetcher(config)
papers = await fetcher.fetch_recent_papers()
print(f"抓取到 {len(papers)} 篇论文")
```

## 🐛 故障排除

### 常见问题

1. **API配额超限**
   - 检查API密钥余额
   - 降低 `max_papers_per_day` 设置
   - 增加 `analysis_timeout` 时间

2. **工作流程失败**
   - 检查GitHub Actions日志
   - 验证API密钥是否正确设置
   - 确认网络连接正常

3. **分析质量不佳**
   - 尝试使用更高级的模型（如GPT-4）
   - 调整提示模板(`templates/` 目录)
   - 增加分析超时时间

### 日志查看

- **GitHub Actions日志**：仓库 → Actions → 选择运行记录
- **本地日志**：`logs/arxiv_analysis.log`

### 性能优化

1. **并发处理**：修改 `config/settings.yaml` 中的 `concurrent_analysis`
2. **批处理**：调整 `batch_size` 设置
3. **缓存**：启用 `cache_results` 选项

## 📈 高级用法

### 自定义分析模板

编辑 `templates/analysis_prompt.txt` 来自定义分析要求：

```text
请重点关注以下方面：
1. 技术创新的商业化潜力
2. 与现有技术的对比分析
3. 实验验证的充分性
...
```

### 添加新的分类

1. 修改 `config/settings.yaml` 中的 `categories` 部分
2. 更新 `templates/classification_prompt.txt` 模板
3. 重新训练或调整分类逻辑

### 集成其他数据源

可以扩展 `src/arxiv_fetcher.py` 来支持其他数据源：

```python
class MultiSourceFetcher(ArXivFetcher):
    async def fetch_from_ieee(self):
        # 实现IEEE数据抓取
        pass
    
    async def fetch_from_aps(self):
        # 实现APS数据抓取  
        pass
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- ArXiv.org 提供开放的学术论文API
- OpenAI 和 Anthropic 提供强大的LLM服务
- GitHub Actions 提供免费的CI/CD服务
