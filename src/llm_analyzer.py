import asyncio
import json
import os
from typing import Dict, List, Optional
import logging
from datetime import datetime

# 动态导入LLM库
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class LLMAnalyzer:
    """LLM论文分析器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 初始化LLM客户端
        self.openai_client = None
        self.anthropic_client = None
        
        # 配置OpenAI
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.openai_client = openai
            self.logger.info("✅ OpenAI客户端初始化成功")
        elif OPENAI_AVAILABLE:
            self.logger.warning("⚠️  OPENAI_API_KEY环境变量未设置")
        else:
            self.logger.warning("⚠️  OpenAI库未安装")
            
        # 配置Anthropic
        if ANTHROPIC_AVAILABLE and os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            self.logger.info("✅ Anthropic客户端初始化成功")
        elif ANTHROPIC_AVAILABLE:
            self.logger.warning("⚠️  ANTHROPIC_API_KEY环境变量未设置")
        else:
            self.logger.warning("⚠️  Anthropic库未安装")
        
        if not self.openai_client and not self.anthropic_client:
            self.logger.error("❌ 没有可用的LLM客户端！请设置API密钥：")
            self.logger.error("   - OPENAI_API_KEY (必需)")
            self.logger.error("   - ANTHROPIC_API_KEY (可选备用)")
            self.logger.error("   在GitHub仓库Settings -> Secrets中设置这些密钥")
        
        # 加载提示模板
        self.analysis_prompt = self._load_prompt_template('analysis_prompt.txt')
        self.classification_prompt = self._load_prompt_template('classification_prompt.txt')
        
    def _load_prompt_template(self, filename: str) -> str:
        """加载提示模板"""
        try:
            template_path = os.path.join('templates', filename)
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
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
        else:
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
        return self._parse_classification(classification_text)
    
    async def _extract_keywords(self, paper: Dict) -> List[str]:
        """提取关键词"""
        prompt = f"""
请从以下加速器物理论文中提取5-10个关键技术词汇：

标题：{paper.get('title', '')}
摘要：{paper.get('abstract', '')}

请只返回关键词列表，用逗号分隔。
"""
        
        keywords_text = await self._call_llm(prompt, max_tokens=200)
        
        # 解析关键词
        keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
        return keywords[:10]  # 最多10个关键词
    
    async def _generate_summary(self, paper: Dict, analysis: str) -> str:
        """生成简要总结"""
        prompt = f"""
基于以下论文信息和分析结果，请生成一个150字以内的简要总结：

论文标题：{paper.get('title', '')}
详细分析：{analysis}

请用中文总结论文的核心贡献和价值。
"""
        
        return await self._call_llm(prompt, max_tokens=300)
    
    async def _call_llm(self, prompt: str, max_tokens: int = 1000) -> str:
        """调用LLM API"""
        
        # 优先使用OpenAI
        if self.openai_client:
            try:
                response = await self._call_openai(prompt, max_tokens)
                if response:
                    return response
            except Exception as e:
                self.logger.warning(f"OpenAI调用失败，尝试Anthropic: {e}")
        
        # 备用Anthropic
        if self.anthropic_client:
            try:
                return await self._call_anthropic(prompt, max_tokens)
            except Exception as e:
                self.logger.error(f"Anthropic调用失败: {e}")
        
        raise Exception("所有LLM服务都不可用")
    
    async def _call_openai(self, prompt: str, max_tokens: int) -> str:
        """调用OpenAI API"""
        try:
            response = await self.openai_client.ChatCompletion.acreate(
                model=self.config.get('openai_model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "你是一个专业的加速器物理学专家，擅长分析和解读科学论文。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI API调用错误: {e}")
            raise
    
    async def _call_anthropic(self, prompt: str, max_tokens: int) -> str:
        """调用Anthropic API"""
        try:
            message = await self.anthropic_client.messages.create(
                model=self.config.get('anthropic_model', 'claude-3-sonnet-20240229'),
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": f"你是一个专业的加速器物理学专家。{prompt}"}
                ]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            self.logger.error(f"Anthropic API调用错误: {e}")
            raise
    
    def _parse_classification(self, classification_text: str) -> Dict:
        """解析分类结果"""
        # 定义分类映射
        categories = {
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
        
        # 尝试从文本中提取分类
        for num, category in categories.items():
            if num in classification_text or category in classification_text:
                return {
                    "category_id": num,
                    "category_name": category,
                    "confidence": "high"
                }
        
        # 默认分类
        return {
            "category_id": "9",
            "category_name": "其他",
            "confidence": "low"
        }
