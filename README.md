# ArXiv 加速器物理论文自动解读系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

一个基于人工智能的自动化系统，专门用于抓取、分析和解读ArXiv加速器物理分类的最新论文。

## 🚀 功能特性

- 🤖 **自动化工作流程**: 基于GitHub Actions的每日自动执行
- 📄 **ArXiv API集成**: 专门抓取加速器物理(physics.acc-ph)分类论文
- 🧠 **多LLM支持**: 支持OpenAI、DeepSeek、HEPAI、Anthropic等多种LLM服务
- 📊 **智能分类**: 自动对论文进行主题分类和技术标签
- 💾 **结构化存储**: JSON格式存储，便于数据分析和可视化
- 📈 **统计报告**: 自动生成每日、每周和月度统计报告
- 🔍 **去重机制**: 智能识别和处理重复论文

## 📁 项目结构

```
ArXiv_AcceleratorPhysics/
├── .github/
│   └── workflows/
│       └── daily_arxiv_analysis.yml    # GitHub Actions工作流程
├── src/
│   ├── __init__.py                     # 包初始化
│   ├── main.py                         # 主程序入口
│   ├── arxiv_fetcher.py               # ArXiv论文抓取模块
│   ├── llm_analyzer.py                # LLM分析引擎
│   ├── llm_analyzer_new.py           # 新版LLM分析器
│   ├── data_processor.py              # 数据处理模块
│   └── utils.py                       # 工具函数库
├── templates/
│   ├── analysis_prompt.txt            # LLM分析提示模板
│   └── classification_prompt.txt     # 分类提示模板
├── data/
│   ├── papers/                        # 论文原始数据
│   ├── analysis/                      # 分析结果
│   └── statistics/                    # 统计数据
├── config/
│   └── settings.yaml                  # 系统配置文件
├── logs/                              # 日志文件目录
├── docs/                              # 项目文档
├── requirements.txt                   # Python依赖包
├── setup.py                          # 项目安装脚本
├── test_api.py                       # API连接测试
└── README.md                         # 项目说明
```

## 🛠️ 安装与配置

### 环境要求

- Python 3.8+
- 有效的LLM API密钥（OpenAI、DeepSeek、HEPAI或Anthropic）

### 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/iuming/ArXiv_AcceleratorPhysics.git
   cd ArXiv_AcceleratorPhysics
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行初始化脚本**
   ```bash
   python setup.py
   ```

4. **配置API密钥**
   
   在GitHub仓库的Settings > Secrets中添加以下secrets：
   - `OPENAI_API_KEY`: OpenAI API密钥
   - `DEEPSEEK_API_KEY`: DeepSeek API密钥（推荐）
   - `HEPAI_API_KEY`: HEPAI API密钥（可选）
   - `ANTHROPIC_API_KEY`: Anthropic API密钥（可选）

5. **启用GitHub Actions**
   
   Fork仓库后，在Actions页面启用工作流程。

## 📊 使用方法

### 自动运行
工作流程每天UTC时间00:00自动运行，抓取前一天发布的论文。

### 手动运行
在GitHub Actions页面可以手动触发工作流程。

### 本地运行
```bash
python src/main.py
```

## 📈 数据输出

分析结果按日期组织存储：

- **论文数据**: `data/papers/YYYY-MM-DD/papers.json`
- **分析结果**: `data/analysis/YYYY-MM-DD/analysis_results.json`
- **每日摘要**: `data/analysis/YYYY-MM-DD/daily_summary.md`
- **统计数据**: `data/statistics/`

## 🔧 配置选项

详细配置请参考 `config/settings.yaml`：

- 最大论文数量限制
- LLM服务提供商选择
- 分析深度设置
- 输出格式配置

## 📚 API文档

详细的API文档请参考：
- [使用指南](USAGE.md)
- [API设置指南](API_SETUP_GUIDE.md)
- [项目概述](PROJECT_SUMMARY.md)

## 🧪 测试

运行API连接测试：
```bash
python test_api.py
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目基于MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

**Ming Liu** - *项目创建者和维护者*

- 📧 Email: ming-1018@foxmail.com
- 🏢 Institution: Institute of High Energy Physics, Chinese Academy of Sciences
- 🔬 Research Focus: Accelerator Physics, Machine Learning Applications

## 🙏 致谢

- ArXiv.org 提供的开放获取科学文献
- OpenAI、DeepSeek、HEPAI、Anthropic 提供的LLM服务
- GitHub Actions 提供的CI/CD平台

## 📞 支持

如果您在使用过程中遇到问题，请：

1. 查看[常见问题](docs/FAQ.md)
2. 搜索已有的[Issues](https://github.com/iuming/ArXiv_AcceleratorPhysics/issues)
3. 创建新的Issue描述您的问题

---

⭐ 如果这个项目对您有帮助，请给它一个星标！
