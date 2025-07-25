# GitHub Pages 部署说明

本项目支持自动构建和部署文档到 GitHub Pages。

## 启用 GitHub Pages

要启用文档的自动部署，请按照以下步骤操作：

### 1. 启用 GitHub Pages
1. 访问仓库的 **Settings** 页面
2. 在左侧菜单中找到 **Pages** 选项
3. 在 **Source** 部分，选择 **GitHub Actions**

### 2. 配置权限（如果需要）
确保仓库的 Actions 有必要的权限：
1. 访问 **Settings** > **Actions** > **General**
2. 在 **Workflow permissions** 部分，确保选择了适当的权限
3. 确保 **Allow GitHub Actions to create and approve pull requests** 被选中

### 3. 重新运行工作流
启用 Pages 后，重新运行 CI 工作流以部署文档。

## 文档访问

启用后，文档将可以通过以下地址访问：
```
https://<username>.github.io/<repository-name>/
```

对于本项目：
```
https://iuming.github.io/ArXiv_AcceleratorPhysics/
```

## 故障排除

如果遇到部署问题：

1. **权限错误**: 确保仓库的 Actions 有 `pages: write` 权限
2. **环境配置**: 确保在仓库设置中创建了 `github-pages` 环境
3. **分支配置**: 确保从正确的分支（通常是 `main`）进行部署

## 本地构建文档

您也可以在本地构建文档：

```bash
cd docs
pip install sphinx sphinx-rtd-theme
make html
```

构建的文档将位于 `docs/_build/html/` 目录中。
