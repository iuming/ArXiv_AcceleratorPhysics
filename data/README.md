# 数据存储目录

这个目录用于存储ArXiv论文分析系统的所有数据：

## 目录结构

- `papers/` - 存储从ArXiv抓取的原始论文数据
- `analysis/` - 存储LLM分析结果和每日总结报告
- `statistics/` - 存储统计数据和趋势信息

## 数据格式

### papers/YYYY-MM-DD/
- `papers.json` - 当日所有论文的汇总
- `[arxiv_id].json` - 单篇论文的详细信息

### analysis/YYYY-MM-DD/  
- `analysis_results.json` - 当日所有分析结果
- `daily_summary.md` - 当日分析总结报告
- `[arxiv_id]_analysis.json` - 单篇论文的分析结果

### statistics/
- `overall_stats.json` - 总体统计信息
- `daily_trend.json` - 每日论文数量趋势
- `category_distribution.json` - 论文分类分布

## 注意事项

- 所有数据文件都使用UTF-8编码
- JSON文件格式化输出，便于阅读
- 每日数据按日期组织，便于管理和查找
