# GitHub Pages Web界面演示部署指南

## 概述

本项目包含了一个完整的Web界面演示，可以部署到GitHub Pages进行展示。这个演示展示了ArXiv加速器物理论文分析系统的所有Web界面功能。

## 自动部署工作流

我们已经创建了GitHub Actions工作流 `.github/workflows/deploy-web-demo.yml`，它将：

1. **自动构建演示页面** - 生成静态版本的Web界面
2. **创建演示数据** - 生成样本数据用于演示
3. **部署到GitHub Pages** - 自动发布到GitHub Pages

## 如何启用GitHub Pages

### 步骤1: 推送代码
首先确保已经推送了包含工作流文件的代码：

```bash
git add .github/workflows/deploy-web-demo.yml
git commit -m "添加GitHub Pages Web界面演示部署工作流"
git push origin main
```

### 步骤2: 在GitHub仓库中启用Pages

1. 访问你的GitHub仓库页面
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** 下拉菜单中选择 **GitHub Actions**
5. 保存设置

### 步骤3: 配置权限（如果需要）

在仓库设置中：
1. 转到 **Settings > Actions > General**
2. 在 **Workflow permissions** 部分：
   - 选择 **Read and write permissions**
   - 勾选 **Allow GitHub Actions to create and approve pull requests**
3. 保存更改

### 步骤4: 触发部署

有三种方式触发部署：

#### 方法1: 推送到main分支（自动触发）
```bash
git push origin main
```

#### 方法2: 手动触发
1. 访问仓库的 **Actions** 标签
2. 选择 **Deploy Web Demo to GitHub Pages** 工作流
3. 点击 **Run workflow** 按钮
4. 选择 `main` 分支并点击 **Run workflow**

#### 方法3: 创建Pull Request
当创建针对main分支的Pull Request时也会触发构建（但不会部署）

## 演示特性

### 界面展示
- **现代化设计**: 基于Bootstrap 5的响应式界面
- **数据可视化**: 使用Chart.js的交互式图表
- **多页面导航**: 展示所有主要功能页面
- **实时风格**: 模拟真实的系统运行状态

### 包含页面
1. **首页仪表板**: 系统概览和关键指标
2. **论文管理**: 论文列表和详情展示
3. **统计分析**: 数据图表和趋势分析
4. **分析管理**: 系统操作和实时日志
5. **系统配置**: 配置管理界面

### 技术栈展示
- **前端**: Bootstrap 5 + Chart.js + Font Awesome
- **后端**: Flask 2.3+ (完整版)
- **样式**: 自定义CSS主题
- **交互**: 现代JavaScript ES6+

## 访问演示

部署完成后，你可以通过以下URL访问演示：

```
https://[用户名].github.io/ArXiv_AcceleratorPhysics/
```

例如：
- `https://iuming.github.io/ArXiv_AcceleratorPhysics/`

## 演示内容

### 演示数据
演示使用预生成的样本数据，包括：
- 443篇论文总数
- 365篇已分析论文
- 12篇今日新增论文
- 5个论文分类
- 3篇最新论文示例

### 交互功能
- 导航菜单切换不同页面
- 图表数据可视化
- 响应式布局适配各种设备
- 模拟的实时数据更新

## 更新演示

当你修改Web界面代码后，演示会自动更新：

1. 修改 `templates/web/` 中的模板文件
2. 更新 `static/` 中的CSS/JS文件
3. 推送到main分支
4. GitHub Actions会自动重新构建和部署

## 自定义演示

### 修改演示数据
编辑工作流文件中的Python脚本部分来自定义演示数据：

```python
demo_data = {
    "stats": {
        "total_papers": 443,      # 修改总论文数
        "analyzed_papers": 365,   # 修改已分析数
        "today_papers": 12,       # 修改今日新增
        "categories_count": 5     # 修改分类数
    },
    # ... 更多数据
}
```

### 修改演示页面
直接编辑工作流文件中的HTML模板或创建单独的模板文件。

## 故障排除

### 常见问题

1. **部署失败**: 检查仓库的Actions权限设置
2. **Pages未启用**: 确保在仓库设置中启用了GitHub Pages
3. **工作流不运行**: 检查工作流文件语法和权限

### 查看构建日志
1. 访问仓库的 **Actions** 标签
2. 点击最新的工作流运行
3. 查看详细的构建和部署日志

### 重新部署
如果需要强制重新部署：
1. 访问 **Actions** 标签
2. 手动运行 **Deploy Web Demo to GitHub Pages** 工作流

## 技术细节

### 静态化处理
由于GitHub Pages只支持静态内容，我们将Flask应用转换为静态HTML：
- 使用JavaScript模拟路由
- 预生成演示数据JSON文件
- 保持原有的视觉设计和交互

### CDN资源
演示使用CDN加载以下资源：
- Bootstrap 5.1.3
- Chart.js (最新版)
- Font Awesome 6.0.0
- jQuery 3.6.0

### 响应式设计
演示完全支持移动设备，在各种屏幕尺寸下都能正常显示。

---

**注意**: 这是一个静态演示版本，用于展示界面设计和功能。完整的生产版本需要运行Flask服务器并连接到实际的数据源。
