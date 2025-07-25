#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: ArXiv_AcceleratorPhysics
File: test_api.py
Author: Ming Liu
Email: ming-1018@foxmail.com
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: July 25th, 2025
Description: API连接测试脚本，用于测试DeepSeek和HEPAI等LLM服务的连通性
             确保API配置正确和服务可用性

Modification History:
- 2025-07-25: Initial creation
- 2025-07-25: Added comprehensive API testing
"""

"""
测试DeepSeek和HEPAI API连接
"""

import os
import asyncio
from openai import OpenAI

async def test_deepseek():
    """测试DeepSeek API"""
    print("🔍 测试DeepSeek API连接...")
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ DEEPSEEK_API_KEY环境变量未设置")
        return False
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=50
        )
        
        print(f"✅ DeepSeek API连接成功！")
        print(f"响应: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek API连接失败: {e}")
        return False

async def test_hepai():
    """测试HEPAI API"""
    print("\n🔍 测试HEPAI API连接...")
    
    api_key = os.getenv('HAI_API_KEY')
    if not api_key:
        print("❌ HAI_API_KEY环境变量未设置")
        return False
    
    try:
        # 由于hepai库可能还未安装，先跳过测试
        print("⚠️  HEPAI库需要先安装，跳过测试")
        return False
        
    except Exception as e:
        print(f"❌ HEPAI API连接失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始API连接测试...")
    
    deepseek_ok = await test_deepseek()
    hepai_ok = await test_hepai()
    
    print(f"\n📊 测试结果:")
    print(f"DeepSeek API: {'✅ 正常' if deepseek_ok else '❌ 失败'}")
    print(f"HEPAI API: {'✅ 正常' if hepai_ok else '❌ 失败'}")
    
    if not deepseek_ok and not hepai_ok:
        print("\n⚠️  请检查以下事项:")
        print("1. 确保设置了正确的API密钥环境变量")
        print("2. 检查网络连接")
        print("3. 验证API密钥是否有效")

if __name__ == "__main__":
    asyncio.run(main())
