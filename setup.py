#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: setup.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: 项目初始化和环境配置脚本，自动创建目录结构、安装依赖
             和配置运行环境

Modification History:
- 2025-07-25: Initial creation
- 2025-07-25: Added comprehensive environment setup
"""

"""
ArXiv 加速器物理分析系统初始化脚本
"""

import os
import sys
from pathlib import Path
import subprocess
import json

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误：需要Python 3.8或更高版本")
        sys.exit(1)
    print(f"✅ Python版本: {sys.version}")

def create_directories():
    """创建必要的目录"""
    directories = [
        "data/papers",
        "data/analysis", 
        "data/statistics",
        "logs",
        "config",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def check_environment_variables():
    """检查环境变量"""
    required_vars = ["OPENAI_API_KEY"]
    optional_vars = ["ANTHROPIC_API_KEY"]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
        else:
            print(f"✅ 环境变量 {var} 已设置")
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
        else:
            print(f"✅ 环境变量 {var} 已设置")
    
    if missing_required:
        print(f"❌ 缺少必需的环境变量: {', '.join(missing_required)}")
        print("\n请设置这些环境变量：")
        for var in missing_required:
            print(f"export {var}='your_api_key_here'")
        return False
    
    if missing_optional:
        print(f"⚠️  缺少可选的环境变量: {', '.join(missing_optional)}")
    
    return True

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def create_sample_config():
    """创建示例配置文件"""
    config_file = Path("config/settings.yaml")
    if not config_file.exists():
        print("⚠️  配置文件不存在，请确保 config/settings.yaml 文件已创建")
        return False
    
    print("✅ 配置文件已存在")
    return True

def test_arxiv_connection():
    """测试ArXiv连接"""
    print("🔗 测试ArXiv API连接...")
    try:
        import aiohttp
        import asyncio
        
        async def test_connection():
            url = "http://export.arxiv.org/api/query?search_query=cat:physics.acc-ph&max_results=1"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return True
                    return False
        
        result = asyncio.run(test_connection())
        if result:
            print("✅ ArXiv API连接正常")
            return True
        else:
            print("❌ ArXiv API连接失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试ArXiv连接时出错: {e}")
        return False

def create_initial_stats():
    """创建初始统计文件"""
    stats_file = Path("data/statistics/overall_stats.json")
    if not stats_file.exists():
        initial_stats = {
            "daily_counts": {},
            "category_totals": {},
            "total_papers": 0,
            "last_updated": None,
            "created_at": "2024-01-01T00:00:00"
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(initial_stats, f, ensure_ascii=False, indent=2)
        
        print("✅ 初始统计文件已创建")
    else:
        print("✅ 统计文件已存在")

def main():
    """主函数"""
    print("🚀 ArXiv 加速器物理分析系统初始化")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 创建目录
    create_directories()
    
    # 检查配置文件
    create_sample_config()
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 初始化失败：无法安装依赖")
        sys.exit(1)
    
    # 检查环境变量
    if not check_environment_variables():
        print("❌ 初始化失败：缺少必需的环境变量")
        sys.exit(1)
    
    # 测试连接
    test_arxiv_connection()
    
    # 创建初始统计
    create_initial_stats()
    
    print("\n" + "=" * 50)
    print("🎉 初始化完成！")
    print("\n下一步操作：")
    print("1. 检查 config/settings.yaml 配置文件")
    print("2. 运行测试：python src/main.py")
    print("3. 查看日志：tail -f logs/arxiv_analysis.log")
    print("4. 设置GitHub Secrets（用于自动化运行）")

if __name__ == "__main__":
    main()
