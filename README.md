<div align="center">

# Marketa-Pro

**A multi-agent prototype that turns a product brief into a marketing content strategy for Chinese e-commerce platforms.**

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Framework](https://img.shields.io/badge/framework-Google%20ADK-4285F4)
![Status](https://img.shields.io/badge/status-prototype-orange)

</div>

---

## What it is

Chinese e-commerce brands sell through content: Xiaohongshu posts, Douyin/TikTok videos, Taobao product stories, and KOL collaborations. Producing that content means researching platform trends, turning a campaign goal into briefs, and adapting the message per platform and audience. Small brands and the agencies that serve them repeat this cycle for every product launch.

Marketa-Pro is an experiment in automating that pipeline with role-specialized AI agents. You give it a product brief (title, selling points, platform, brand tone, audience, goal) and it produces a trend read, a campaign plan, and a combined content strategy map. It was written against the workflow of a real marketing agency (the author's sister's), and it is an early prototype: the planning layer runs, but most of the larger platform is still a design on paper.

## Agent design

The system is built on Google's Agent Development Kit (ADK). Four agents each wrap a single ADK `Agent` (LLM plus role instruction), an async `Runner`, and an in-memory session:

- **Orchestrator** takes the brief and runs the pipeline, tracking each task through status phases (`initiated`, `campaign_planning_completed`, `trend_analysis_completed`, `content_strategy_completed`) in a `task_states` dictionary.
- **Trend Radar** analyzes platform trends. It registers a `FunctionTool` that the LLM calls to fetch trend data (topics, hashtags, format performance, posting windows) for Xiaohongshu, TikTok, or a generic default.
- **Campaign Planner** turns the goal and product into a seven-section strategy (objectives, audience, messaging pillars, content flow, platform customization, brand voice, measurement).
- **Content Strategy Map** merges the plan and the trends into one execution roadmap (pillars, calendar, metrics, resource allocation).

The design idea from the project docs is to mirror how a content team hands work down a line (trend researcher to strategist to writer), with each agent's markdown-section output acting as a loose contract the next agent reads. The docs also sketch a cross-border ("going global") direction with a localization knowledge base and RAG, plus a "text micro-tuner" refiner agent for guided edits. None of that is built yet.

Two honest caveats about the current code:

- The orchestrator sequences the agents in Python in a fixed order. It does not use an LLM to decide the route, and its own agent output is computed but not used for any decision. So this is a fixed pipeline of role-specialized LLM calls, not an autonomous loop.
- The Trend Radar tool returns hardcoded simulated data. It is structured to be swapped for a real crawler or API later, but today it does not fetch anything live.

Models are routed through LiteLLM to OpenRouter, defaulting to Gemini Pro 1.5. Changing the model is a one-line edit in `utils/config.py`.

## Quick start

Requires Python 3.11+ and an OpenRouter API key.

```bash
git clone https://github.com/shizhigu/marketa-pro.git
cd marketa-pro
pip install -r requirements.txt

# create a .env file with your key
echo "OPENROUTER_API_KEY=sk-or-..." > .env

python main.py        # run the planning pipeline on a built-in example brief
bash run_web.sh       # or open the ADK web UI on http://localhost:8000
```

`main.py` runs the orchestrator against a sample "smart thermos cup" brief. `run_web.sh` launches ADK's web UI, which discovers the `SequentialAgent` in `agents/workflow/marketa_workflow.py`.

## Status

Built and runnable:

- Orchestrator, Trend Radar, Campaign Planner, and Content Strategy Map agents
- Sequential pipeline with task-state tracking and degradation when trend analysis fails
- LiteLLM/OpenRouter routing
- ADK web workflow entry point
- Standalone test scripts per agent (`test_*.py`)

Designed but not implemented:

- Real trend crawlers behind the Trend Radar tool
- Content generation, execution, and monitoring layers (copywriter, image, KOL brief, publishing, feedback)
- Localization knowledge base and RAG for cross-border campaigns
- A refiner/micro-tuner agent
- Persistence: `db.sql` defines a Postgres schema (users, projects, tasks, outputs, feedback, subscriptions) but no code reads or writes it
- Any web API, frontend, or billing

`PROJECT_BRIEF.md` and `architecture.md` hold the fuller product thinking.

## License

No license file is included, so no usage rights are granted by default. Add a LICENSE before reuse.
