#!/usr/bin/env python3
"""
测试完整的Marketa-Pro工作流
"""

import asyncio
import os
import json
from agents.orchestrator_agent import OrchestratorAgent

async def main():
    print("🛍️ Marketa-Pro: 完整工作流测试")
    print("==============================\n")
    
    # 创建Orchestrator Agent
    print("📊 初始化Orchestrator Agent...")
    orchestrator = OrchestratorAgent()
    
    # 示例用户输入
    user_input = {
        "goal": "新产品种草推广",
        "product_title": "智能保温杯",
        "product_selling_points": "24小时保温保冷，APP温度显示，喝水提醒功能",
        "product_tags": "科技,健康,生活方式",
        "product_category": "生活用品",
        "platform": "xiaohongshu",
        "brand_tone": "极简科技风",
        "audience": "25-35岁都市年轻人"
    }
    
    print("\n📝 处理用户输入:")
    print(json.dumps(user_input, indent=2, ensure_ascii=False))
    
    print("\n🚀 开始执行工作流...")
    result = await orchestrator.process_user_input(user_input)
    
    if result["status"] == "content_strategy_completed":
        print("\n✅ 工作流执行成功!")
        
        print("\n📋 初始规划结果:")
        print(result["initial_planning"])
        
        print("\n📊 营销计划结果:")
        print(result["campaign_plan"])
        
        print("\n📈 趋势分析结果:")
        print(result["trend_analysis"])
        
        print("\n🗺️ 内容策略地图:")
        print(result["content_strategy"])
        
        print("\n⏭️ 下一步:")
        for step in result["next_steps"]:
            print(f"  - {step}")
    else:
        print(f"\n❌ 工作流执行失败: {result.get('error', '未知错误')}")
        print(f"失败状态: {result.get('status')}")

if __name__ == "__main__":
    # 在Windows上运行需要这个
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    # 运行测试
    asyncio.run(main()) 