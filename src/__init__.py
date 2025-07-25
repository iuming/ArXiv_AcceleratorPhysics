#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: __init__.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: ArXiv加速器物理论文自动解读系统核心模块包初始化文件
             定义版本信息和模块元数据

主要功能模块：
- arxiv_fetcher: ArXiv论文数据抓取
- llm_analyzer: 多LLM智能分析引擎
- data_processor: 数据处理和存储
- web_app: 完整Web界面 (v1.1.0新增)
- utils: 配置管理和工具函数

Web界面特性 (v1.1.0):
- 基于Flask的现代Web界面
- Bootstrap 5响应式设计
- Chart.js交互式图表
- 实时分析状态监控
- 论文管理和系统配置

Modification History:
- 2025-07-25: Initial creation
- 2025-07-25: Added comprehensive package metadata
- 2025-07-25: v1.1.0 - Integrated complete web interface
"""

# ArXiv 加速器物理论文分析系统
# 核心模块包

__version__ = "1.1.0"
__author__ = "Ming Liu"
__email__ = "ming-1018@foxmail.com"
__institution__ = "Institute of High Energy Physics, Chinese Academy of Sciences"
__description__ = "ArXiv加速器物理论文自动分析系统 - 支持完整Web界面"
__license__ = "MIT"
__url__ = "https://github.com/iuming/ArXiv_AcceleratorPhysics"
