#!/bin/bash
# Start ADK web UI

# Print welcome message
echo "🛍️ Starting Marketa-Pro ADK Web UI"
echo "========================="

# Check environment variables configuration
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please copy .env.example to .env and fill in your OpenRouter API key"
fi

# Use ADK web command to start web interface
echo "🚀 Starting web interface..."
adk web --port 8000

# Note: After startup, visit http://localhost:8000 in your browser
# Available agents:
# - marketa_pro_agent: Main root agent
# - marketa_workflow: Sequential workflow from orchestrator to campaign planner 