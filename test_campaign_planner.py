"""
Test script for Campaign Planner Agent

Run this script to test the Campaign Planner Agent functionality independently
"""

import asyncio
import logging
from agents import CampaignPlannerAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Test the Campaign Planner Agent functionality"""
    print("📋 Testing Campaign Planner Agent")
    
    # Initialize the Campaign Planner Agent
    planner = CampaignPlannerAgent()
    print("Campaign Planner Agent initialized")
    
    # Example user input
    user_input = {
        "goal": "New product seeding",
        "product_title": "Smart Thermos Cup",
        "product_selling_points": "24-hour heat retention, APP temperature display, water drinking reminder function",
        "product_tags": "Technology,Health,Lifestyle",
        "platform": "Xiaohongshu",
        "brand_tone": "Minimalist technology",
        "audience": "25-35 year-old urban young people"
    }
    
    # Example trend analysis (would normally come from Trend Radar Agent)
    trend_analysis = """
    Current Platform Trends:
    - Morning routine videos featuring tech products
    - Minimalist aesthetic product showcases
    - Health-focused lifestyle content
    
    Relevant Hashtags:
    - #SmartLiving
    - #MorningRoutine
    - #TechForHealth
    - #HydrationCheck
    - #MinimalistTech
    
    Content Format Recommendations:
    - Short carousel posts showing product features
    - Day-in-the-life format featuring the product
    - Comparison content with traditional products
    """
    
    print("\nGenerating campaign plan...")
    print("This may take a moment...")
    
    # Test without trend analysis first
    print("\n🧪 TEST 1: Campaign planning without trend analysis")
    result1 = await planner.create_campaign_plan(user_input)
    
    if result1["status"] == "success":
        print("\n✅ Campaign plan without trend analysis generated successfully!")
        print("\n📝 CAMPAIGN PLAN (without trend analysis):")
        print(result1["campaign_plan"])
    else:
        print(f"\n❌ Campaign planning failed: {result1.get('error')}")
    
    # Test with trend analysis
    print("\n🧪 TEST 2: Campaign planning with trend analysis")
    result2 = await planner.create_campaign_plan(user_input, trend_analysis)
    
    if result2["status"] == "success":
        print("\n✅ Campaign plan with trend analysis generated successfully!")
        print("\n📝 CAMPAIGN PLAN (with trend analysis):")
        print(result2["campaign_plan"])
    else:
        print(f"\n❌ Campaign planning failed: {result2.get('error')}")
    
    # Compare results
    print("\n🔍 COMPARISON:")
    print("You can now compare the two campaign plans to see how trend analysis influences the strategy.")

if __name__ == "__main__":
    asyncio.run(main()) 