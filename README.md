# Marketa-Pro

> Multi-agent AI platform that automates e-commerce content strategy for Chinese brands and KOL teams.

## What is this?

Marketa-Pro transforms a product brief into a complete, platform-optimized marketing content package for Xiaohongshu, Douyin/TikTok, and Taobao. It orchestrates specialized AI agents -- trend research, campaign planning, and content strategy synthesis -- to replace the sequential handoff between trend researcher, content strategist, copywriter, and campaign manager, executing in minutes rather than days.

## Why?

I noticed that my sister's marketing agency spent the majority of its time on repetitive content operations: researching platform trends, decomposing campaign goals into briefs, and adapting messaging for different KOL personas across platforms. Small and mid-size Chinese brands -- the majority of sellers on these platforms -- cannot afford the 5-10 person content teams needed to keep pace with weekly trend shifts.

## How it works

Marketa-Pro uses a layered multi-agent architecture built on Google's Agent Development Kit (ADK):

1. **Orchestrator Agent**: Receives user input (product title, selling points, platform, brand tone, audience, campaign goal) and manages the full execution chain with task state tracking and graceful degradation on individual agent failures.
2. **Trend Radar Agent**: Analyzes platform-specific trends using a FunctionTool pattern -- trending topics, hashtags, content format performance, and optimal posting windows for Xiaohongshu, TikTok, or generic platforms.
3. **Campaign Planner Agent**: Decomposes goals into structured strategy: objectives, audience personas, messaging pillars, content flow, platform customization, brand voice rules, and measurement signals.
4. **Content Strategy Map Agent**: Synthesizes trend analysis and campaign plan into a unified execution roadmap with content pillars, calendar, performance metrics, and resource allocation.

All agents use LiteLLM through OpenRouter for model-agnostic routing (Gemini Pro 1.5 default, swappable per-agent). The system runs in two modes: programmatic via `main.py` or interactive through ADK's built-in web UI on port 8000.

## Key Technical Highlights

- **Graceful Pipeline Degradation**: Individual agent failures are caught and logged but never halt the pipeline -- if trend analysis fails, the strategy map agent operates on campaign plan data alone.
- **Model-Agnostic Agent Design**: LiteLLM + OpenRouter abstraction allows per-agent model selection (cheaper Flash for formatting, capable Pro for strategy), swappable with a single config change.
- **Structured Prompting as Agent Contract**: Each agent's instruction prompt defines explicit markdown-section output formats, creating a soft schema that downstream agents reliably parse without brittle JSON extraction.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Agent Framework | Google ADK (Agent Development Kit) |
| Model Routing | LiteLLM + OpenRouter |
| Default LLM | Gemini Pro 1.5 |
| Async | asyncio |
| Config | python-dotenv |
| Database (planned) | PostgreSQL (Supabase) |
| Payments (planned) | Stripe |

## Quick Start

```bash
git clone https://github.com/gushizhi/Marketa-Pro.git
cd Marketa-Pro
pip install google-adk python-dotenv litellm
cp .env.example .env            # Add OPENROUTER_API_KEY
python main.py                  # Run full pipeline
bash run_web.sh                 # Or launch ADK web UI on port 8000
```

## License

MIT
