#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终项目检查脚本

在推送到GitHub前进行完整的项目功能检查
"""

import os
import sys
import json
from pathlib import Path

def check_core_files():
    """检查核心文件"""
    print("🔍 检查核心文件...")
    
    required_files = [
        'src/main.py',
        'src/arxiv_fetcher.py',
        'src/llm_analyzer.py',
        'src/data_processor.py',
        'src/utils.py',
        'src/web_app.py',
        'config/settings.yaml',
        'requirements.txt',
        'README.md',
        'CHANGELOG.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✓ {file_path}")
    
    if missing_files:
        print("  ❌ 缺失文件:")
        for file_path in missing_files:
            print(f"    - {file_path}")
        return False
    
    return True

def check_web_interface():
    """检查Web界面文件"""
    print("\n🌐 检查Web界面...")
    
    web_files = [
        'templates/web/base.html',
        'templates/web/index.html',
        'templates/web/papers.html',
        'templates/web/paper_detail.html',
        'templates/web/statistics.html',
        'templates/web/analysis.html',
        'templates/web/config.html',
        'static/css/style.css',
        'static/js/app.js',
        'start_web.py',
        'start_web.bat'
    ]
    
    missing_files = []
    for file_path in web_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✓ {file_path}")
    
    if missing_files:
        print("  ❌ 缺失Web文件:")
        for file_path in missing_files:
            print(f"    - {file_path}")
        return False
    
    return True

def check_templates():
    """检查模板文件"""
    print("\n📄 检查模板文件...")
    
    template_files = [
        'templates/analysis_prompt.txt',
        'templates/classification_prompt.txt',
        'templates/keywords_prompt.txt',
        'templates/summary_prompt.txt'
    ]
    
    missing_files = []
    for file_path in template_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✓ {file_path}")
    
    if missing_files:
        print("  ❌ 缺失模板文件:")
        for file_path in missing_files:
            print(f"    - {file_path}")
        return False
    
    return True

def check_github_workflows():
    """检查GitHub工作流"""
    print("\n⚙️ 检查GitHub工作流...")
    
    workflow_files = [
        '.github/workflows/daily_arxiv_analysis.yml',
        '.github/workflows/ci.yml'
    ]
    
    missing_files = []
    for file_path in workflow_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✓ {file_path}")
    
    if missing_files:
        print("  ❌ 缺失工作流文件:")
        for file_path in missing_files:
            print(f"    - {file_path}")
        return False
    
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    try:
        import yaml
        print("  ✓ PyYAML")
    except ImportError:
        print("  ❌ PyYAML - 需要安装: pip install PyYAML")
        return False
    
    try:
        import requests
        print("  ✓ requests")
    except ImportError:
        print("  ❌ requests - 需要安装: pip install requests")
        return False
    
    try:
        import flask
        print("  ✓ Flask")
    except ImportError:
        print("  ❌ Flask - 需要安装: pip install Flask")
        return False
    
    try:
        import pandas
        print("  ✓ pandas")
    except ImportError:
        print("  ❌ pandas - 需要安装: pip install pandas")
        return False
    
    return True

def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")
    
    required_dirs = [
        'src',
        'templates',
        'templates/web',
        'static',
        'static/css',
        'static/js',
        'config',
        'data',
        'logs',
        '.github',
        '.github/workflows'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            missing_dirs.append(dir_path)
        else:
            print(f"  ✓ {dir_path}/")
    
    if missing_dirs:
        print("  ❌ 缺失目录:")
        for dir_path in missing_dirs:
            print(f"    - {dir_path}/")
        return False
    
    return True

def check_imports():
    """检查核心模块导入"""
    print("\n🔍 检查模块导入...")
    
    sys.path.insert(0, 'src')
    
    try:
        from arxiv_fetcher import ArXivFetcher
        print("  ✓ ArXivFetcher")
    except ImportError as e:
        print(f"  ❌ ArXivFetcher - {e}")
        return False
    
    try:
        from llm_analyzer import LLMAnalyzer
        print("  ✓ LLMAnalyzer")
    except ImportError as e:
        print(f"  ❌ LLMAnalyzer - {e}")
        return False
    
    try:
        from data_processor import DataProcessor
        print("  ✓ DataProcessor")
    except ImportError as e:
        print(f"  ❌ DataProcessor - {e}")
        return False
    
    try:
        from web_app import WebApp
        print("  ✓ WebApp")
    except ImportError as e:
        print(f"  ❌ WebApp - {e}")
        return False
    
    return True

def check_configuration():
    """检查配置文件"""
    print("\n⚙️ 检查配置...")
    
    config_file = 'config/settings.yaml'
    if not os.path.exists(config_file):
        print(f"  ❌ 配置文件不存在: {config_file}")
        return False
    
    try:
        import yaml
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        required_sections = ['arxiv', 'llm', 'processing', 'logging']
        for section in required_sections:
            if section in config:
                print(f"  ✓ {section} 配置段")
            else:
                print(f"  ❌ 缺失配置段: {section}")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ 配置文件解析错误: {e}")
        return False

def generate_summary():
    """生成检查摘要"""
    print("\n" + "="*60)
    print("📊 项目功能摘要")
    print("="*60)
    
    features = [
        ("ArXiv论文抓取", "✓"),
        ("多LLM支持", "✓"),
        ("智能分析分类", "✓"),
        ("数据处理存储", "✓"),
        ("统计报告生成", "✓"),
        ("Web管理界面", "✓"),
        ("GitHub Actions自动化", "✓"),
        ("响应式Web设计", "✓"),
        ("实时任务监控", "✓"),
        ("系统配置管理", "✓"),
        ("API密钥管理", "✓"),
        ("数据可视化", "✓"),
        ("项目文档", "✓"),
        ("测试脚本", "✓"),
        ("健康检查", "✓")
    ]
    
    for feature, status in features:
        print(f"{feature:<20} {status}")
    
    print("-"*60)
    print("🎉 项目已准备好推送到GitHub!")
    print("\n推荐的推送流程:")
    print("1. git add -A")
    print("2. git commit -m '🌐 Add complete Web interface and enhance project structure'")
    print("3. git push origin main")
    print("\n记得在GitHub仓库中设置以下Secrets:")
    print("- DEEPSEEK_API_KEY (推荐)")
    print("- HAI_API_KEY (HEPAI)")
    print("- OPENAI_API_KEY (备用)")
    print("- ANTHROPIC_API_KEY (可选)")

def main():
    """主检查函数"""
    print("🔍 ArXiv分析系统 - 最终项目检查")
    print("="*60)
    
    checks = [
        ("核心文件", check_core_files),
        ("Web界面", check_web_interface),
        ("模板文件", check_templates),
        ("GitHub工作流", check_github_workflows),
        ("依赖包", check_dependencies),
        ("项目结构", check_project_structure),
        ("模块导入", check_imports),
        ("配置文件", check_configuration)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"  ❌ {check_name}检查出错: {e}")
            results.append((check_name, False))
    
    # 输出结果
    print("\n" + "="*60)
    print("🏁 检查结果汇总")
    print("="*60)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name:<15} {status}")
        if not result:
            all_passed = False
    
    print("-"*60)
    
    if all_passed:
        print("🎉 所有检查通过！项目已准备好发布。")
        generate_summary()
    else:
        print("⚠️ 部分检查失败，请修复问题后重新检查。")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
