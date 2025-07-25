#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: main.py
Author: Ming Liu
Email: ming-1018@foxm        logger.error(f"严重错误: {e}")
        raise

def cli_main():
    """命令行入口点函数"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()om
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: 主程序入口，协调整个ArXiv加速器物理论文自动分析流程
             包括论文抓取、LLM分析、数据处理和统计报告生成

Modification History:
- 2025-07-25: Initial creation
- 2025-07-25: Added comprehensive logging and error handling
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(current_dir))

# 切换到项目根目录（为了正确访问配置文件）
os.chdir(project_root)

# 直接导入模块（不使用src前缀）
from arxiv_fetcher import ArXivFetcher
from llm_analyzer import LLMAnalyzer
from data_processor import DataProcessor
from utils import setup_logging, load_config

async def main():
    """主函数：协调整个分析流程"""
    
    # 设置日志
    logger = setup_logging()
    logger.info("开始每日ArXiv加速器物理论文分析")
    
    # 检查API密钥
    logger.info("🔑 检查API密钥配置...")
    openai_key = os.getenv('OPENAI_API_KEY')
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    hepai_key = os.getenv('HAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    available_apis = []
    if deepseek_key:
        available_apis.append("DeepSeek (推荐)")
    if hepai_key:
        available_apis.append("HEPAI (备用)")
    if openai_key:
        available_apis.append("OpenAI")
    if anthropic_key:
        available_apis.append("Anthropic")
    
    if not available_apis:
        logger.error("❌ 未设置任何LLM API密钥！")
        logger.error("请在GitHub仓库Settings -> Secrets中设置：")
        logger.error("- DEEPSEEK_API_KEY (推荐，性价比高)")
        logger.error("- HAI_API_KEY (HEPAI，中科院高能所)")
        logger.error("- OPENAI_API_KEY (备用)")
        logger.error("- ANTHROPIC_API_KEY (备用)")
        logger.error("系统将仅抓取论文，不进行LLM分析")
    else:
        logger.info(f"✅ 已设置API密钥: {', '.join(available_apis)}")
    
    # 加载配置
    config = load_config()
    
    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"分析日期: {today}")
    
    try:
        # 初始化组件
        fetcher = ArXivFetcher(config)
        analyzer = LLMAnalyzer(config)
        processor = DataProcessor(config)
        
        # 1. 抓取最新论文
        logger.info("正在抓取ArXiv最新论文...")
        papers = await fetcher.fetch_recent_papers()
        logger.info(f"成功抓取 {len(papers)} 篇论文")
        
        if not papers:
            logger.warning("今日无新论文，跳过分析")
            return
        
        # 2. 保存原始论文数据（去重处理）
        await processor.save_papers(papers, today)
        
        # 3. 检查哪些论文需要分析
        papers_to_analyze = await processor.get_papers_needing_analysis(papers, today)
        
        if not papers_to_analyze:
            logger.info("所有论文已分析完成，无需重复分析")
        else:
            logger.info(f"需要分析 {len(papers_to_analyze)} 篇论文")
            
            # 4. 使用LLM分析论文
            logger.info("开始LLM分析...")
            analysis_results = []
            
            for i, paper in enumerate(papers_to_analyze, 1):
                logger.info(f"分析论文 {i}/{len(papers_to_analyze)}: {paper['title'][:50]}...")
                
                try:
                    analysis = await analyzer.analyze_paper(paper)
                    analysis_results.append(analysis)
                except Exception as e:
                    logger.error(f"分析论文失败: {e}")
                    # 即使失败也要保存错误信息
                    analysis_results.append({
                        'timestamp': datetime.now().isoformat(),
                        'paper_id': paper.get('arxiv_id'),
                        'analysis': None,
                        'classification': None,
                        'keywords': [],
                        'summary': None,
                        'error': str(e)
                    })
            
            # 5. 保存分析结果（去重处理）
            await processor.save_analysis_results(analysis_results, today)
            
            logger.info(f"✅ 本次分析完成！处理了 {len(analysis_results)} 篇论文")
        
        # 6. 生成统计报告（基于所有论文）
        all_analysis_results = await processor._load_existing_analysis(
            processor.base_data_dir / "analysis" / today
        )
        if all_analysis_results:
            await processor.generate_daily_summary(all_analysis_results, today)
            await processor.update_statistics(all_analysis_results, today)
            logger.info(f"📊 统计报告已更新，总计 {len(all_analysis_results)} 篇论文")
        
    except Exception as e:
        logger.error(f"❌ 分析过程中发生错误: {e}")
        raise

def cli_main():
    """命令行入口点函数"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
