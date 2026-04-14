"""
Marketa-Pro Workflow Definition
"""

from google.adk.agents import SequentialAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.campaign_planner_agent import CampaignPlannerAgent
from agents.content_strategy_map_agent import ContentStrategyMapAgent
from agents.trend_radar_agent import TrendRadarAgent

# Create instances of our agents
orchestrator = OrchestratorAgent()
campaign_planner = CampaignPlannerAgent()
trend_radar = TrendRadarAgent()
content_strategy_map = ContentStrategyMapAgent()

# Create the Sequential Workflow using the agent objects
# This will be discovered by the ADK web interface
root_agent = SequentialAgent(
    name="marketa_workflow",
    description="Marketa-Pro workflow for e-commerce content generation",
    sub_agents=[orchestrator.agent, trend_radar.agent, campaign_planner.agent, content_strategy_map.agent]
) 