#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: health_check.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: 项目健康状态监控脚本，检查API连接、数据完整性、系统状态等
             提供全面的系统健康诊断和问题报告

Modification History:
- 2025-07-25: Initial creation
- 2025-07-25: Added comprehensive health monitoring
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import aiohttp
import yaml

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import setup_logging

class HealthChecker:
    """系统健康状态检查器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results = {}
        self.issues = []
        
    async def run_all_checks(self) -> Dict[str, Any]:
        """运行所有健康检查"""
        self.logger.info("🏥 开始系统健康检查...")
        
        checks = [
            ("🔑 API密钥检查", self.check_api_keys),
            ("🌐 网络连接检查", self.check_network_connectivity),
            ("📁 文件系统检查", self.check_file_system),
            ("📊 数据完整性检查", self.check_data_integrity),
            ("⚙️ 配置文件检查", self.check_configuration),
            ("📦 依赖包检查", self.check_dependencies),
            ("📈 性能指标检查", self.check_performance_metrics),
            ("🔒 安全检查", self.check_security),
        ]
        
        for check_name, check_func in checks:
            try:
                self.logger.info(f"执行 {check_name}...")
                result = await check_func()
                self.results[check_name] = result
                if not result.get('status', True):
                    self.issues.append(f"{check_name}: {result.get('message', '未知错误')}")
            except Exception as e:
                self.logger.error(f"{check_name} 失败: {e}")
                self.results[check_name] = {'status': False, 'error': str(e)}
                self.issues.append(f"{check_name}: {str(e)}")
        
        # 生成总体健康报告
        overall_health = len(self.issues) == 0
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': overall_health,
            'total_checks': len(checks),
            'passed_checks': len([r for r in self.results.values() if r.get('status', True)]),
            'failed_checks': len(self.issues),
            'issues': self.issues,
            'detailed_results': self.results,
            'recommendations': self.generate_recommendations()
        }
        
        self.logger.info(f"✅ 健康检查完成。总体状态: {'健康' if overall_health else '存在问题'}")
        return report
    
    async def check_api_keys(self) -> Dict[str, Any]:
        """检查API密钥配置"""
        api_keys = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY'),
            'HEPAI_API_KEY': os.getenv('HEPAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        }
        
        configured_keys = {k: v for k, v in api_keys.items() if v}
        
        if not configured_keys:
            return {
                'status': False,
                'message': '没有配置任何API密钥',
                'configured_keys': []
            }
        
        # 测试API连接
        working_keys = []
        for key_name, key_value in configured_keys.items():
            if await self._test_api_key(key_name, key_value):
                working_keys.append(key_name)
        
        status = len(working_keys) > 0
        return {
            'status': status,
            'message': f'配置了 {len(configured_keys)} 个密钥，其中 {len(working_keys)} 个可用',
            'configured_keys': list(configured_keys.keys()),
            'working_keys': working_keys
        }
    
    async def _test_api_key(self, key_name: str, key_value: str) -> bool:
        """测试单个API密钥"""
        try:
            if key_name == 'OPENAI_API_KEY':
                return await self._test_openai_key(key_value)
            elif key_name == 'DEEPSEEK_API_KEY':
                return await self._test_deepseek_key(key_value)
            # 可以添加其他API的测试
            return True  # 暂时返回True
        except:
            return False
    
    async def _test_openai_key(self, api_key: str) -> bool:
        """测试OpenAI API密钥"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {api_key}'}
                async with session.get(
                    'https://api.openai.com/v1/models',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def _test_deepseek_key(self, api_key: str) -> bool:
        """测试DeepSeek API密钥"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {api_key}'}
                async with session.get(
                    'https://api.deepseek.com/v1/models',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def check_network_connectivity(self) -> Dict[str, Any]:
        """检查网络连接"""
        test_urls = [
            'https://export.arxiv.org/api/query',
            'https://api.openai.com',
            'https://api.deepseek.com',
            'https://github.com'
        ]
        
        working_connections = 0
        connection_details = {}
        
        async with aiohttp.ClientSession() as session:
            for url in test_urls:
                try:
                    start_time = datetime.now()
                    async with session.get(
                        url,
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as response:
                        response_time = (datetime.now() - start_time).total_seconds()
                        connection_details[url] = {
                            'status': 'ok',
                            'response_time': response_time,
                            'status_code': response.status
                        }
                        working_connections += 1
                except Exception as e:
                    connection_details[url] = {
                        'status': 'failed',
                        'error': str(e)
                    }
        
        status = working_connections >= len(test_urls) // 2  # 至少一半的连接正常
        return {
            'status': status,
            'message': f'{working_connections}/{len(test_urls)} 个网络连接正常',
            'details': connection_details
        }
    
    async def check_file_system(self) -> Dict[str, Any]:
        """检查文件系统状态"""
        required_dirs = [
            'data',
            'data/papers',
            'data/analysis',
            'data/statistics',
            'logs',
            'config',
            'templates'
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if not Path(dir_path).exists():
                missing_dirs.append(dir_path)
        
        # 检查磁盘空间
        disk_usage = self._get_disk_usage()
        
        # 检查文件权限
        permission_issues = self._check_file_permissions()
        
        status = len(missing_dirs) == 0 and disk_usage['free_gb'] > 1.0
        issues = []
        if missing_dirs:
            issues.append(f"缺少目录: {', '.join(missing_dirs)}")
        if disk_usage['free_gb'] < 1.0:
            issues.append(f"磁盘空间不足: 剩余 {disk_usage['free_gb']:.2f}GB")
        if permission_issues:
            issues.extend(permission_issues)
        
        return {
            'status': status,
            'message': '文件系统正常' if status else '; '.join(issues),
            'missing_directories': missing_dirs,
            'disk_usage': disk_usage,
            'permission_issues': permission_issues
        }
    
    def _get_disk_usage(self) -> Dict[str, float]:
        """获取磁盘使用情况"""
        import shutil
        
        try:
            total, used, free = shutil.disk_usage('.')
            return {
                'total_gb': total / (1024**3),
                'used_gb': used / (1024**3),
                'free_gb': free / (1024**3),
                'usage_percent': (used / total) * 100
            }
        except:
            return {'total_gb': 0, 'used_gb': 0, 'free_gb': 0, 'usage_percent': 100}
    
    def _check_file_permissions(self) -> List[str]:
        """检查文件权限"""
        issues = []
        
        # 检查关键文件的读写权限
        critical_paths = [
            'config/settings.yaml',
            'data',
            'logs'
        ]
        
        for path_str in critical_paths:
            path = Path(path_str)
            if path.exists():
                if not os.access(path, os.R_OK):
                    issues.append(f"无法读取 {path}")
                if path.is_dir() and not os.access(path, os.W_OK):
                    issues.append(f"无法写入 {path}")
        
        return issues
    
    async def check_data_integrity(self) -> Dict[str, Any]:
        """检查数据完整性"""
        data_issues = []
        
        # 检查最近几天的数据
        for i in range(7):  # 检查最近7天
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            papers_file = Path(f'data/papers/{date}/papers.json')
            analysis_file = Path(f'data/analysis/{date}/analysis_results.json')
            
            if papers_file.exists():
                try:
                    with open(papers_file, 'r', encoding='utf-8') as f:
                        papers_data = json.load(f)
                    
                    if not isinstance(papers_data, list):
                        data_issues.append(f"{date}: 论文数据格式错误")
                    elif len(papers_data) == 0:
                        data_issues.append(f"{date}: 没有论文数据")
                    
                    # 如果有论文数据但没有分析结果
                    if len(papers_data) > 0 and not analysis_file.exists():
                        data_issues.append(f"{date}: 有论文数据但缺少分析结果")
                        
                except json.JSONDecodeError:
                    data_issues.append(f"{date}: 论文数据JSON格式错误")
                except Exception as e:
                    data_issues.append(f"{date}: 读取论文数据失败 - {e}")
        
        # 检查统计数据
        stats_files = [
            'data/statistics/overall_stats.json',
            'data/statistics/category_distribution.json'
        ]
        
        for stats_file in stats_files:
            if not Path(stats_file).exists():
                data_issues.append(f"缺少统计文件: {stats_file}")
        
        status = len(data_issues) == 0
        return {
            'status': status,
            'message': '数据完整性正常' if status else f'发现 {len(data_issues)} 个数据问题',
            'issues': data_issues
        }
    
    async def check_configuration(self) -> Dict[str, Any]:
        """检查配置文件"""
        config_issues = []
        
        # 检查主配置文件
        config_file = Path('config/settings.yaml')
        if not config_file.exists():
            config_issues.append('主配置文件不存在')
        else:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                # 检查必要的配置项
                required_sections = ['arxiv', 'llm', 'storage']
                for section in required_sections:
                    if section not in config:
                        config_issues.append(f'配置缺少 {section} 部分')
                
                # 检查具体配置
                if 'arxiv' in config:
                    if config['arxiv'].get('max_papers_per_day', 0) <= 0:
                        config_issues.append('max_papers_per_day 配置无效')
                
            except yaml.YAMLError:
                config_issues.append('配置文件YAML格式错误')
            except Exception as e:
                config_issues.append(f'读取配置文件失败: {e}')
        
        # 检查模板文件
        template_files = [
            'templates/analysis_prompt.txt',
            'templates/classification_prompt.txt'
        ]
        
        for template_file in template_files:
            if not Path(template_file).exists():
                config_issues.append(f'模板文件不存在: {template_file}')
        
        status = len(config_issues) == 0
        return {
            'status': status,
            'message': '配置正常' if status else f'发现 {len(config_issues)} 个配置问题',
            'issues': config_issues
        }
    
    async def check_dependencies(self) -> Dict[str, Any]:
        """检查依赖包"""
        import pkg_resources
        import subprocess
        
        missing_packages = []
        outdated_packages = []
        
        # 读取requirements.txt
        try:
            with open('requirements.txt', 'r') as f:
                requirements = f.read().splitlines()
            
            for requirement in requirements:
                if requirement.strip() and not requirement.startswith('#'):
                    package_name = requirement.split('>=')[0].split('==')[0].strip()
                    try:
                        pkg_resources.get_distribution(package_name)
                    except pkg_resources.DistributionNotFound:
                        missing_packages.append(package_name)
        
        except FileNotFoundError:
            missing_packages.append('requirements.txt不存在')
        
        # 检查是否有可更新的包
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                outdated = json.loads(result.stdout)
                outdated_packages = [pkg['name'] for pkg in outdated]
        except:
            pass  # 忽略错误
        
        status = len(missing_packages) == 0
        return {
            'status': status,
            'message': f'依赖检查完成，缺少 {len(missing_packages)} 个包，{len(outdated_packages)} 个包可更新',
            'missing_packages': missing_packages,
            'outdated_packages': outdated_packages[:10]  # 只显示前10个
        }
    
    async def check_performance_metrics(self) -> Dict[str, Any]:
        """检查性能指标"""
        import psutil
        
        # 系统资源使用情况
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # 检查日志文件大小
        log_files = list(Path('logs').glob('*.log')) if Path('logs').exists() else []
        large_log_files = []
        
        for log_file in log_files:
            size_mb = log_file.stat().st_size / (1024 * 1024)
            if size_mb > 100:  # 大于100MB
                large_log_files.append({'file': str(log_file), 'size_mb': size_mb})
        
        # 检查数据目录大小
        data_size = self._get_directory_size('data') if Path('data').exists() else 0
        
        performance_issues = []
        if cpu_percent > 80:
            performance_issues.append(f'CPU使用率过高: {cpu_percent}%')
        if memory.percent > 85:
            performance_issues.append(f'内存使用率过高: {memory.percent}%')
        if large_log_files:
            performance_issues.append(f'发现 {len(large_log_files)} 个大日志文件')
        
        status = len(performance_issues) == 0
        return {
            'status': status,
            'message': '性能正常' if status else f'发现 {len(performance_issues)} 个性能问题',
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'data_size_mb': data_size / (1024 * 1024),
            'large_log_files': large_log_files,
            'issues': performance_issues
        }
    
    def _get_directory_size(self, path: str) -> int:
        """获取目录大小"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except:
                    pass
        return total_size
    
    async def check_security(self) -> Dict[str, Any]:
        """安全检查"""
        security_issues = []
        
        # 检查敏感文件权限
        sensitive_files = [
            'config/settings.yaml',
            '.env',
            '.env.local'
        ]
        
        for file_path in sensitive_files:
            path = Path(file_path)
            if path.exists():
                # 在Unix系统上检查文件权限
                if hasattr(os, 'stat') and hasattr(os.stat(file_path), 'st_mode'):
                    mode = oct(os.stat(file_path).st_mode)[-3:]
                    if mode != '600' and mode != '644':
                        security_issues.append(f'{file_path} 权限过于宽松: {mode}')
        
        # 检查是否意外提交了敏感信息
        gitignore_path = Path('.gitignore')
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            
            sensitive_patterns = ['.env', '*.key', 'secrets.yaml']
            missing_patterns = [p for p in sensitive_patterns if p not in gitignore_content]
            
            if missing_patterns:
                security_issues.append(f'.gitignore缺少敏感文件模式: {", ".join(missing_patterns)}')
        
        # 检查默认密码或API密钥
        default_patterns = ['sk-test', 'your-api-key', 'changeme', 'default']
        for env_var in os.environ:
            if 'API_KEY' in env_var or 'TOKEN' in env_var or 'SECRET' in env_var:
                value = os.environ[env_var].lower()
                for pattern in default_patterns:
                    if pattern in value:
                        security_issues.append(f'环境变量 {env_var} 可能使用了默认值')
        
        status = len(security_issues) == 0
        return {
            'status': status,
            'message': '安全检查通过' if status else f'发现 {len(security_issues)} 个安全问题',
            'issues': security_issues
        }
    
    def generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于检查结果生成建议
        for check_name, result in self.results.items():
            if not result.get('status', True):
                if 'API密钥' in check_name:
                    recommendations.append('配置至少一个有效的LLM API密钥')
                elif '网络连接' in check_name:
                    recommendations.append('检查网络连接和防火墙设置')
                elif '文件系统' in check_name:
                    recommendations.append('确保必要的目录存在且有适当权限')
                elif '数据完整性' in check_name:
                    recommendations.append('检查数据处理流程和错误处理')
                elif '配置文件' in check_name:
                    recommendations.append('验证配置文件格式和必要设置')
                elif '依赖包' in check_name:
                    recommendations.append('运行 pip install -r requirements.txt')
                elif '性能' in check_name:
                    recommendations.append('考虑清理日志文件和优化系统资源')
                elif '安全' in check_name:
                    recommendations.append('审查文件权限和敏感信息保护')
        
        # 通用建议
        if not recommendations:
            recommendations.append('系统运行正常，建议定期运行健康检查')
        
        return recommendations[:5]  # 限制建议数量

async def main():
    """主函数"""
    logger = setup_logging()
    
    try:
        checker = HealthChecker()
        report = await checker.run_all_checks()
        
        # 保存报告
        report_dir = Path('logs/health_reports')
        report_dir.mkdir(exist_ok=True)
        
        report_file = report_dir / f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 输出摘要
        print(f"\n{'='*60}")
        print(f"🏥 系统健康检查报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"总体状态: {'✅ 健康' if report['overall_health'] else '❌ 存在问题'}")
        print(f"检查项目: {report['passed_checks']}/{report['total_checks']} 通过")
        
        if report['issues']:
            print(f"\n🚨 发现的问题:")
            for issue in report['issues']:
                print(f"  • {issue}")
        
        if report['recommendations']:
            print(f"\n💡 改进建议:")
            for rec in report['recommendations']:
                print(f"  • {rec}")
        
        print(f"\n📋 详细报告已保存到: {report_file}")
        print(f"{'='*60}")
        
        # 如果有问题，以非零退出码退出
        sys.exit(0 if report['overall_health'] else 1)
        
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
