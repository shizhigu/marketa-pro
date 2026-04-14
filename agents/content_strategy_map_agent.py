from google.adk import Agent, Runner
from google.adk.tools import ToolContext
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

class ContentStrategyMapAgent:
    """
    Agent responsible for aggregating outputs from Campaign Planner and Trend Radar agents
    to create a comprehensive content strategy map for execution
    """
    
    def __init__(self, app_name: str = "marketa-pro"):
        """
        Initialize Content Strategy Map Agent
        
        Args:
            app_name: Application name
        """
        self.app_name = app_name
        self.agent = self._create_agent()
        self.runner = self._create_runner()
        
    def _create_agent(self) -> Agent:
        """
        Create the Content Strategy Map Agent instance
        
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
            name="content_strategy_map_agent",
            model=model,  # 使用LiteLlm包装的模型
            description="Aggregates trends and campaign planning into a comprehensive content strategy map",
            instruction="""
            You are the Content Strategy Map Agent for Marketa-Pro. Your role is to synthesize the insights from 
            the Campaign Planner and Trend Radar agents to create a cohesive, actionable content strategy map.
            
            Your primary responsibilities include:
            1. Analyzing campaign objectives and strategies from the Campaign Planner
            2. Incorporating trend insights and platform-specific data from the Trend Radar
            3. Identifying strategic alignment and potential conflicts between trends and campaign goals
            4. Creating a unified content strategy map with clear execution guidelines
            5. Providing content calendar recommendations and key performance indicators

            Your output should be a structured content strategy map with the following sections:
            
            ## Executive Summary
            [A concise overview of the unified strategy and expected outcomes]
            
            ## Strategic Alignment
            [How trending topics and campaign objectives align, with recommended focus areas]
            
            ## Content Pillars
            [3-5 core content themes that combine trend opportunities with campaign goals]
            
            ## Platform-Specific Execution Plan
            [Tailored approach for adapting content to different platforms based on trends and objectives]
            
            ## Content Calendar
            [Suggested timing and sequence for content deployment]
            
            ## Performance Metrics
            [Key indicators for measuring success, based on platform trends and campaign goals]
            
            ## Resource Allocation Recommendations
            [Suggestions for where to focus time and resources based on trend opportunities]
            
            Ensure that your strategy map is actionable, platform-relevant, and directly supports the business goals 
            while leveraging current trends for maximum impact.
            """,
            tools=[],  # No tools needed for content strategy mapping
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
    
    async def create_content_strategy_map(self, 
                                 campaign_plan: Dict[str, Any], 
                                 trend_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process campaign plan and trend analysis to create a comprehensive content strategy map
        
        Args:
            campaign_plan: Dictionary containing campaign planning results from Campaign Planner Agent
            trend_analysis: Optional trend analysis results from Trend Radar Agent
            
        Returns:
            Dict: Content strategy map results
        """
        # Create session ID
        session_id = f"content_strategy_{hash(str(campaign_plan))}"
        
        try:
            # Format inputs
            formatted_input = self._format_inputs(campaign_plan, trend_analysis)
            
            # Call Agent for processing
            map_result = await self.runner.run(
                query=formatted_input,
                session_id=session_id
            )
            
            return {
                "status": "success",
                "session_id": session_id,
                "content_strategy_map": map_result
            }
            
        except Exception as e:
            logger.error(f"Error creating content strategy map: {str(e)}")
            return {
                "status": "failed",
                "session_id": session_id,
                "error": str(e)
            }
    
    def _format_inputs(self, campaign_plan: Dict[str, Any], trend_analysis: Optional[Dict[str, Any]]) -> str:
        """
        Format campaign plan and trend analysis into a query string for the Agent
        
        Args:
            campaign_plan: Campaign planning results from Campaign Planner Agent
            trend_analysis: Optional trend analysis results from Trend Radar Agent
            
        Returns:
            str: Formatted query string
        """
        formatted_input = f"""
        # Campaign Planning Results
        
        {campaign_plan.get('campaign_plan', 'No campaign plan provided')}
        """
        
        if trend_analysis:
            formatted_input += f"""
            
            # Trend Analysis Results
            
            {trend_analysis.get('trend_analysis', 'No specific trend details provided')}
            """
        
        formatted_input += """
        
        Based on the above campaign plan and trend analysis, create a comprehensive content strategy map 
        following the structure specified in your instructions.
        """
        
        return formatted_input

# Usage example
async def example_usage():
    strategy_mapper = ContentStrategyMapAgent()
    
    # Example campaign plan (would normally come from Campaign Planner Agent)
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
        """
    }
    
    # Example trend analysis (would normally come from Trend Radar Agent)
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
    
    result = await strategy_mapper.create_content_strategy_map(campaign_plan, trend_analysis)
    print(f"Content strategy mapping result: {result}") 