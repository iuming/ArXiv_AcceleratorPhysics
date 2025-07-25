# 🔑 API密钥设置指南

## 问题说明

当前系统运行正常，但**LLM分析功能未启用**，因为缺少API密钥。论文能够正常抓取，但无法进行智能分析和分类。

## 🚨 当前状态

- ✅ **论文抓取**: 正常工作
- ❌ **LLM分析**: 未工作（缺少API密钥）
- ❌ **智能分类**: 未工作（缺少API密钥）
- ❌ **总结生成**: 未工作（缺少API密钥）

## 🔧 解决方案

### 步骤1: 获取API密钥

**推荐选项 - DeepSeek API（性价比最高）**：
1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册/登录账户
3. 进入 API Keys 页面
4. 创建新的API密钥
5. 复制密钥（格式类似：`sk-...`）

**备用选项1 - OpenAI API**：
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账户
3. 进入 API Keys 页面
4. 创建新的API密钥
5. 复制密钥（格式类似：`sk-proj-...`）

**备用选项2 - Anthropic API**：
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账户
3. 创建API密钥
4. 复制密钥

### 步骤2: 在GitHub中设置密钥

1. **进入你的GitHub仓库**：
   https://github.com/iuming/ArXiv_AcceleratorPhysics

2. **进入设置页面**：
   点击仓库页面上方的 **"Settings"** 标签

3. **找到Secrets设置**：
   在左侧菜单中点击 **"Secrets and variables"** → **"Actions"**

4. **添加密钥**：
   点击 **"New repository secret"** 按钮

5. **设置密钥信息**：
   
   **对于DeepSeek** (推荐，性价比最高)：
   - Name: `DEEPSEEK_API_KEY`
   - Secret: 粘贴你的DeepSeek API密钥
   - 点击 "Add secret"
   
   **对于OpenAI** (备用)：
   - Name: `OPENAI_API_KEY`
   - Secret: 粘贴你的OpenAI API密钥
   - 点击 "Add secret"
   
   **对于Anthropic** (可选备用)：
   - Name: `ANTHROPIC_API_KEY`
   - Secret: 粘贴你的Anthropic API密钥
   - 点击 "Add secret"

### 步骤3: 验证设置

设置完API密钥后：

1. **手动触发工作流程**：
   - 进入 Actions 标签页
   - 选择 "Daily ArXiv Accelerator Physics Analysis"
   - 点击 "Run workflow"
   - 选择 main 分支
   - 点击绿色的 "Run workflow" 按钮

2. **查看运行结果**：
   - 等待工作流程完成（约5-10分钟）
   - 检查生成的Issue中是否包含详细分析
   - 查看Actions日志确认无错误

## 💰 API费用说明

### DeepSeek API费用（推荐）：
- **deepseek-chat**: ~$0.0001-0.0003 每次分析
- **每日20篇论文**: 约$0.002-0.006/天
- **月费用**: 约$0.06-0.18/月
- **🏆 性价比最高，比OpenAI便宜10-20倍**

### OpenAI API费用：
- **GPT-3.5-turbo**: ~$0.001-0.002 每次分析
- **每日20篇论文**: 约$0.02-0.04/天
- **月费用**: 约$0.6-1.2/月

### Anthropic API费用：
- **Claude-3-Sonnet**: ~$0.003-0.015 每次分析
- **每日20篇论文**: 约$0.06-0.3/天
- **月费用**: 约$1.8-9/月

## 🎯 设置完成后的效果

设置API密钥后，系统将能够：

- 🧠 **深度分析论文内容**：研究主题、技术创新、应用价值等
- 📊 **智能分类**：自动分类到9个专业类别
- 🏷️ **提取关键词**：识别重要技术术语
- 📝 **生成总结**：创建简洁的中文总结
- 📈 **统计分析**：分类分布、趋势分析

## 📋 示例：设置前后对比

### 设置前（当前状态）：
```markdown
### 1. Commissioning of a radiofrequency quadrupole cooler-buncher
**作者**: Yin-Shen Liu, Han-Rui Hu, Xiao-Fei Yang 等  
**分类**: 未分类  
**简要总结**: 
```

### 设置后（预期效果）：
```markdown
### 1. Commissioning of a radiofrequency quadrupole cooler-buncher
**作者**: Yin-Shen Liu, Han-Rui Hu, Xiao-Fei Yang 等  
**分类**: 射频技术  
**简要总结**: 该研究开发了射频四极杆冷却聚束器系统，用于改善共线激光光谱实验中的离子束质量。系统通过离线测试验证，传输效率超过60%，束团时间分布半宽约2微秒，显著提升了整体传输效率，为精密激光光谱测量提供了重要技术支撑。
```

## ❓ 常见问题

**Q: 我需要两个API密钥吗？**
A: 不需要。只需要设置一个即可（推荐OpenAI）。Anthropic是备用选项。

**Q: API密钥安全吗？**
A: 是的。GitHub Secrets加密存储，只有工作流程能访问。

**Q: 设置后多久生效？**
A: 立即生效。可以手动运行工作流程测试。

**Q: 如果我不想花钱怎么办？**
A: 系统仍然会抓取和存储论文，只是缺少LLM分析功能。

---

**🎯 现在就去设置API密钥，让你的ArXiv分析系统发挥完整功能！**
