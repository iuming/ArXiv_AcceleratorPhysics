#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: llm_analyzer_new.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: 新版LLM分析器模块，支持多种LLM服务(DeepSeek、HEPAI、OpenAI、Anthropic)
             提供更稳定的API调用和增强的错误处理机制

Modification History:
- 2025-07-25: Initial creation based on llm_analyzer.py
- 2025-07-25: Enhanced error handling and retry mechanism
- 2025-07-25: Improved multi-provider support
"""

"""
LLM分析器 - 使用多种LLM服务分析ArXiv论文
支持DeepSeek、HEPAI、OpenAI、Anthropic
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import asyncio

# 条件导入LLM库
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from hepai import Hepai
    HEPAI_AVAILABLE = True
except ImportError:
    HEPAI_AVAILABLE = False


class LLMAnalyzer:
    """LLM分析器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.api_type = None
        
        # 加载提示模板
        self.analysis_prompt = self._load_prompt_template('analysis_prompt.txt')
        self.classification_prompt = self._load_prompt_template('classification_prompt.txt')
        self.keywords_prompt = self._load_prompt_template('keywords_prompt.txt')
        self.summary_prompt = self._load_prompt_template('summary_prompt.txt')
        
        # 初始化LLM客户端
        self.openai_client = None
        self.anthropic_client = None
        self.hepai_client = None
        
        # 优先级1: 检查DeepSeek API密钥
        deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        if OPENAI_AVAILABLE and deepseek_key:
            try:
                self.openai_client = OpenAI(
                    api_key=deepseek_key,
                    base_url="https://api.deepseek.com/v1"
                )
                self.api_type = "deepseek"
                self.logger.info("✅ DeepSeek API客户端初始化成功")
            except Exception as e:
                self.logger.error(f"DeepSeek API初始化失败: {e}")
        
        # 优先级2: 检查HEPAI API密钥
        elif HEPAI_AVAILABLE and os.getenv('HAI_API_KEY'):
            try:
                self.hepai_client = Hepai(api_key=os.getenv('HAI_API_KEY'))
                self.api_type = "hepai"
                self.logger.info("✅ HEPAI客户端初始化成功")
            except Exception as e:
                self.logger.error(f"HEPAI初始化失败: {e}")
        
        # 优先级3: 检查OpenAI API密钥
        elif OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                self.api_type = "openai"
                self.logger.info("✅ OpenAI客户端初始化成功")
            except Exception as e:
                self.logger.error(f"OpenAI初始化失败: {e}")
            
        # 优先级4: 检查Anthropic API密钥
        elif ANTHROPIC_AVAILABLE and os.getenv('ANTHROPIC_API_KEY'):
            try:
                self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                self.api_type = "anthropic"
                self.logger.info("✅ Anthropic客户端初始化成功")
            except Exception as e:
                self.logger.error(f"Anthropic初始化失败: {e}")
        
        if not self.openai_client and not self.anthropic_client and not self.hepai_client:
            self.logger.error("❌ 没有可用的LLM客户端！请设置API密钥：")
            self.logger.error("   - DEEPSEEK_API_KEY (推荐，性价比高)")
            self.logger.error("   - HAI_API_KEY (HEPAI，中科院高能所)")
            self.logger.error("   - OPENAI_API_KEY (备用)")
            self.logger.error("   - ANTHROPIC_API_KEY (可选备用)")
            self.logger.error("   在GitHub仓库Settings -> Secrets中设置这些密钥")
    
    def _load_prompt_template(self, filename: str) -> str:
        """加载提示模板"""
        template_path = os.path.join('templates', filename)
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            self.logger.warning(f"提示模板文件未找到: {filename}")
            return self._get_default_prompt(filename)
    
    def _get_default_prompt(self, filename: str) -> str:
        """获取默认提示模板"""
        if 'analysis' in filename:
            return """
请对以下加速器物理论文进行详细分析：

标题：{title}
作者：{authors}
摘要：{abstract}

请从以下几个方面进行分析：

1. **研究主题**：论文的核心研究内容是什么？
2. **技术创新**：论文提出了哪些新的技术、方法或理论？
3. **应用价值**：这项研究在加速器物理领域的实际应用价值如何？
4. **技术难点**：论文解决了哪些技术难题？
5. **研究意义**：对加速器物理学科发展的意义如何？
6. **未来展望**：可能的后续研究方向或应用前景？

请用中文回答，保持专业性和准确性。
"""
        elif 'classification' in filename:
            return """
请对以下加速器物理论文进行分类：

标题：{title}
摘要：{abstract}

请从以下分类中选择最适合的类别：

1. 束流动力学 (Beam Dynamics)
2. 射频技术 (RF Technology)
3. 磁体技术 (Magnet Technology)
4. 束流诊断 (Beam Diagnostics)
5. 加速器设计 (Accelerator Design)
6. 超导技术 (Superconducting Technology)
7. 真空技术 (Vacuum Technology)
8. 控制系统 (Control Systems)
9. 其他 (Others)

