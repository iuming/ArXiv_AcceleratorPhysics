import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from urllib.parse import urlencode

class ArXivFetcher:
    """ArXiv论文抓取器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "http://export.arxiv.org/api/query"
        self.category = "physics.acc-ph"  # 加速器物理分类
        self.max_papers = config.get('max_papers_per_day', 20)
        self.logger = logging.getLogger(__name__)
        
    async def fetch_recent_papers(self, days_back: int = 1) -> List[Dict]:
        """
        抓取最近几天的论文
        
        Args:
            days_back: 回溯天数，默认1天
            
        Returns:
            论文列表
        """
        papers = []
        
        # 计算查询日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # 构建查询参数
        query_params = {
            'search_query': f'cat:{self.category}',
            'start': 0,
            'max_results': self.max_papers,
            'sortBy': 'lastUpdatedDate',
            'sortOrder': 'descending'
        }
        
        url = f"{self.base_url}?{urlencode(query_params)}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        papers = self._parse_arxiv_response(content, start_date)
                    else:
                        self.logger.error(f"ArXiv API请求失败: {response.status}")
                        
        except Exception as e:
            self.logger.error(f"抓取论文时发生错误: {e}")
            
        return papers
    
    def _parse_arxiv_response(self, xml_content: str, start_date: datetime) -> List[Dict]:
        """解析ArXiv API响应"""
        papers = []
        
        try:
            root = ET.fromstring(xml_content)
            
            # 定义命名空间
            namespaces = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            entries = root.findall('atom:entry', namespaces)
            
            for entry in entries:
                # 获取更新时间
                updated = entry.find('atom:updated', namespaces)
                if updated is not None:
                    updated_date = datetime.fromisoformat(updated.text.replace('Z', '+00:00'))
                    
                    # 只保留指定日期范围内的论文
                    if updated_date.date() >= start_date.date():
                        paper = self._extract_paper_info(entry, namespaces)
                        if paper:
                            papers.append(paper)
                            
        except ET.ParseError as e:
            self.logger.error(f"解析XML响应失败: {e}")
        except Exception as e:
            self.logger.error(f"处理ArXiv响应时发生错误: {e}")
            
        return papers
    
    def _extract_paper_info(self, entry, namespaces: Dict) -> Optional[Dict]:
        """从XML条目中提取论文信息"""
        try:
            # 基本信息
            paper = {}
            
            # ArXiv ID
            id_elem = entry.find('atom:id', namespaces)
            if id_elem is not None:
                arxiv_id = id_elem.text.split('/')[-1]
                paper['arxiv_id'] = arxiv_id
                paper['url'] = f"https://arxiv.org/abs/{arxiv_id}"
                paper['pdf_url'] = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            
            # 标题
            title_elem = entry.find('atom:title', namespaces)
            if title_elem is not None:
                paper['title'] = title_elem.text.strip().replace('\n', ' ')
            
            # 摘要
            summary_elem = entry.find('atom:summary', namespaces)
            if summary_elem is not None:
                paper['abstract'] = summary_elem.text.strip().replace('\n', ' ')
            
            # 作者
            authors = []
            author_elems = entry.findall('atom:author', namespaces)
            for author_elem in author_elems:
                name_elem = author_elem.find('atom:name', namespaces)
                if name_elem is not None:
                    authors.append(name_elem.text.strip())
            paper['authors'] = authors
            
            # 发布日期
            published_elem = entry.find('atom:published', namespaces)
            if published_elem is not None:
                paper['published'] = published_elem.text
            
            # 更新日期
            updated_elem = entry.find('atom:updated', namespaces)
            if updated_elem is not None:
                paper['updated'] = updated_elem.text
            
            # 类别
            categories = []
            category_elems = entry.findall('atom:category', namespaces)
            for cat_elem in category_elems:
                term = cat_elem.get('term')
                if term:
                    categories.append(term)
            paper['categories'] = categories
            
            # 主要类别
            primary_category = entry.find('arxiv:primary_category', namespaces)
            if primary_category is not None:
                paper['primary_category'] = primary_category.get('term')
            
            # DOI（如果有）
            doi_elem = entry.find('arxiv:doi', namespaces)
            if doi_elem is not None:
                paper['doi'] = doi_elem.text
            
            return paper
            
        except Exception as e:
            self.logger.error(f"提取论文信息失败: {e}")
            return None
    
    async def download_pdf(self, paper: Dict, save_path: str) -> bool:
        """
        下载论文PDF
        
        Args:
            paper: 论文信息字典
            save_path: 保存路径
            
        Returns:
            是否成功下载
        """
        if 'pdf_url' not in paper:
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(paper['pdf_url']) as response:
                    if response.status == 200:
                        with open(save_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)
                        return True
                    else:
                        self.logger.error(f"下载PDF失败: {response.status}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"下载PDF时发生错误: {e}")
            return False
