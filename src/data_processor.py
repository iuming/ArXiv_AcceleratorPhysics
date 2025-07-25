import json
import os
from datetime import datetime
from typing import Dict, List
import logging
from pathlib import Path
import yaml

# 动态导入aiofiles
try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False

class DataProcessor:
    """数据处理器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.base_data_dir = Path("data")
        
        # 确保数据目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        directories = [
            self.base_data_dir / "papers",
            self.base_data_dir / "analysis", 
            self.base_data_dir / "statistics"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    async def save_papers(self, papers: List[Dict], date: str):
        """保存原始论文数据"""
        papers_dir = self.base_data_dir / "papers" / date
        papers_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存所有论文到一个JSON文件
        papers_file = papers_dir / "papers.json"
        if AIOFILES_AVAILABLE:
            async with aiofiles.open(papers_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(papers, ensure_ascii=False, indent=2))
        else:
            with open(papers_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(papers, ensure_ascii=False, indent=2))
        
        # 为每篇论文创建单独的文件
        for paper in papers:
            arxiv_id = paper.get('arxiv_id', 'unknown')
            paper_file = papers_dir / f"{arxiv_id}.json"
            if AIOFILES_AVAILABLE:
                async with aiofiles.open(paper_file, 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(paper, ensure_ascii=False, indent=2))
            else:
                with open(paper_file, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(paper, ensure_ascii=False, indent=2))
        
        self.logger.info(f"✅ 已保存 {len(papers)} 篇论文数据到 {papers_dir}")
    
    async def save_analysis_results(self, analysis_results: List[Dict], date: str):
        """保存分析结果"""
        analysis_dir = self.base_data_dir / "analysis" / date
        analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存所有分析结果
        results_file = analysis_dir / "analysis_results.json"
        if AIOFILES_AVAILABLE:
            async with aiofiles.open(results_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(analysis_results, ensure_ascii=False, indent=2))
        else:
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(analysis_results, ensure_ascii=False, indent=2))
        
        # 为每个分析结果创建单独的文件
        for result in analysis_results:
            paper_id = result.get('paper_id', 'unknown')
            result_file = analysis_dir / f"{paper_id}_analysis.json"
            if AIOFILES_AVAILABLE:
                async with aiofiles.open(result_file, 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                with open(result_file, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=2))
        
        self.logger.info(f"✅ 已保存 {len(analysis_results)} 个分析结果到 {analysis_dir}")
    
    async def generate_daily_summary(self, analysis_results: List[Dict], date: str):
        """生成每日总结报告"""
        analysis_dir = self.base_data_dir / "analysis" / date
        
        # 统计信息
        total_papers = len(analysis_results)
        successful_analyses = sum(1 for r in analysis_results if r.get('analysis'))
        
        # 分类统计
        category_stats = {}
        for result in analysis_results:
            classification = result.get('classification', {})
            category = classification.get('category_name', '未分类')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        # 生成Markdown报告
        summary_content = f"""# ArXiv加速器物理论文每日分析报告

**日期**: {date}
**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 概览统计

- **总论文数**: {total_papers}
- **成功分析**: {successful_analyses}
- **分析成功率**: {successful_analyses/total_papers*100:.1f}%

## 📈 分类分布

"""
        
        for category, count in sorted(category_stats.items()):
            percentage = count / total_papers * 100
            summary_content += f"- **{category}**: {count} 篇 ({percentage:.1f}%)\n"
        
        summary_content += "\n## 📚 论文详情\n\n"
        
        # 添加每篇论文的简要信息
        for i, result in enumerate(analysis_results, 1):
            paper = result.get('paper', {})
            analysis = result.get('analysis', '')
            classification = result.get('classification', {})
            summary = result.get('summary', '')
            
            title = paper.get('title', '未知标题')
            authors = ', '.join(paper.get('authors', [])[:3])  # 只显示前3个作者
            if len(paper.get('authors', [])) > 3:
                authors += " 等"
            
            category = classification.get('category_name', '未分类')
            arxiv_id = paper.get('arxiv_id', '')
            
            summary_content += f"""### {i}. {title}

**作者**: {authors}  
**ArXiv ID**: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})  
**分类**: {category}  

**简要总结**: {summary[:200]}{'...' if len(summary) > 200 else ''}

---

"""
        
        # 保存总结报告
        summary_file = analysis_dir / "daily_summary.md"
        async with aiofiles.open(summary_file, 'w', encoding='utf-8') as f:
            await f.write(summary_content)
        
        self.logger.info(f"✅ 已生成每日总结报告: {summary_file}")
    
    async def update_statistics(self, analysis_results: List[Dict], date: str):
        """更新总体统计信息"""
        stats_file = self.base_data_dir / "statistics" / "overall_stats.json"
        
        # 加载现有统计
        overall_stats = {}
        if stats_file.exists():
            try:
                async with aiofiles.open(stats_file, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    overall_stats = json.loads(content)
            except Exception as e:
                self.logger.warning(f"加载统计文件失败: {e}")
        
        # 初始化统计结构
        if 'daily_counts' not in overall_stats:
            overall_stats['daily_counts'] = {}
        if 'category_totals' not in overall_stats:
            overall_stats['category_totals'] = {}
        if 'total_papers' not in overall_stats:
            overall_stats['total_papers'] = 0
        if 'last_updated' not in overall_stats:
            overall_stats['last_updated'] = date
        
        # 更新统计
        overall_stats['daily_counts'][date] = len(analysis_results)
        overall_stats['total_papers'] += len(analysis_results)
        overall_stats['last_updated'] = date
        
        # 更新分类统计
        for result in analysis_results:
            classification = result.get('classification', {})
            category = classification.get('category_name', '未分类')
            overall_stats['category_totals'][category] = overall_stats['category_totals'].get(category, 0) + 1
        
        # 保存更新后的统计
        async with aiofiles.open(stats_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(overall_stats, ensure_ascii=False, indent=2))
        
        # 生成统计图表数据
        await self._generate_stats_charts(overall_stats)
        
        self.logger.info(f"✅ 已更新总体统计信息")
    
    async def _generate_stats_charts(self, overall_stats: Dict):
        """生成统计图表数据"""
        stats_dir = self.base_data_dir / "statistics"
        
        # 生成每日论文数量趋势数据
        daily_trend = {
            "labels": list(overall_stats['daily_counts'].keys()),
            "data": list(overall_stats['daily_counts'].values())
        }
        
        trend_file = stats_dir / "daily_trend.json"
        async with aiofiles.open(trend_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(daily_trend, ensure_ascii=False, indent=2))
        
        # 生成分类分布数据
        category_distribution = {
            "labels": list(overall_stats['category_totals'].keys()),
            "data": list(overall_stats['category_totals'].values())
        }
        
        category_file = stats_dir / "category_distribution.json"
        async with aiofiles.open(category_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(category_distribution, ensure_ascii=False, indent=2))
        
        # 生成统计摘要
        stats_summary = {
            "total_papers": overall_stats['total_papers'],
            "total_days": len(overall_stats['daily_counts']),
            "average_papers_per_day": overall_stats['total_papers'] / max(len(overall_stats['daily_counts']), 1),
            "most_common_category": max(overall_stats['category_totals'].items(), key=lambda x: x[1]) if overall_stats['category_totals'] else ("无", 0),
            "last_updated": overall_stats['last_updated']
        }
        
        summary_file = stats_dir / "summary.json"
        async with aiofiles.open(summary_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(stats_summary, ensure_ascii=False, indent=2))
