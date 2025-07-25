import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 尝试相对导入，如果失败则使用绝对导入
try:
    from src.arxiv_fetcher import ArXivFetcher
    from src.llm_analyzer import LLMAnalyzer
    from src.data_processor import DataProcessor
    from src.utils import setup_logging, load_config
except ImportError:
    # 如果相对导入失败，尝试直接导入
    from arxiv_fetcher import ArXivFetcher
    from llm_analyzer import LLMAnalyzer
    from data_processor import DataProcessor
    from utils import setup_logging, load_config

async def main():
    """主函数：协调整个分析流程"""
    
    # 设置日志
    logger = setup_logging()
    logger.info("开始每日ArXiv加速器物理论文分析")
    
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
        
        # 2. 保存原始论文数据
        await processor.save_papers(papers, today)
        
        # 3. 使用LLM分析论文
        logger.info("开始LLM分析...")
        analysis_results = []
        
        for i, paper in enumerate(papers, 1):
            logger.info(f"分析论文 {i}/{len(papers)}: {paper['title'][:50]}...")
            
            try:
                analysis = await analyzer.analyze_paper(paper)
                analysis_results.append({
                    'paper': paper,
                    'analysis': analysis
                })
            except Exception as e:
                logger.error(f"分析论文失败: {e}")
                continue
        
        # 4. 保存分析结果
        await processor.save_analysis_results(analysis_results, today)
        
        # 5. 生成统计报告
        await processor.generate_daily_summary(analysis_results, today)
        
        # 6. 更新总体统计
        await processor.update_statistics(analysis_results, today)
        
        logger.info(f"✅ 分析完成！处理了 {len(analysis_results)} 篇论文")
        
    except Exception as e:
        logger.error(f"❌ 分析过程中发生错误: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
