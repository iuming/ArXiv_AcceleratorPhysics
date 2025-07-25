#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: project_stats.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: 项目统计脚本，生成代码行数、文件数量、项目完成度等统计信息
             为项目管理和进度跟踪提供数据支持

Modification History:
- 2025-07-25: Initial creation
- 2025-07-25: Added comprehensive project statistics
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re

class ProjectStatsGenerator:
    """项目统计信息生成器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.stats = {}
        
    def generate_all_stats(self) -> Dict[str, Any]:
        """生成所有统计信息"""
        self.stats = {
            'timestamp': datetime.now().isoformat(),
            'project_name': 'ArXiv_AcceleratorPhysics',
            'author': 'Ming Liu',
            'version': '1.0.0',
            'file_stats': self._get_file_stats(),
            'code_stats': self._get_code_stats(),
            'documentation_stats': self._get_documentation_stats(),
            'data_stats': self._get_data_stats(),
            'git_stats': self._get_git_stats(),
            'project_health': self._assess_project_health()
        }
        
        return self.stats
    
    def _get_file_stats(self) -> Dict[str, Any]:
        """获取文件统计信息"""
        file_counts = {}
        total_size = 0
        file_extensions = {}
        
        for root, dirs, files in os.walk(self.project_root):
            # 跳过隐藏目录和虚拟环境
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', '__pycache__', 'node_modules']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    size = file_path.stat().st_size
                    total_size += size
                    
                    # 按扩展名分类
                    ext = file_path.suffix.lower()
                    if ext not in file_extensions:
                        file_extensions[ext] = {'count': 0, 'size': 0}
                    file_extensions[ext]['count'] += 1
                    file_extensions[ext]['size'] += size
                    
                    # 按文件类型分类
                    file_type = self._categorize_file(file_path)
                    if file_type not in file_counts:
                        file_counts[file_type] = 0
                    file_counts[file_type] += 1
                    
                except OSError:
                    continue
        
        return {
            'total_files': sum(file_counts.values()),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'by_type': file_counts,
            'by_extension': file_extensions
        }
    
    def _categorize_file(self, file_path: Path) -> str:
        """文件分类"""
        ext = file_path.suffix.lower()
        name = file_path.name.lower()
        
        if ext in ['.py']:
            return 'Python源码'
        elif ext in ['.md']:
            return 'Markdown文档'
        elif ext in ['.yaml', '.yml']:
            return '配置文件'
        elif ext in ['.json']:
            return 'JSON数据'
        elif ext in ['.txt']:
            return '文本文件'
        elif ext in ['.log']:
            return '日志文件'
        elif name in ['requirements.txt', 'setup.py', 'pyproject.toml']:
            return '项目配置'
        elif name.startswith('readme'):
            return '说明文档'
        elif ext in ['.gitignore', '.gitattributes'] or name.startswith('.git'):
            return 'Git相关'
        else:
            return '其他文件'
    
    def _get_code_stats(self) -> Dict[str, Any]:
        """获取代码统计信息"""
        python_files = list(self.project_root.rglob('*.py'))
        total_lines = 0
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        docstring_lines = 0
        
        functions_count = 0
        classes_count = 0
        imports_count = 0
        
        for py_file in python_files:
            if any(part.startswith('.') or part in ['venv', '__pycache__'] for part in py_file.parts):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                in_docstring = False
                docstring_delimiter = None
                
                for line in lines:
                    total_lines += 1
                    stripped = line.strip()
                    
                    if not stripped:
                        blank_lines += 1
                    elif stripped.startswith('#'):
                        comment_lines += 1
                    elif '"""' in stripped or "'''" in stripped:
                        docstring_lines += 1
                        # 简单的文档字符串检测
                        if stripped.count('"""') % 2 == 1:
                            in_docstring = not in_docstring
                            docstring_delimiter = '"""'
                        elif stripped.count("'''") % 2 == 1:
                            in_docstring = not in_docstring
                            docstring_delimiter = "'''"
                    elif in_docstring:
                        docstring_lines += 1
                        if docstring_delimiter in stripped:
                            in_docstring = False
                    else:
                        code_lines += 1
                
                # 统计函数、类、导入
                functions_count += len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
                classes_count += len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
                imports_count += len(re.findall(r'^\s*(import|from)\s+', content, re.MULTILINE))
                
            except Exception:
                continue
        
        return {
            'python_files': len(python_files),
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'docstring_lines': docstring_lines,
            'blank_lines': blank_lines,
            'functions': functions_count,
            'classes': classes_count,
            'imports': imports_count,
            'code_to_comment_ratio': round(code_lines / max(comment_lines + docstring_lines, 1), 2)
        }
    
    def _get_documentation_stats(self) -> Dict[str, Any]:
        """获取文档统计信息"""
        doc_files = []
        doc_types = {
            'README': 0,
            'API文档': 0,
            '使用指南': 0,
            '贡献指南': 0,
            '变更日志': 0,
            '其他文档': 0
        }
        
        total_doc_size = 0
        
        for md_file in self.project_root.rglob('*.md'):
            if any(part.startswith('.') for part in md_file.parts):
                continue
                
            try:
                size = md_file.stat().st_size
                total_doc_size += size
                doc_files.append(str(md_file.relative_to(self.project_root)))
                
                # 按文档类型分类
                name = md_file.name.lower()
                if 'readme' in name:
                    doc_types['README'] += 1
                elif 'api' in name or 'setup' in name:
                    doc_types['API文档'] += 1
                elif 'usage' in name or 'user' in name:
                    doc_types['使用指南'] += 1
                elif 'contribut' in name or 'develop' in name:
                    doc_types['贡献指南'] += 1
                elif 'changelog' in name or 'history' in name:
                    doc_types['变更日志'] += 1
                else:
                    doc_types['其他文档'] += 1
                    
            except OSError:
                continue
        
        return {
            'total_doc_files': len(doc_files),
            'total_doc_size_kb': round(total_doc_size / 1024, 2),
            'doc_types': doc_types,
            'doc_files': doc_files
        }
    
    def _get_data_stats(self) -> Dict[str, Any]:
        """获取数据统计信息"""
        data_path = self.project_root / 'data'
        if not data_path.exists():
            return {'status': '数据目录不存在'}
        
        papers_count = 0
        analysis_count = 0
        latest_date = None
        date_range = []
        
        # 统计论文数据
        papers_dir = data_path / 'papers'
        if papers_dir.exists():
            for date_dir in papers_dir.iterdir():
                if date_dir.is_dir():
                    date_range.append(date_dir.name)
                    papers_file = date_dir / 'papers.json'
                    if papers_file.exists():
                        try:
                            with open(papers_file, 'r', encoding='utf-8') as f:
                                papers_data = json.load(f)
                                papers_count += len(papers_data)
                        except:
                            continue
        
        # 统计分析数据
        analysis_dir = data_path / 'analysis'
        if analysis_dir.exists():
            for date_dir in analysis_dir.iterdir():
                if date_dir.is_dir():
                    analysis_file = date_dir / 'analysis_results.json'
                    if analysis_file.exists():
                        analysis_count += 1
        
        if date_range:
            date_range.sort()
            latest_date = date_range[-1]
        
        return {
            'total_papers': papers_count,
            'analysis_days': analysis_count,
            'date_range': f"{date_range[0]} - {date_range[-1]}" if len(date_range) > 1 else date_range[0] if date_range else "无数据",
            'latest_date': latest_date,
            'avg_papers_per_day': round(papers_count / max(len(date_range), 1), 2)
        }
    
    def _get_git_stats(self) -> Dict[str, Any]:
        """获取Git统计信息"""
        git_dir = self.project_root / '.git'
        if not git_dir.exists():
            return {'status': '非Git仓库'}
        
        try:
            import subprocess
            
            # 获取提交数量
            result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            commits_count = int(result.stdout.strip()) if result.returncode == 0 else 0
            
            # 获取分支信息
            result = subprocess.run(['git', 'branch', '-r'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            branches = len(result.stdout.strip().split('\n')) if result.returncode == 0 else 0
            
            # 获取最近提交日期
            result = subprocess.run(['git', 'log', '-1', '--format=%ci'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            last_commit = result.stdout.strip() if result.returncode == 0 else "未知"
            
            return {
                'commits_count': commits_count,
                'branches_count': branches,
                'last_commit_date': last_commit,
                'status': '已初始化'
            }
        except Exception:
            return {'status': 'Git信息获取失败'}
    
    def _assess_project_health(self) -> Dict[str, Any]:
        """评估项目健康状况"""
        health_score = 0
        max_score = 100
        issues = []
        strengths = []
        
        # 代码质量评估
        if 'code_stats' in self.stats:
            code_stats = self.stats['code_stats']
            
            # 注释比例
            if code_stats.get('code_to_comment_ratio', 0) >= 3:
                health_score += 10
                strengths.append('良好的代码注释')
            else:
                issues.append('代码注释不足')
            
            # 函数和类的数量
            if code_stats.get('functions', 0) > 20:
                health_score += 10
                strengths.append('功能模块化良好')
            
            if code_stats.get('classes', 0) > 5:
                health_score += 10
                strengths.append('面向对象设计')
        
        # 文档完整性评估
        if 'documentation_stats' in self.stats:
            doc_stats = self.stats['documentation_stats']
            doc_types = doc_stats.get('doc_types', {})
            
            if doc_types.get('README', 0) > 0:
                health_score += 15
                strengths.append('有README文档')
            else:
                issues.append('缺少README文档')
            
            if doc_types.get('API文档', 0) > 0:
                health_score += 10
                strengths.append('有API文档')
            
            if doc_types.get('贡献指南', 0) > 0:
                health_score += 10
                strengths.append('有贡献指南')
            
            if doc_stats.get('total_doc_files', 0) >= 5:
                health_score += 10
                strengths.append('文档齐全')
        
        # 项目结构评估
        if 'file_stats' in self.stats:
            file_stats = self.stats['file_stats']
            by_type = file_stats.get('by_type', {})
            
            if '项目配置' in by_type:
                health_score += 10
                strengths.append('有项目配置文件')
            
            if '配置文件' in by_type:
                health_score += 5
                strengths.append('有应用配置')
        
        # Git使用评估
        if 'git_stats' in self.stats:
            git_stats = self.stats['git_stats']
            if git_stats.get('status') == '已初始化':
                health_score += 10
                strengths.append('使用Git版本控制')
                
                if git_stats.get('commits_count', 0) > 10:
                    health_score += 10
                    strengths.append('活跃的开发历史')
        
        # 数据完整性评估
        if 'data_stats' in self.stats:
            data_stats = self.stats['data_stats']
            if data_stats.get('total_papers', 0) > 0:
                health_score += 10
                strengths.append('有实际数据产出')
        
        # 计算等级
        if health_score >= 80:
            grade = 'A'
            status = '优秀'
        elif health_score >= 60:
            grade = 'B'
            status = '良好'
        elif health_score >= 40:
            grade = 'C'
            status = '一般'
        else:
            grade = 'D'
            status = '需要改进'
        
        return {
            'health_score': health_score,
            'max_score': max_score,
            'grade': grade,
            'status': status,
            'strengths': strengths,
            'issues': issues
        }
    
    def save_stats(self, output_file: str = None) -> str:
        """保存统计信息到文件"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'project_stats_{timestamp}.json'
        
        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def print_summary(self):
        """打印统计摘要"""
        print(f"\n{'='*60}")
        print(f"📊 项目统计报告 - {self.stats['project_name']}")
        print(f"{'='*60}")
        print(f"作者: {self.stats['author']}")
        print(f"版本: {self.stats['version']}")
        print(f"生成时间: {self.stats['timestamp']}")
        
        # 文件统计
        file_stats = self.stats.get('file_stats', {})
        print(f"\n📁 文件统计:")
        print(f"  总文件数: {file_stats.get('total_files', 0)}")
        print(f"  总大小: {file_stats.get('total_size_mb', 0)} MB")
        
        # 代码统计
        code_stats = self.stats.get('code_stats', {})
        if code_stats:
            print(f"\n💻 代码统计:")
            print(f"  Python文件: {code_stats.get('python_files', 0)}")
            print(f"  总行数: {code_stats.get('total_lines', 0)}")
            print(f"  代码行数: {code_stats.get('code_lines', 0)}")
            print(f"  注释行数: {code_stats.get('comment_lines', 0)} + {code_stats.get('docstring_lines', 0)}")
            print(f"  函数数量: {code_stats.get('functions', 0)}")
            print(f"  类数量: {code_stats.get('classes', 0)}")
        
        # 文档统计
        doc_stats = self.stats.get('documentation_stats', {})
        if doc_stats:
            print(f"\n📚 文档统计:")
            print(f"  文档文件: {doc_stats.get('total_doc_files', 0)}")
            print(f"  文档大小: {doc_stats.get('total_doc_size_kb', 0)} KB")
        
        # 数据统计
        data_stats = self.stats.get('data_stats', {})
        if 'total_papers' in data_stats:
            print(f"\n📊 数据统计:")
            print(f"  处理论文: {data_stats.get('total_papers', 0)}")
            print(f"  分析天数: {data_stats.get('analysis_days', 0)}")
            print(f"  平均每日: {data_stats.get('avg_papers_per_day', 0)} 篇")
        
        # 项目健康状况
        health = self.stats.get('project_health', {})
        if health:
            print(f"\n🏥 项目健康:")
            print(f"  健康评分: {health.get('health_score', 0)}/{health.get('max_score', 100)}")
            print(f"  评级: {health.get('grade', 'N/A')} ({health.get('status', '未知')})")
            
            if health.get('strengths'):
                print(f"  优势: {', '.join(health['strengths'][:3])}")
            
            if health.get('issues'):
                print(f"  改进点: {', '.join(health['issues'][:3])}")
        
        print(f"{'='*60}")

def main():
    """主函数"""
    generator = ProjectStatsGenerator()
    
    print("🔍 正在生成项目统计信息...")
    stats = generator.generate_all_stats()
    
    # 打印摘要
    generator.print_summary()
    
    # 保存详细报告
    output_file = generator.save_stats()
    print(f"\n💾 详细报告已保存到: {output_file}")

if __name__ == "__main__":
    main()
