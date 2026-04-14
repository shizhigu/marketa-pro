#!/usr/bin/env python3
"""
测试Content Strategy Map Agent
"""

import asyncio
import os
from agents.content_strategy_map_agent import ContentStrategyMapAgent

async def main():
    print("🛍️ Marketa-Pro: Content Strategy Map Agent 测试")
    print("===============================================\n")
    
    # 创建Content Strategy Map Agent
    print("📊 初始化Content Strategy Map Agent...")
    strategy_mapper = ContentStrategyMapAgent()
    
    # 示例Campaign Plan数据
    campaign_plan = {
        "campaign_plan": """
        ## Campaign Objectives
        - Drive awareness of new Smart Thermos Cup product
        - Position product as a premium, tech-forward lifestyle accessory
        - Generate 50,000+ views across Xiaohongshu content
        
        ## Audience Insights
        Urban professionals 25-35 who value both aesthetics and functionality in their daily items.
        They are tech-savvy, health-conscious, and respond well to minimalist design.
        
        ## Key Messages
        - 24-hour heat retention for all-day temperature control
        - APP connectivity provides real-time temperature monitoring
        - Hydration tracking encourages better health habits
        
        ## Content Structure
        - Hero product introduction with lifestyle context
        - Feature-benefit breakdown with visual demonstrations
        - Daily routine integration scenarios
        
        ## Platform Adaptation Strategy
        For Xiaohongshu: Focus on aesthetic appeal with minimalist photography and personal testimonial style.
        
        ## Brand Voice Implementation
        Clean, precise language with technical terminology balanced by approachable explanations.
        
        ## Performance Indicators
        - Engagement rate: aim for 5%+ (likes, comments, saves)
        - View-to-click ratio: 10% or higher
        - Content sharing: 2% of viewers
        """
    }
    
    # 示例Trend Analysis数据
    trend_analysis = {
        "trend_analysis": """
        Current Platform Trends:
        - Morning routine videos featuring tech products are receiving 40% higher engagement
        - Minimalist aesthetic product showcases are trending in the lifestyle category
        - Health-focused content is seeing increased save rates among urban users
        
        Relevant Hashtags:
        - #SmartLiving
        - #MorningRoutine
        - #TechForHealth
        - #HydrationCheck
        - #MinimalistTech
        
        Content Format Recommendations:
        - Short carousel posts showing product features have 32% higher conversion
        - Day-in-the-life format is currently trending with 25-35 age demographic
        - Comparison content with traditional products generates higher comment rates
        
        Optimal Posting Times:
        - Weekday mornings (7-9 AM) for routine-based content
        - Sunday evenings (7-9 PM) for planning/aspirational content
        """
    }
    
    # 测试不带趋势分析的内容策略生成
    print("\n🧪 TEST 1: 生成内容策略地图（不包含趋势分析）")
    result1 = await strategy_mapper.create_content_strategy_map(campaign_plan)
    
    if result1["status"] == "success":
        print("\n✅ 成功生成内容策略地图（不含趋势分析）!")
        print("\n📝 内容策略地图（不含趋势分析）:")
        print(result1["content_strategy_map"])
    else:
        print(f"\n❌ 生成失败: {result1.get('error', '未知错误')}")
    
    # 测试带趋势分析的内容策略生成
    print("\n🧪 TEST 2: 生成内容策略地图（包含趋势分析）")
    result2 = await strategy_mapper.create_content_strategy_map(campaign_plan, trend_analysis)
    
    if result2["status"] == "success":
        print("\n✅ 成功生成内容策略地图（含趋势分析）!")
        print("\n📝 内容策略地图（含趋势分析）:")
        print(result2["content_strategy_map"])
    else:
        print(f"\n❌ 生成失败: {result2.get('error', '未知错误')}")
    
    print("\n🔍 您可以比较两个内容策略地图，看看趋势分析是如何影响策略的。")

if __name__ == "__main__":
    # 在Windows上运行需要这个
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    # 运行测试
    asyncio.run(main()) 