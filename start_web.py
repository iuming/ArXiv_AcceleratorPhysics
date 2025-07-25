#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: start_web.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: Web界面启动脚本 - 快速启动ArXiv分析系统的Web界面

功能特性：
- 跨平台Web服务器启动
- 命令行参数配置支持
- 自动环境检查和目录创建
- 详细的启动状态显示

支持参数：
- --host: 监听地址 (默认: 0.0.0.0)
- --port: 端口号 (默认: 5000) 
- --debug: 调试模式
- --config: 配置文件路径

使用示例：
  python start_web.py                    # 使用默认配置启动
  python start_web.py --port 8080        # 指定端口启动
  python start_web.py --debug            # 调试模式启动
  python start_web.py --host 127.0.0.1   # 指定监听地址

Modification History:
- 2025-07-25: Initial creation with comprehensive web interface support
"""

import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.web_app import WebApp
except ImportError as e:
    print(f"导入Web应用失败: {e}")
    print("请确保已安装所有依赖包:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="ArXiv加速器物理论文分析系统 - Web界面",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python start_web.py                    # 使用默认配置启动
  python start_web.py --port 8080        # 指定端口启动
  python start_web.py --debug            # 调试模式启动
  python start_web.py --host 127.0.0.1   # 指定监听地址
        """
    )
    
    parser.add_argument(
        '--host', 
        default='0.0.0.0',
        help='Web服务器监听地址 (默认: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=5000,
        help='Web服务器端口号 (默认: 5000)'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='启用调试模式'
    )
    
    parser.add_argument(
        '--config', 
        default='config/settings.yaml',
        help='配置文件路径 (默认: config/settings.yaml)'
    )
    
    args = parser.parse_args()
    
    # 检查配置文件
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"配置文件不存在: {config_path}")
        print("请确保配置文件存在或使用 --config 参数指定正确的路径")
        sys.exit(1)
    
    # 检查必要的目录
    required_dirs = ['data', 'logs', 'templates/web', 'static']
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            print(f"创建目录: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("ArXiv加速器物理论文分析系统 - Web界面")
    print("=" * 60)
    print(f"监听地址: {args.host}")
    print(f"端口号: {args.port}")
    print(f"调试模式: {'开启' if args.debug else '关闭'}")
    print(f"配置文件: {config_path.absolute()}")
    print("-" * 60)
    
    try:
        # 创建并启动Web应用
        web_app = WebApp(str(config_path))
        
        print(f"启动Web服务器...")
        print(f"访问地址: http://{args.host}:{args.port}")
        if args.host == '0.0.0.0':
            print(f"本地访问: http://localhost:{args.port}")
            print(f"局域网访问: http://127.0.0.1:{args.port}")
        print("-" * 60)
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        web_app.run(host=args.host, port=args.port, debug=args.debug)
        
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
    except Exception as e:
        print(f"\n启动Web应用失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