请只返回类别名称和编号。
"""
        elif 'keywords' in filename:
            return """
请从以下加速器物理论文中提取关键词：

标题：{title}
摘要：{abstract}

请提取5-8个最重要的技术关键词，用逗号分隔。
"""
        else:  # summary
            return """
基于以下论文分析，生成一个简要总结：

论文标题：{title}
详细分析：{analysis}

请用1-2句话概括论文的核心贡献和意义。
"""
    
    async def analyze_paper(self, paper: Dict) -> Dict:
        """
        分析单篇论文
        
        Args:
            paper: 论文信息字典
            
        Returns:
            分析结果字典
        """
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'paper_id': paper.get('arxiv_id'),
            'analysis': None,
            'classification': None,
            'keywords': [],
            'summary': None,
            'error': None
        }
        
        try:
            # 1. 详细分析
            analysis_result['analysis'] = await self._perform_detailed_analysis(paper)
            
            # 2. 分类
            analysis_result['classification'] = await self._classify_paper(paper)
            
            # 3. 提取关键词
            analysis_result['keywords'] = await self._extract_keywords(paper)
            
            # 4. 生成简要总结
            analysis_result['summary'] = await self._generate_summary(paper, analysis_result['analysis'])
            
            self.logger.info(f"✅ 论文分析完成: {paper.get('title', 'Unknown')[:50]}...")
            
        except Exception as e:
            self.logger.error(f"❌ 论文分析失败: {e}")
            analysis_result['error'] = str(e)
            
        return analysis_result
    
    async def _perform_detailed_analysis(self, paper: Dict) -> str:
        """执行详细分析"""
        prompt = self.analysis_prompt.format(
            title=paper.get('title', ''),
            authors=', '.join(paper.get('authors', [])),
            abstract=paper.get('abstract', '')
        )
        
        return await self._call_llm(prompt, max_tokens=1500)
    
    async def _classify_paper(self, paper: Dict) -> Dict:
        """论文分类"""
        prompt = self.classification_prompt.format(
            title=paper.get('title', ''),
            abstract=paper.get('abstract', '')
        )
        
        classification_text = await self._call_llm(prompt, max_tokens=100)
        
        # 解析分类结果
        return {
            'category': classification_text.strip(),
            'confidence': 0.8  # 默认置信度
        }
    
    async def _extract_keywords(self, paper: Dict) -> List[str]:
        """提取关键词"""
        prompt = self.keywords_prompt.format(
            title=paper.get('title', ''),
            abstract=paper.get('abstract', '')
        )
        
        keywords_text = await self._call_llm(prompt, max_tokens=200)
        
        # 解析关键词
        keywords = [kw.strip() for kw in keywords_text.split(',')]
        return keywords[:8]  # 最多8个关键词
    
    async def _generate_summary(self, paper: Dict, analysis: str) -> str:
        """生成简要总结"""
        if not analysis:
            return "分析失败，无法生成总结"
            
        prompt = self.summary_prompt.format(
            title=paper.get('title', ''),
            analysis=analysis
        )
        
        return await self._call_llm(prompt, max_tokens=300)
    
    async def _call_llm(self, prompt: str, max_tokens: int = 1000) -> str:
        """调用LLM API"""
        
        # 优先级1: DeepSeek（已初始化的客户端）
        if self.openai_client and self.api_type == "deepseek":
            try:
                response = self.openai_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个专业的加速器物理学专家，擅长分析和解读科学论文。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                self.logger.warning(f"DeepSeek调用失败，尝试其他服务: {e}")
        
        # 优先级2: HEPAI
        if self.hepai_client:
            try:
                response = self.hepai_client.completions.create(
                    model="deepseek-v2.5",
                    prompt=f"你是一个专业的加速器物理学专家。{prompt}",
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].text.strip()
            except Exception as e:
                self.logger.warning(f"HEPAI调用失败，尝试其他服务: {e}")
        
        # 优先级3: OpenAI（原版）
        if self.openai_client and self.api_type == "openai":
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一个专业的加速器物理学专家，擅长分析和解读科学论文。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                self.logger.warning(f"OpenAI调用失败，尝试其他服务: {e}")
        
        # 备用: Anthropic
        if self.anthropic_client:
            try:
                message = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=max_tokens,
                    temperature=0.7,
                    messages=[{
                        "role": "user", 
                        "content": f"你是一个专业的加速器物理学专家。{prompt}"
                    }]
                )
                return message.content[0].text.strip()
            except Exception as e:
                self.logger.error(f"Anthropic调用失败: {e}")
        
        raise Exception("所有LLM服务都不可用")
    
    def get_available_services(self) -> List[str]:
        """获取可用的LLM服务列表"""
        services = []
        if self.openai_client:
            services.append(f"OpenAI ({self.api_type})")
        if self.anthropic_client:
            services.append("Anthropic")
        if self.hepai_client:
            services.append("HEPAI")
        return services
