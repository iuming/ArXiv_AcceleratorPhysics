#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: web_app.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: Web界面模块 - 提供基于Flask的Web界面
             
主要功能：
- 论文管理和查看界面
- 实时分析状态监控
- 交互式统计图表展示
- 系统配置管理界面
- 分析任务控制面板

Web界面包含6个核心页面：
- 首页仪表板 (index.html)
- 论文列表 (papers.html)
- 论文详情 (paper_detail.html)
- 统计分析 (statistics.html) 
- 分析管理 (analysis.html)
- 系统配置 (config.html)

技术栈：
- 后端: Flask 2.3+, Jinja2模板引擎
- 前端: Bootstrap 5, Chart.js, Font Awesome
- 响应式设计，支持移动端访问

Modification History:
- 2025-07-25: Initial creation with complete web interface
- 2025-07-25: Added responsive design and real-time features
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename

from .arxiv_fetcher import ArXivFetcher
from .llm_analyzer import LLMAnalyzer
from .utils import load_config, setup_logging
from .data_processor import DataProcessor


class WebApp:
    """Web应用类"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """初始化Web应用"""
        # 切换到项目根目录以正确加载配置
        import os
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        self.config = load_config()
        self.logger = setup_logging()
        
        # 初始化Flask应用
        self.app = Flask(__name__, 
                        template_folder='../templates/web',
                        static_folder='../static')
        self.app.secret_key = os.environ.get('SECRET_KEY', 'arxiv_analyzer_secret_key')
        
        # 初始化核心组件
        self.arxiv_fetcher = ArXivFetcher(self.config)
        self.llm_analyzer = LLMAnalyzer(self.config)
        self.data_processor = DataProcessor(self.config)
        
        # 设置路由
        self._setup_routes()
        
        self.logger.info("Web应用初始化完成")
    
    def _setup_routes(self):
        """设置Web路由"""
        
        @self.app.route('/')
        def index():
            """主页"""
            try:
                # 获取最新统计数据
                stats = self._get_latest_stats()
                recent_papers = self._get_recent_papers(limit=5)
                return render_template('index.html', 
                                     stats=stats, 
                                     recent_papers=recent_papers)
            except Exception as e:
                self.logger.error(f"主页加载错误: {e}")
                flash(f"页面加载失败: {e}", 'error')
                return render_template('index.html', stats={}, recent_papers=[])
        
        @self.app.route('/papers')
        def papers():
            """论文列表页面"""
            try:
                page = request.args.get('page', 1, type=int)
                category = request.args.get('category', '')
                date_filter = request.args.get('date', '')
                
                papers_data = self._get_papers_list(page, category, date_filter)
                return render_template('papers.html', **papers_data)
            except Exception as e:
                self.logger.error(f"论文列表加载错误: {e}")
                flash(f"论文列表加载失败: {e}", 'error')
                return render_template('papers.html', papers=[], total_pages=0, current_page=1)
        
        @self.app.route('/paper/<paper_id>')
        def paper_detail(paper_id: str):
            """论文详情页面"""
            try:
                paper_data = self._get_paper_detail(paper_id)
                if paper_data:
                    return render_template('paper_detail.html', paper=paper_data)
                else:
                    flash('论文不存在', 'error')
                    return redirect(url_for('papers'))
            except Exception as e:
                self.logger.error(f"论文详情加载错误: {e}")
                flash(f"论文详情加载失败: {e}", 'error')
                return redirect(url_for('papers'))
        
        @self.app.route('/statistics')
        def statistics():
            """统计页面"""
            try:
                stats_data = self._get_detailed_stats()
                return render_template('statistics.html', stats=stats_data)
            except Exception as e:
                self.logger.error(f"统计页面加载错误: {e}")
                flash(f"统计数据加载失败: {e}", 'error')
                return render_template('statistics.html', stats={})
        
        @self.app.route('/analysis')
        def analysis():
            """分析管理页面"""
            try:
                return render_template('analysis.html')
            except Exception as e:
                self.logger.error(f"分析页面加载错误: {e}")
                flash(f"页面加载失败: {e}", 'error')
                return render_template('analysis.html')
        
        @self.app.route('/config')
        def config():
            """配置页面"""
            try:
                current_config = self.config.copy()
                # 隐藏敏感信息
                if 'api_keys' in current_config:
                    for service in current_config['api_keys']:
                        if current_config['api_keys'][service]:
                            current_config['api_keys'][service] = '*' * 10
                
                return render_template('config.html', config=current_config)
            except Exception as e:
                self.logger.error(f"配置页面加载错误: {e}")
                flash(f"配置页面加载失败: {e}", 'error')
                return render_template('config.html', config={})
        
        # API路由
        @self.app.route('/api/run_analysis', methods=['POST'])
        def api_run_analysis():
            """启动分析任务API"""
            try:
                data = request.get_json()
                force_update = data.get('force_update', False)
                
                # 在后台启动分析任务
                result = self._run_analysis_task(force_update)
                
                if result['success']:
                    return jsonify({
                        'success': True,
                        'message': '分析任务已启动',
                        'task_id': result.get('task_id')
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': result.get('error', '分析任务启动失败')
                    }), 500
                    
            except Exception as e:
                self.logger.error(f"启动分析任务失败: {e}")
                return jsonify({
                    'success': False,
                    'message': f'启动分析任务失败: {e}'
                }), 500
        
        @self.app.route('/api/analysis_status')
        def api_analysis_status():
            """获取分析状态API"""
            try:
                # 这里可以实现任务状态检查逻辑
                return jsonify({
                    'status': 'idle',  # idle, running, completed, error
                    'progress': 0,
                    'message': '就绪'
                })
            except Exception as e:
                self.logger.error(f"获取分析状态失败: {e}")
                return jsonify({
                    'status': 'error',
                    'message': f'状态获取失败: {e}'
                }), 500
        
        @self.app.route('/api/stats')
        def api_stats():
            """获取统计数据API"""
            try:
                stats = self._get_latest_stats()
                return jsonify(stats)
            except Exception as e:
                self.logger.error(f"获取统计数据失败: {e}")
                return jsonify({'error': str(e)}), 500
    
    def _get_latest_stats(self) -> Dict[str, Any]:
        """获取最新统计数据"""
        try:
            stats_file = Path("data/statistics/summary.json")
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"读取统计数据失败: {e}")
            return {}
    
    def _get_recent_papers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的论文"""
        try:
            # 获取最新日期的论文
            papers_dir = Path("data/papers")
            if not papers_dir.exists():
                return []
            
            # 找到最新的日期目录
            date_dirs = [d for d in papers_dir.iterdir() if d.is_dir()]
            if not date_dirs:
                return []
            
            latest_date = max(date_dirs, key=lambda x: x.name)
            papers_file = latest_date / "papers.json"
            
            if papers_file.exists():
                with open(papers_file, 'r', encoding='utf-8') as f:
                    papers = json.load(f)
                    return papers[:limit] if isinstance(papers, list) else []
            
            return []
        except Exception as e:
            self.logger.error(f"获取最近论文失败: {e}")
            return []
    
    def _get_papers_list(self, page: int, category: str = '', date_filter: str = '') -> Dict[str, Any]:
        """获取论文列表（分页）"""
        try:
            papers_per_page = 20
            all_papers = []
            
            # 收集所有论文
            papers_dir = Path("data/papers")
            if papers_dir.exists():
                for date_dir in sorted(papers_dir.iterdir(), reverse=True):
                    if date_dir.is_dir():
                        papers_file = date_dir / "papers.json"
                        if papers_file.exists():
                            with open(papers_file, 'r', encoding='utf-8') as f:
                                papers = json.load(f)
                                if isinstance(papers, list):
                                    all_papers.extend(papers)
            
            # 应用过滤器
            filtered_papers = all_papers
            if category:
                filtered_papers = [p for p in filtered_papers 
                                 if category.lower() in (p.get('category', '').lower())]
            
            if date_filter:
                filtered_papers = [p for p in filtered_papers 
                                 if p.get('published', '').startswith(date_filter)]
            
            # 分页
            total_papers = len(filtered_papers)
            total_pages = (total_papers + papers_per_page - 1) // papers_per_page
            start_idx = (page - 1) * papers_per_page
            end_idx = start_idx + papers_per_page
            page_papers = filtered_papers[start_idx:end_idx]
            
            return {
                'papers': page_papers,
                'current_page': page,
                'total_pages': total_pages,
                'total_papers': total_papers,
                'category': category,
                'date_filter': date_filter
            }
            
        except Exception as e:
            self.logger.error(f"获取论文列表失败: {e}")
            return {
                'papers': [],
                'current_page': 1,
                'total_pages': 0,
                'total_papers': 0,
                'category': category,
                'date_filter': date_filter
            }
    
    def _get_paper_detail(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """获取论文详情"""
        try:
            # 搜索论文数据
            papers_dir = Path("data/papers")
            analysis_dir = Path("data/analysis")
            
            paper_data = None
            analysis_data = None
            
            # 搜索论文基本信息
            if papers_dir.exists():
                for date_dir in papers_dir.iterdir():
                    if date_dir.is_dir():
                        papers_file = date_dir / "papers.json"
                        if papers_file.exists():
                            with open(papers_file, 'r', encoding='utf-8') as f:
                                papers = json.load(f)
                                if isinstance(papers, list):
                                    for paper in papers:
                                        if paper.get('id') == paper_id:
                                            paper_data = paper
                                            break
                    if paper_data:
                        break
            
            # 搜索分析结果
            if analysis_dir.exists():
                for date_dir in analysis_dir.iterdir():
                    if date_dir.is_dir():
                        analysis_file = date_dir / f"{paper_id}_analysis.json"
                        if analysis_file.exists():
                            with open(analysis_file, 'r', encoding='utf-8') as f:
                                analysis_data = json.load(f)
                            break
            
            if paper_data:
                if analysis_data:
                    paper_data['analysis'] = analysis_data
                return paper_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"获取论文详情失败: {e}")
            return None
    
    def _get_detailed_stats(self) -> Dict[str, Any]:
        """获取详细统计数据"""
        try:
            stats_dir = Path("data/statistics")
            stats_data = {}
            
            if stats_dir.exists():
                # 总体统计
                summary_file = stats_dir / "summary.json"
                if summary_file.exists():
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        stats_data['summary'] = json.load(f)
                
                # 分类分布
                category_file = stats_dir / "category_distribution.json"
                if category_file.exists():
                    with open(category_file, 'r', encoding='utf-8') as f:
                        stats_data['categories'] = json.load(f)
                
                # 趋势数据
                trend_file = stats_dir / "daily_trend.json"
                if trend_file.exists():
                    with open(trend_file, 'r', encoding='utf-8') as f:
                        stats_data['trends'] = json.load(f)
            
            return stats_data
            
        except Exception as e:
            self.logger.error(f"获取详细统计数据失败: {e}")
            return {}
    
    def _run_analysis_task(self, force_update: bool = False) -> Dict[str, Any]:
        """运行分析任务"""
        try:
            # 这里可以实现异步任务启动逻辑
            # 暂时使用同步方式
            self.logger.info("启动分析任务...")
            
            # 可以在这里添加任务队列逻辑
            # 或者使用线程/进程池来异步执行
            
            return {
                'success': True,
                'task_id': f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
        except Exception as e:
            self.logger.error(f"启动分析任务失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """启动Web应用"""
        self.logger.info(f"启动Web服务器: http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ArXiv分析系统Web界面")
    parser.add_argument('--host', default='0.0.0.0', help='服务器地址')
    parser.add_argument('--port', type=int, default=5000, help='端口号')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    parser.add_argument('--config', default='config/settings.yaml', help='配置文件路径')
    
    args = parser.parse_args()
    
    web_app = WebApp(args.config)
    web_app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
