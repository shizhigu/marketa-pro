"""
Marketa-Pro E-commerce Content Agent Platform - Workflow Module

This module contains workflow agents that orchestrate the execution of other agents
in predefined patterns like sequential, parallel, or loop.
"""

# Import workflow root_agent
from .marketa_workflow import root_agent

__all__ = ['root_agent']

"""
Marketa-Pro Workflow Package
"""

# Import workflow module to expose root_agent
from . import marketa_workflow 