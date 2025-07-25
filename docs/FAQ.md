# 常见问题解答 (FAQ)

## 🚀 快速开始

### Q: 我需要什么API密钥？
**A:** 项目支持多种LLM服务，您至少需要以下其中一个API密钥：
- **OpenAI API密钥** (推荐)
- **DeepSeek API密钥** (推荐，成本较低)
- **HEPAI API密钥** (可选)
- **Anthropic API密钥** (可选)

### Q: 如何获取API密钥？
**A:** 
- **OpenAI**: 访问 https://platform.openai.com/api-keys
- **DeepSeek**: 访问 https://platform.deepseek.com/api-keys
- **Anthropic**: 访问 https://console.anthropic.com/

### Q: 项目运行需要多少费用？
**A:** 费用主要来自LLM API调用：
- **DeepSeek**: 约 $0.001-0.003 每篇论文
- **OpenAI GPT-4**: 约 $0.01-0.03 每篇论文
- 每日20篇论文，月费用大约 $0.6-18（取决于选择的服务）

## 🔧 安装和配置

### Q: 支持哪些Python版本？
**A:** 项目要求Python 3.8或更高版本。推荐使用Python 3.9+。

### Q: 如何在Windows上运行？
**A:** 
1. 安装Python 3.8+
2. 打开PowerShell或命令提示符
3. 运行安装命令：
   ```powershell
   pip install -r requirements.txt
   python setup.py
   ```

### Q: GitHub Actions无法运行怎么办？
**A:** 请检查：
1. 是否已在仓库Settings > Secrets中配置API密钥
2. 是否已启用GitHub Actions
3. 是否有足够的GitHub Actions运行时间配额

### Q: 如何本地测试API连接？
**A:** 使用提供的测试脚本：
```bash
python test_api.py
```

## 📊 使用相关

### Q: 为什么抓取的论文数量少于预期？
**A:** 可能的原因：
1. **ArXiv发布时间**: 加速器物理领域每日发布论文数量有限
2. **查询范围**: 项目专门针对 `physics.acc-ph` 分类
3. **去重机制**: 自动过滤重复或已处理的论文
4. **配置限制**: 检查 `config/settings.yaml` 中的 `max_papers_per_day` 设置

### Q: 如何修改分析提示？
**A:** 编辑以下模板文件：
- `templates/analysis_prompt.txt` - 主要分析提示
- `templates/classification_prompt.txt` - 分类提示

### Q: 分析结果存储在哪里？
**A:** 
- **论文数据**: `data/papers/YYYY-MM-DD/`
- **分析结果**: `data/analysis/YYYY-MM-DD/`
- **统计信息**: `data/statistics/`

### Q: 如何自定义分类标签？
**A:** 修改 `templates/classification_prompt.txt` 文件中的分类定义。

## 🐛 故障排除

### Q: 出现 "API密钥无效" 错误
**A:** 
1. 确认API密钥正确复制（没有额外空格）
2. 检查API密钥是否有足够的配额
3. 验证API密钥对应的服务是否可用
4. 检查网络连接

### Q: 程序运行中断怎么办？
**A:** 
1. 检查日志文件 `logs/arxiv_analysis.log`
2. 确认API配额是否用完
3. 检查网络连接稳定性
4. 重新运行通常会自动跳过已处理的论文

### Q: 内存使用过高
**A:** 
1. 减少 `max_papers_per_day` 设置
2. 确保系统有足够的可用内存
3. 考虑分批处理大量论文

### Q: 无法写入文件
**A:** 
1. 检查文件权限
2. 确保磁盘空间充足
3. 验证目录是否存在

## 🔄 数据和结果

### Q: 如何查看分析历史？
**A:** 
- 每日结果保存在 `data/analysis/YYYY-MM-DD/` 目录
- 统计摘要在 `data/statistics/` 目录
- 日志记录在 `logs/arxiv_analysis.log`

### Q: 可以重新分析之前的论文吗？
**A:** 可以，通过以下方式：
1. 删除对应日期的分析结果文件
2. 重新运行程序，指定日期范围
3. 或者修改代码跳过去重检查

### Q: 如何导出数据？
**A:** 所有数据都以JSON格式存储，可以：
1. 直接读取JSON文件
2. 使用Python脚本处理数据
3. 转换为CSV或其他格式

### Q: 分析质量如何评估？
**A:** 
1. 查看 `analysis_results.json` 中的置信度分数
2. 人工审查部分结果样本
3. 检查分类一致性
4. 监控错误日志

## 🛠️ 开发相关

### Q: 如何添加新的LLM服务？
**A:** 
1. 在 `llm_analyzer.py` 中添加新的client实现
2. 更新配置文件支持新服务
3. 添加相应的环境变量
4. 更新文档和测试

### Q: 如何修改数据存储格式？
**A:** 修改 `data_processor.py` 中的存储方法，但要注意：
1. 保持向后兼容性
2. 更新相关的读取逻辑
3. 测试数据迁移

### Q: 如何贡献代码？
**A:** 
1. Fork仓库
2. 创建功能分支
3. 遵循代码规范
4. 添加测试
5. 提交Pull Request

详见 [CONTRIBUTING.md](../CONTRIBUTING.md)

## ⚡ 性能优化

### Q: 如何提高处理速度？
**A:** 
1. 使用更快的LLM服务（如DeepSeek）
2. 减少分析深度
3. 启用并发处理
4. 优化网络连接

### Q: 如何减少API调用成本？
**A:** 
1. 选择成本较低的LLM服务
2. 优化提示词长度
3. 实施智能缓存
4. 设置每日处理限制

## 🔒 安全相关

### Q: API密钥安全吗？
**A:** 
1. 使用环境变量存储密钥
2. 不要在代码中硬编码
3. 定期轮换API密钥
4. 监控API使用情况

### Q: 数据隐私如何保护？
**A:** 
1. 论文数据是公开的ArXiv内容
2. 不存储个人敏感信息
3. 遵循相关数据保护法规
4. 定期清理旧数据

## 📞 获取帮助

### Q: 在哪里可以获得更多帮助？
**A:** 
1. **文档**: 查看项目文档目录
2. **Issues**: 在GitHub上创建issue
3. **邮件**: ming-1018@foxmail.com
4. **讨论**: GitHub Discussions

### Q: 如何报告Bug？
**A:** 
1. 使用GitHub Issue模板
2. 提供详细的复现步骤
3. 包含日志信息
4. 描述环境配置

### Q: 如何提交功能请求？
**A:** 
1. 搜索现有的功能请求
2. 使用功能请求模板
3. 详细描述用例
4. 考虑实现可行性

---

如果您的问题没有在这里找到答案，请随时通过以下方式联系我们：

- 📧 Email: ming-1018@foxmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/iuming/ArXiv_AcceleratorPhysics/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/iuming/ArXiv_AcceleratorPhysics/discussions)
