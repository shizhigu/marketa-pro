"""
Configuration utilities for Marketa-Pro
"""

import os
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Model configuration
DEFAULT_MODEL = "openrouter/google/gemini-pro-1.5"  # Can be replaced with other models supported by OpenRouter

# Check if API key is set
if not OPENROUTER_API_KEY:
    logger.warning("OpenRouter API key is not set. Please set OPENROUTER_API_KEY in the .env file.")

def get_model_config(model_name=DEFAULT_MODEL):
    """
    Get LiteLlm model configuration parameters
    
    Args:
        model_name: Model name to use
        
    Returns:
        dict: Dictionary containing model configuration parameters
    """
    return {
        "model": model_name,
        "api_key": OPENROUTER_API_KEY,
        "base_url": OPENROUTER_BASE_URL
    } 