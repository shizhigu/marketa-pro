from google.adk import Agent, Runner
from google.adk.tools import ToolContext
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from typing import Dict, List, Any, Optional
import logging
import asyncio

# Import configuration
from utils.config import get_model_config, DEFAULT_MODEL

# Import sub-agents
from agents.campaign_planner_agent import CampaignPlannerAgent
from agents.content_strategy_map_agent import ContentStrategyMapAgent
from agents.trend_radar_agent import TrendRadarAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define model constants
MODEL_GEMINI_1_5_PRO = DEFAULT_MODEL
MODEL_GEMINI_1_5_FLASH = "google/gemini-1.5-flash"

# OpenRouter configurations
# OpenRouter configuration is managed centrally via utils/config.py

class OrchestratorAgent:
    """
    Core coordinator agent responsible for orchestrating all downstream agents,
    managing task states and execution chains
    """
    
    def __init__(self, app_name: str = "marketa-pro"):
        """
        Initialize the Orchestrator Agent
        
        Args:
            app_name: Application name
        """
        self.app_name = app_name
        self.agent = self._create_agent()
        self.runner = self._create_runner()
        self.task_states = {}  # For storing task states
        
        # Initialize sub-agents
        self.campaign_planner_agent = CampaignPlannerAgent(app_name=self.app_name)
        self.content_strategy_map_agent = ContentStrategyMapAgent(app_name=self.app_name)
        self.trend_radar_agent = TrendRadarAgent(app_name=self.app_name)
        
    def _create_agent(self) -> Agent:
        """
        Create the core Agent instance
        
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
            name="orchestrator_agent",
            model=model,  # 使用LiteLlm包装的模型
            description="Core orchestrator for e-commerce content platform, responsible for scheduling and managing all sub-agent tasks",
            instruction="""
            You are the core orchestrator of the Marketa-Pro platform, responsible for receiving user input, 
            arranging and coordinating the work of other agents.
            
            Your primary responsibilities include:
            1. Analyzing user goals and requirements to determine the downstream agent workflow needed
            2. Scheduling appropriate agent combinations based on task type and platform requirements
            3. Managing the entire task execution chain, including status tracking and failure retries
            4. Integrating final results and returning them to the user
            
            Workflow process:
            1. Receive user input (goals, product information, platform, brand tone, etc.)
            2. Determine task type and plan execution path
            3. Call Trend Radar Agent and Campaign Planner Agent to obtain trends and content strategy
            4. Based on the strategy guidance, schedule Content Generation Layer agents
            5. Coordinate Execution Layer agents for publishing or generating briefs
            6. Collect feedback and trigger Analysis & Optimization Layer agents
            7. Store learning results in the memory module
            
            You should be capable of handling various complex e-commerce content creation scenarios, including but not limited to: 
            new product seeding, holiday promotions, cross-border store initial content, etc.
            
            DO NOT ask user to provide any information, just use the user input directly.
            """,
            tools=[],  # No tools in initial stage, can be added later
            sub_agents=[],  # No sub-agents in initial stage, can be added as needed
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
    
    async def process_user_input(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and coordinate the entire task workflow
        
        Args:
            user_input: Dictionary containing user goals, product information, etc.
        
        Returns:
            Dict: Processing results
        """
        # Create task ID and initial state
        task_id = f"task_{len(self.task_states) + 1}"
        self.task_states[task_id] = {
            "status": "initiated",
            "user_input": user_input,
            "results": {},
            "current_step": "planning"
        }
        
        try:
            # Call Orchestrator Agent for initial planning
            logger.info(f"Starting orchestration for task {task_id}")
            
            # Call Agent for initial planning processing
            initial_result = await self.runner.run(
                query=self._format_user_input(user_input),
                session_id=task_id,
            )
            
            # Update task status
            self.task_states[task_id]["status"] = "planning_initial_completed"
            self.task_states[task_id]["results"]["initial_planning"] = initial_result
            
            # Call Campaign Planner Agent
            logger.info(f"Calling Campaign Planner Agent for task {task_id}")
            campaign_plan_result = await self.campaign_planner_agent.create_campaign_plan(user_input)
            
            if campaign_plan_result["status"] == "success":
                # Update task status with campaign plan results
                self.task_states[task_id]["status"] = "campaign_planning_completed"
                self.task_states[task_id]["results"]["campaign_plan"] = campaign_plan_result["campaign_plan"]
                
                # Call Trend Radar Agent to get real trend data
                logger.info(f"Calling Trend Radar Agent for task {task_id}")
                platform = user_input.get("platform", "xiaohongshu")
                product_category = user_input.get("product_category", "general")
                product_tags = user_input.get("product_tags", "").split(",") if user_input.get("product_tags") else []
                
                trend_result = await self.trend_radar_agent.analyze_platform_trends(
                    platform=platform,
                    product_category=product_category,
                    product_tags=product_tags
                )
                
                # Update task status with trend analysis results
                if trend_result["status"] == "success":
                    self.task_states[task_id]["status"] = "trend_analysis_completed"
                    self.task_states[task_id]["results"]["trend_analysis"] = trend_result["trend_analysis"]
                else:
                    logger.warning(f"Trend analysis failed: {trend_result.get('error', 'Unknown error')}")
                    # Continue with process even if trend analysis fails
                
                # Call Content Strategy Map Agent
                logger.info(f"Calling Content Strategy Map Agent for task {task_id}")
                content_strategy_result = await self.content_strategy_map_agent.create_content_strategy_map(
                    {"campaign_plan": campaign_plan_result["campaign_plan"]},
                    {"trend_analysis": trend_result.get("trend_analysis")} if trend_result.get("status") == "success" else None
                )
                
                if content_strategy_result["status"] == "success":
                    # Update task status with content strategy results
                    self.task_states[task_id]["status"] = "content_strategy_completed"
                    self.task_states[task_id]["results"]["content_strategy"] = content_strategy_result["content_strategy_map"]
                    
                    # In future implementations, we would continue with other agents like:
                    # - Copywriting Agent
                    # - Image Agent
                    # - etc.
                    
                    return {
                        "task_id": task_id,
                        "status": "content_strategy_completed",
                        "initial_planning": initial_result,
                        "campaign_plan": campaign_plan_result["campaign_plan"],
                        "trend_analysis": trend_result.get("trend_analysis") if trend_result.get("status") == "success" else "Failed to obtain trend analysis",
                        "content_strategy": content_strategy_result["content_strategy_map"],
                        "next_steps": ["content_generation", "execution"]
                    }
                else:
                    # Update task status with failure
                    self.task_states[task_id]["status"] = "content_strategy_failed"
                    self.task_states[task_id]["error"] = content_strategy_result.get("error", "Unknown error")
                    
                    return {
                        "task_id": task_id,
                        "status": "content_strategy_failed",
                        "error": content_strategy_result.get("error", "Unknown error")
                    }
                    
            else:
                # Update task status with failure
                self.task_states[task_id]["status"] = "campaign_planning_failed"
                self.task_states[task_id]["error"] = campaign_plan_result.get("error", "Unknown error")
                
                return {
                    "task_id": task_id,
                    "status": "campaign_planning_failed",
                    "error": campaign_plan_result.get("error", "Unknown error")
                }
            
        except Exception as e:
            logger.error(f"Error in process_user_input: {str(e)}")
            self.task_states[task_id]["status"] = "failed"
            self.task_states[task_id]["error"] = str(e)
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }
    
    def _format_user_input(self, user_input: Dict[str, Any]) -> str:
        """
        Format user input into a query string that the Agent can process
        
        Args:
            user_input: User input dictionary
        
        Returns:
            str: Formatted query string
        """
        formatted_input = f"""
        Goal: {user_input.get('goal', 'Not specified')}
        Product Information: 
          - Title: {user_input.get('product_title', 'Not specified')}
          - Selling Points: {user_input.get('product_selling_points', 'Not specified')}
          - Tags: {user_input.get('product_tags', 'Not specified')}
        Platform: {user_input.get('platform', 'Not specified')}
        Brand Tone: {user_input.get('brand_tone', 'Not specified')}
        Target Audience: {user_input.get('audience', 'Not specified')}
        """
        return formatted_input
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a specified task
        
        Args:
            task_id: Task ID
        
        Returns:
            Dict: Task status information
        """
        if task_id not in self.task_states:
            return {"status": "not_found", "error": "Task ID does not exist"}
        
        return self.task_states[task_id]

# Usage example
async def example_usage():
    orchestrator = OrchestratorAgent()
    
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
    
    result = await orchestrator.process_user_input(user_input)
    print(f"Processing result: {result}")
    
    # Get task status
    if result.get("task_id"):
        status = orchestrator.get_task_status(result["task_id"])
        print(f"Task status: {status}") 