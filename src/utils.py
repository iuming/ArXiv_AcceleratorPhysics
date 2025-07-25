#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: utils.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: 工具函数模块，提供日志配置、配置文件加载、错误处理等通用功能
             为整个项目提供基础设施支持

Modification History:
- 2025-07-25: Initial creation
- 2025-07-25: Added comprehensive logging setup
- 2025-07-25: Implemented configuration management
"""

import logging
import os
import yaml
from pathlib import Path
from typing import Dict, Any

def setup_logging() -> logging.Logger:
    """设置日志配置"""
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "arxiv_analysis.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("arxiv_analyzer")

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    
    config_file = Path("config/settings.yaml")
    
    # 默认配置
    default_config = {
        "max_papers_per_day": 20,
        "openai_model": "gpt-3.5-turbo",
        "anthropic_model": "claude-3-sonnet-20240229",
        "analysis_timeout": 300,  # 5分钟超时
        "retry_attempts": 3,
        "categories": {
            "1": "束流动力学",
            "2": "射频技术",
            "3": "磁体技术", 
            "4": "束流诊断",
            "5": "加速器设计",
            "6": "超导技术",
            "7": "真空技术",
            "8": "控制系统",
            "9": "其他"
        }
    }
    
    # 如果配置文件存在，加载并合并
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    default_config.update(file_config)
        except Exception as e:
            logging.warning(f"加载配置文件失败，使用默认配置: {e}")
    
    return default_config

def validate_environment() -> bool:
    """验证环境配置"""
    
    required_env_vars = ['OPENAI_API_KEY']
    optional_env_vars = ['ANTHROPIC_API_KEY']
    
    missing_required = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    if missing_required:
        logging.error(f"缺少必需的环境变量: {', '.join(missing_required)}")
        return False
    
    missing_optional = []
    for var in optional_env_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_optional:
        logging.warning(f"缺少可选的环境变量: {', '.join(missing_optional)}")
    
    return True

def format_authors(authors: list, max_authors: int = 3) -> str:
    """格式化作者列表"""
    if not authors:
        return "未知作者"
    
    if len(authors) <= max_authors:
        return ", ".join(authors)
    else:
        return ", ".join(authors[:max_authors]) + " 等"

def truncate_text(text: str, max_length: int = 200) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def safe_filename(filename: str) -> str:
    """生成安全的文件名"""
    # 移除或替换不安全的字符
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # 限制长度
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename

def ensure_directory(path: Path) -> None:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)

def calculate_success_rate(successful: int, total: int) -> float:
    """计算成功率"""
    if total == 0:
        return 0.0
    return (successful / total) * 100

def parse_arxiv_id(url_or_id: str) -> str:
    """从URL或ID字符串中解析ArXiv ID"""
    if 'arxiv.org' in url_or_id:
        # 从URL中提取
        parts = url_or_id.split('/')
        return parts[-1]
    else:
        # 假设已经是ID
        return url_or_id

def format_date(date_str: str) -> str:
    """格式化日期字符串"""
    try:
        from datetime import datetime
        
        # 尝试解析ISO格式
        if 'T' in date_str:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        return date_obj.strftime('%Y年%m月%d日')
    except:
        return date_str

def get_file_size(file_path: Path) -> str:
    """获取文件大小的可读格式"""
    try:
        size_bytes = file_path.stat().st_size
        
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    except:
        return "未知大小"
