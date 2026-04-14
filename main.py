"""
Marketa-Pro E-commerce Content Agent Platform - Main Entry

How to start:
1. Install dependencies: pip install google-adk
2. Run: python main.py
"""

import asyncio
import logging
from agents import OrchestratorAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main function, starts the Orchestrator Agent and processes example requests"""
    print("🛍️ Welcome to Marketa-Pro E-commerce Content Agent Platform")
    print("Initializing Orchestrator Agent...")
    
    # Initialize the orchestrator agent
    orchestrator = OrchestratorAgent()
    print("Orchestrator Agent initialization complete!")
    
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
    
    print("\nProcessing example request...")
    print("This may take a moment as multiple agents collaborate on your content...")
    
    result = await orchestrator.process_user_input(user_input)
    
    print("\n✅ Processing complete!")
    print(f"Task ID: {result.get('task_id')}")
    print(f"Status: {result.get('status')}")
    
    if result.get('status') == 'campaign_planning_completed':
        print("\n📋 Initial Planning:")
        print(result.get('initial_planning', 'Not available'))
        
        print("\n📝 Campaign Plan:")
        print(result.get('campaign_plan', 'Not available'))
        
        print("\n⏭️ Next Steps:")
        for step in result.get('next_steps', []):
            print(f" - {step}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
        
    print("\nThank you for using Marketa-Pro!")

if __name__ == "__main__":
    asyncio.run(main()) 