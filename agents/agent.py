# """
# Marketa-Pro E-commerce Content Workflow

# This module defines the sequential workflow from Orchestrator to Campaign Planner for ADK web.
# """

# from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm

# from agents.orchestrator_agent import OrchestratorAgent
# from agents.campaign_planner_agent import CampaignPlannerAgent
# from utils.config import get_model_config, DEFAULT_MODEL

# # Create orchestrator instance for initialization
# orchestrator = OrchestratorAgent()

# # Define the root agent that will be exposed to ADK web
# root_agent = Agent(
#     name="marketa_pro_agent",
#     model=orchestrator.agent.model,  # Reuse the model configuration from orchestrator
#     description="Marketa-Pro e-commerce marketing content generation platform",
#     instruction="""
#     You are the main agent for Marketa-Pro, an e-commerce content generation platform.
#     You will help users create marketing campaigns, content strategies, and execution plans
#     for various e-commerce platforms.
    
#     When a user provides their goal, product information, platform, and brand details,
#     coordinate with the appropriate sub-agents to deliver a comprehensive marketing solution.
#     """,
#     tools=[],  # No direct tools needed at root level
#     sub_agents=[
#         orchestrator.agent  # Use orchestrator agent as sub-agent
#     ]
# ) 


"""
Marketa-Pro Workflow Definition
"""

from google.adk.agents import SequentialAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.campaign_planner_agent import CampaignPlannerAgent

# Create instances of our agents
orchestrator = OrchestratorAgent()
campaign_planner = CampaignPlannerAgent()

# Create the Sequential Workflow using the agent objects
# This will be discovered by the ADK web interface
root_agent = SequentialAgent(
    name="marketa_workflow",
    description="Marketa-Pro workflow for e-commerce content generation",
    sub_agents=[orchestrator.agent, campaign_planner.agent]
) 