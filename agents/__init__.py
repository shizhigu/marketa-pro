"""
Marketa-Pro E-commerce Content Agent Platform - Agent Module

This module contains various AI agent components used in the system, organized by layers:
- Orchestrator Layer: Core coordinator
- Planning Layer: Trend Radar, Campaign Planner
- Content Generation Layer: Copywriting, Image, CTA, Video Script
- Execution Layer: Multichannel Publishing, KOL Brief Generator
- Monitoring Layer: Data Feedback Collector, Engagement Tracker
- Analysis & Optimization Layer: Critic, Rhythm Adjuster, A/B Testing
- Learning Feedback Layer: Learning Memory Module
"""

from agents.orchestrator_agent import OrchestratorAgent
from agents.campaign_planner_agent import CampaignPlannerAgent
from agents.content_strategy_map_agent import ContentStrategyMapAgent
from agents.trend_radar_agent import TrendRadarAgent

__all__ = ['OrchestratorAgent', 'CampaignPlannerAgent', 'ContentStrategyMapAgent', 'TrendRadarAgent']

# Import agent module to expose root_agent
from . import agent 