# ArXiv 加速器物理论文自动解读系统

这个项目实现了一个自动化工作流程，用于：
- 每天自动抓取ArXiv加速器物理分类的最新论文
- 使用LLM进行论文内容解读和分类
- 自动保存结果到GitHub仓库

## 功能特性

- 🤖 自动化GitHub Actions工作流程
- 📄 ArXiv API集成
- 🧠 LLM驱动的论文解读
- 📊 智能分类系统
- 💾 结构化数据存储
- 📈 可视化统计报告

## 项目结构

```
├── .github/
│   └── workflows/
│       └── daily_arxiv_analysis.yml    # GitHub Actions工作流程
├── src/
│   ├── arxiv_fetcher.py               # ArXiv论文抓取
│   ├── llm_analyzer.py                # LLM分析引擎
│   ├── data_processor.py              # 数据处理
│   └── utils.py                       # 工具函数
├── templates/
│   ├── analysis_prompt.txt            # LLM分析提示模板
│   └── classification_prompt.txt     # 分类提示模板
├── data/
│   ├── papers/                        # 论文数据存储
│   ├── analysis/                      # 分析结果
│   └── statistics/                    # 统计数据
├── config/
│   └── settings.yaml                  # 配置文件
└── requirements.txt                   # Python依赖
```

## 快速开始

1. Fork此仓库
2. 配置环境变量（详见配置章节）
3. 启用GitHub Actions
4. 工作流程将每天自动运行

## 配置

在GitHub仓库的Settings > Secrets中添加以下secrets：
- `OPENAI_API_KEY`: OpenAI API密钥
- `ANTHROPIC_API_KEY`: Anthropic API密钥（可选）

## 使用方法

工作流程每天UTC时间00:00自动运行，也可以手动触发。

分析结果将保存在：
- `data/papers/YYYY-MM-DD/` - 原始论文数据
- `data/analysis/YYYY-MM-DD/` - LLM分析结果
- `data/statistics/` - 统计信息

## 贡献

欢迎提交Issue和Pull Request！
