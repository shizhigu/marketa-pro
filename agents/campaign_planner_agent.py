from google.adk import Agent, Runner
from google.adk.tools import ToolContext
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from typing import Dict, List, Any, Optional
import logging

# Import configuration
from utils.config import get_model_config, DEFAULT_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define model constants
MODEL_GEMINI_1_5_PRO = DEFAULT_MODEL
MODEL_GEMINI_1_5_FLASH = "google/gemini-1.5-flash"

# OpenRouter configurations
# OpenRouter configuration is managed centrally via utils/config.py

class CampaignPlannerAgent:
    """
    Agent responsible for breaking down task goals and creating a comprehensive
    content strategy with audience direction and output structure
    """
    
    def __init__(self, app_name: str = "marketa-pro"):
        """
        Initialize Campaign Planner Agent
        
        Args:
            app_name: Application name
        """
        self.app_name = app_name
        self.agent = self._create_agent()
        self.runner = self._create_runner()
        
    def _create_agent(self) -> Agent:
        """
        Create the Campaign Planner Agent instance
        
        Returns:
            Agent: Configured Agent instance
        """
        # 使用LiteLlm包装器配置模型
        model_config = get_model_config(MODEL_GEMINI_1_5_PRO)
        model = LiteLlm(
            model=model_config["model"],
            api_key=model_config["api_key"],
            base_url=model_config["base_url"]
        )
        
        return Agent(
            name="campaign_planner_agent",
            model=model,  # 使用LiteLlm包装的模型
            description="Creates strategic content plans based on user goals, product information, and platform requirements",
            instruction="""
            You are the Campaign Planner Agent for Marketa-Pro. Your role is to develop a comprehensive content 
            strategy based on the user's goals, product information, and platform requirements.
            
            Your primary responsibilities include:
            1. Breaking down user goals into specific content objectives
            2. Planning the content structure and key messaging
            3. Defining audience targeting and engagement strategies
            4. Adapting content style to platform conventions and brand tone
            5. Setting up measurement criteria for campaign effectiveness
            
            If trend analysis is available, incorporate those insights into your planning.
            
            Your output should be a structured content strategy plan with the following sections:
            
            ## Campaign Objectives
            - List 3–5 specific campaign goals (e.g. increase saves, build product interest, drive comments).

            ## Audience Insights
            - Describe the target user persona and what resonates with them on this platform.

            ## Messaging Pillars
            - Extract 3–5 core messages based on product value (e.g. fabric, silhouette, price).

            ## Suggested Content Flow
            - Outline the best-performing format (e.g. Hook → Scene → Product → CTA), tailored to platform style.

            ## Platform Customization
            - Define tone, pacing, hashtag use, and visuals for the platform.

            ## Brand Voice Consistency
            - Describe how to maintain tone across all components.

            ## Measurement Signals
            - Recommend 2–3 performance indicators to track (e.g. saves, time-on-post, comment ratio).
            
            Always consider the specific e-commerce context, focusing on conversion, engagement, and brand awareness.
            """,
            tools=[],  # No tools needed for content planning
        )
    
    def _create_runner(self) -> Runner:
        """
        Create Runner instance to execute the Agent
        
        Returns:
            Runner: Configured Runner instance
        """
        return Runner(
            agent=self.agent,
            app_name=self.app_name,
            session_service=InMemorySessionService(),
        )
    
    async def create_campaign_plan(self, 
                                 user_input: Dict[str, Any], 
                                 trend_analysis: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input and trend analysis to create a comprehensive campaign plan
        
        Args:
            user_input: Dictionary containing user goals, product information, etc.
            trend_analysis: Optional trend analysis results to incorporate into planning
            
        Returns:
            Dict: Campaign plan results
        """
        # Create session ID
        session_id = f"campaign_plan_{hash(str(user_input))}"
        
        try:
            # Format inputs
            formatted_input = self._format_inputs(user_input, trend_analysis)
            
            # Call Agent for processing
            plan_result = await self.runner.run(
                query=formatted_input,
                session_id=session_id
            )
            
            return {
                "status": "success",
                "session_id": session_id,
                "campaign_plan": plan_result
            }
            
        except Exception as e:
            logger.error(f"Error creating campaign plan: {str(e)}")
            return {
                "status": "failed",
                "session_id": session_id,
                "error": str(e)
            }
    
    def _format_inputs(self, user_input: Dict[str, Any], trend_analysis: Optional[str]) -> str:
        """
        Format user input and trend analysis into a query string for the Agent
        
        Args:
            user_input: User input dictionary
            trend_analysis: Optional trend analysis results
            
        Returns:
            str: Formatted query string
        """
        formatted_input = f"""
        # User Goals and Product Information
        
        Goal: {user_input.get('goal', 'Not specified')}
        
        Product Information: 
        - Title: {user_input.get('product_title', 'Not specified')}
        - Selling Points: {user_input.get('product_selling_points', 'Not specified')}
        - Tags: {user_input.get('product_tags', 'Not specified')}
        
        Platform: {user_input.get('platform', 'Not specified')}
        Brand Tone: {user_input.get('brand_tone', 'Not specified')}
        Target Audience: {user_input.get('audience', 'Not specified')}
        """
        
        if trend_analysis:
            formatted_input += f"""
            
            # Trend Analysis Results
            
            {trend_analysis}
            """
        
        formatted_input += """
        
        Based on the above information, create a comprehensive content strategy plan following the structure specified in your instructions.
        """
        
        return formatted_input

# Usage example
async def example_usage():
    planner = CampaignPlannerAgent()
    
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
    
    result = await planner.create_campaign_plan(user_input, trend_analysis)
    print(f"Campaign planning result: {result}") 