# GitLab CI/CD 配置指南

## 📋 概述

本文档描述如何在 `code.ihep.ac.cn` (GitLab) 上配置 CI/CD 管道，实现：
- 代码质量检查
- 自动化测试
- 每日 ArXiv 论文分析
- Web 演示部署

## 🚀 快速开始

### 1. 推送代码到 GitLab

```bash
# 添加 GitLab 远程仓库（如果还没有）
git remote add gitlab git@code.ihep.ac.cn:mliu/ArXiv_AcceleratorPhysics.git

# 推送代码和 CI 配置
git add .gitlab-ci.yml
git commit -m "添加 GitLab CI/CD 配置"
git push gitlab main
```

### 2. 配置环境变量

在 GitLab 项目中：`Settings` → `CI/CD` → `Variables`

添加以下环境变量：

| 变量名 | 描述 | 类型 | 示例值 |
|--------|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API密钥 | Masked | `sk-...` |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | Masked | `sk-...` |
| `HAI_API_KEY` | HAI API密钥 | Masked | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API密钥 | Masked | `claude-...` |

### 3. 配置定时任务

在 GitLab 项目中：`CI/CD` → `Schedules` → `New schedule`

配置每日论文分析：
- **描述**: Daily ArXiv Analysis
- **Interval Pattern**: `0 0 * * *` (每天 UTC 00:00，北京时间 08:00)
- **Cron timezone**: UTC
- **Target Branch**: main
- **Variables**: 可以添加 `SCHEDULE_TYPE=daily_analysis`

## 📁 文件结构

```
.gitlab-ci.yml          # GitLab CI/CD 主配置文件
docs/
├── GITLAB_CI_SETUP.md  # 本配置指南
└── ...
```

## 🔧 CI/CD 管道阶段

### 1. Lint 阶段 (代码质量检查)
- **Black**: 代码格式化检查
- **isort**: 导入排序检查
- **Flake8**: 代码风格检查
- **Pylint**: 静态代码分析
- **Bandit**: 安全漏洞检查

### 2. Test 阶段 (测试)
- **pytest**: 单元测试和集成测试
- **Coverage**: 代码覆盖率报告

### 3. Analyze 阶段 (论文分析)
- **daily-arxiv-analysis**: 每日论文抓取和分析
- **health-check**: 系统健康检查

### 4. Deploy 阶段 (部署)
- **deploy-web-demo**: 构建和部署 Web 演示
- **pages**: GitLab Pages 部署

## 🎯 触发条件

### 自动触发
- **推送到 main 分支**: 运行 lint、test、deploy
- **合并请求**: 运行 lint、test
- **定时任务**: 运行 analyze 和 health-check
- **修改 .gitlab-ci.yml**: 运行完整管道

### 手动触发
- **Web 界面**: `CI/CD` → `Pipelines` → `Run pipeline`
- **API**: 使用 GitLab API 触发

## 📊 监控和日志

### 查看管道状态
1. 访问项目页面
2. 点击 `CI/CD` → `Pipelines`
3. 查看各个作业的状态和日志

### 下载构建产物
- **覆盖率报告**: 在作业页面下载 `coverage.xml`
- **健康检查报告**: 在 `artifacts` 中下载
- **Web 演示**: 自动部署到 GitLab Pages

## 🔐 权限配置

确保 GitLab Runner 有以下权限：
- **读取代码**: 默认已有
- **推送结果**: 需要配置部署密钥或使用项目访问令牌
- **创建 Issue**: 如需要自动创建分析报告

## 🐛 故障排除

### 常见问题

1. **管道失败**
   - 检查环境变量是否正确配置
   - 查看作业日志确定具体错误
   - 确认 requirements.txt 中的依赖版本

2. **定时任务不执行**
   - 检查 Schedule 配置是否正确
   - 确认项目有足够的 CI/CD 分钟数
   - 查看 `CI/CD` → `Schedules` 页面的执行历史

3. **部署失败**
   - 检查 GitLab Pages 是否启用
   - 确认分支权限设置
   - 查看部署日志

### 调试步骤

1. **本地测试**
   ```bash
   # 运行代码质量检查
   black --check src/
   flake8 src/
   
   # 运行测试
   pytest
   
   # 运行主程序
   cd src && python main.py
   ```

2. **查看管道变量**
   在作业脚本中添加调试信息：
   ```yaml
   script:
     - echo "CI_COMMIT_BRANCH: $CI_COMMIT_BRANCH"
     - echo "CI_PIPELINE_SOURCE: $CI_PIPELINE_SOURCE"
   ```

## 📈 性能优化

### 缓存策略
- **pip 缓存**: 缓存 Python 包安装
- **虚拟环境缓存**: 缓存 `.venv` 目录

### 并行执行
- 多个作业可以并行运行
- 使用 `needs` 关键字控制依赖关系

### 资源限制
```yaml
variables:
  KUBERNETES_CPU_REQUEST: "100m"
  KUBERNETES_CPU_LIMIT: "500m"
  KUBERNETES_MEMORY_REQUEST: "128Mi"
  KUBERNETES_MEMORY_LIMIT: "512Mi"
```

## 🔄 持续改进

### 定期维护
- 更新依赖版本
- 优化管道性能
- 监控资源使用情况

### 扩展功能
- 添加更多测试类型
- 集成代码质量门禁
- 自动生成发布说明

## 📞 支持

如有问题，请联系：
- **作者**: Ming Liu (ming-1018@foxmail.com)
- **机构**: Institute of High Energy Physics, Chinese Academy of Sciences
- **项目地址**: git@code.ihep.ac.cn:mliu/ArXiv_AcceleratorPhysics.git

---

*最后更新: 2025-07-26*
