#!/usr/bin/env python3
"""
测试Trend Radar Agent
"""

import asyncio
import os
from agents.trend_radar_agent import TrendRadarAgent

async def main():
    print("🛍️ Marketa-Pro: Trend Radar Agent 测试")
    print("=======================================\n")
    
    # 创建Trend Radar Agent
    print("📊 初始化Trend Radar Agent...")
    trend_radar = TrendRadarAgent()
    
    # 测试小红书平台的趋势分析
    print("\n🧪 TEST 1: 分析小红书平台趋势")
    result1 = await trend_radar.analyze_platform_trends(
        platform="xiaohongshu",
        product_category="smart home devices",
        product_tags=["technology", "smart cup", "health", "lifestyle"]
    )
    
    if result1["status"] == "success":
        print("\n✅ 成功获取小红书趋势分析!")
        print("\n📝 小红书趋势分析:")
        print(result1["trend_analysis"])
    else:
        print(f"\n❌ 分析失败: {result1.get('error', '未知错误')}")
    
    # 测试抖音平台的趋势分析
    print("\n🧪 TEST 2: 分析抖音平台趋势")
    result2 = await trend_radar.analyze_platform_trends(
        platform="tiktok",
        product_category="portable electronics",
        product_tags=["tech", "gadgets", "portable", "lifestyle"]
    )
    
    if result2["status"] == "success":
        print("\n✅ 成功获取抖音趋势分析!")
        print("\n📝 抖音趋势分析:")
        print(result2["trend_analysis"])
    else:
        print(f"\n❌ 分析失败: {result2.get('error', '未知错误')}")
    
    print("\n🔍 您可以比较两个平台的趋势分析，看看不同平台的内容策略差异。")

if __name__ == "__main__":
    # 在Windows上运行需要这个
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    # 运行测试
    asyncio.run(main()) 