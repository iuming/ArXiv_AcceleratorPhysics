#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: test_web.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: Web界面测试脚本 - 全面测试Web界面的功能完整性

测试覆盖范围：
- 模块导入测试 (Flask, WebApp等)
- 文件结构完整性验证
- 目录结构检查
- 配置文件有效性
- Web应用实例创建测试

测试结果输出：
- 详细的测试过程日志
- 清晰的成功/失败状态
- 问题诊断和解决建议
- 启动命令和访问指南

使用方法：
  python test_web.py

Modification History:
- 2025-07-25: Initial creation with comprehensive web testing framework
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试必要模块的导入"""
    print("测试模块导入...")
    
    try:
        import flask
        print(f"✓ Flask版本: {flask.__version__}")
    except ImportError:
        print("✗ Flask未安装，请运行: pip install Flask>=2.3.0")
        return False
    
    try:
        from src.web_app import WebApp
        print("✓ WebApp模块导入成功")
    except ImportError as e:
        print(f"✗ WebApp模块导入失败: {e}")
        return False
    
    return True

def test_file_structure():
    """测试文件结构"""
    print("\n测试文件结构...")
    
    required_files = [
        'src/web_app.py',
        'templates/web/base.html',
        'templates/web/index.html',
        'static/css/style.css',
        'static/js/app.js',
        'start_web.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - 文件不存在")
            all_exist = False
    
    return all_exist

def test_directories():
    """测试必要目录"""
    print("\n测试目录结构...")
    
    required_dirs = [
        'templates/web',
        'static/css',
        'static/js',
        'data',
        'logs'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - 目录不存在")
            all_exist = False
    
    return all_exist

def test_config():
    """测试配置文件"""
    print("\n测试配置文件...")
    
    config_file = 'config/settings.yaml'
    if os.path.exists(config_file):
        print(f"✓ {config_file}")
        return True
    else:
        print(f"✗ {config_file} - 配置文件不存在")
        print("  请先运行初始化脚本: python init_project.py")
        return False

def test_web_app():
    """测试Web应用创建"""
    print("\n测试Web应用...")
    
    try:
        from src.web_app import WebApp
        
        # 尝试创建Web应用实例（不启动服务器）
        if os.path.exists('config/settings.yaml'):
            app = WebApp('config/settings.yaml')
            print("✓ Web应用实例创建成功")
            return True
        else:
            print("✗ 配置文件不存在，跳过Web应用测试")
            return False
            
    except Exception as e:
        print(f"✗ Web应用创建失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("ArXiv分析系统 - Web界面测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("文件结构", test_file_structure),
        ("目录结构", test_directories),
        ("配置文件", test_config),
        ("Web应用", test_web_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}测试出错: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name:<12} {status}")
        if not result:
            all_passed = False
    
    print("-" * 60)
    if all_passed:
        print("🎉 所有测试通过！Web界面可以正常启动。")
        print("\n启动命令:")
        print("  python start_web.py")
        print("  或")
        print("  start_web.bat  (Windows)")
        print("\n访问地址: http://localhost:5000")
    else:
        print("❌ 部分测试失败，请检查上述问题。")
        print("\n常见解决方案:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 运行初始化: python init_project.py")
        print("3. 检查文件完整性")
    
    print("=" * 60)
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
