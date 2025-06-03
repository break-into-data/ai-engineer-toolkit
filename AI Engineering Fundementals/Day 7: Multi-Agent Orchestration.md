# Day 7: Multi-Agent Orchestration

### Multi-Agent Orchestration with the OpenAI Agents SDK

Previously (Day 2) we compared different workflow types—**prompt chaining**, **parallelization**, **orchestrator–worker**, and **evaluator–optimizer**. Today’s focus is the **orchestrator–worker** pattern, which coordinates specialized agents to work in concert on complex tasks. In the AI Engineering bootcamp, we will deep dive into complex multi-agent architecture and systems. 

---

### Why a multi-agent research bot?

A single LLM can answer questions, but three specialized agents working together can:

- **Plan** a smart search strategy
- **Parallel-fetch** fresh information from the web
- **Synthesize** a long-form, well-structured report – all while streaming traces you can debug in real time.

The official `examples/research_bot` directory in the Agents SDK implements exactly this four-step flow – user → planner → searchers → writer → report. [GitHub](https://github.com/openai/openai-agents-python/blob/main/examples/research_bot/README.md)

### Project setup

First, create and activate a virtual environment, then install dependencies:

```bash
python -m venv env && source env/bin/activate
pip install openai-agents rich  # rich is only for console output
export OPENAI_API_KEY="<YOUR_API_KEY>"
```

Your project folder should mirror the SDK example:

```
research_bot/
├── agents/
│   ├── planner_agent.py
│   ├── search_agent.py
│   └── writer_agent.py
├── manager.py        # orchestration glue
└── main.py           # CLI entry point
```

### Defining the three agents

### Planner Agent – turns a raw question into search tasks

The planner’s only job is to decompose the user’s query into a concise set of web-search prompts that will later run in parallel.

```python
# research_bot/agents/planner_agent.py
from pydantic import BaseModel
from agents import Agent

class WebSearchItem(BaseModel):
    reason: str            # why we’re running this search
    query: str             # the exact search term

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]

planner_agent = Agent(
    name="PlannerAgent",
    instructions=(
        "You are a research strategist. Given a question, propose 5-20 web "
        "searches that, together, will answer it comprehensively. "
        "Return them as JSON in the schema provided."
    ),
    model="gpt-4o",
    output_type=WebSearchPlan,
)
```

---

### Search Agent – executes one web search and summarizes the page results

Each search agent instance receives **one** `query` from the plan, calls an external WebSearchTool, and condenses what it finds into a < 300-word bullet list.

```python
# research_bot/agents/search_agent.py
from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

search_agent = Agent(
    name="SearchAgent",
    instructions=(
        "You are an internet researcher. Use the WebSearch tool to gather the "
        "most relevant information for the given query. Summarize your findings "
        "in clear, markdown bullets (≤300 words)."
    ),
    tools=[WebSearchTool()],
    # force the model to choose the tool; no stray text-only answers
    model_settings=ModelSettings(tool_choice="required"),
)
```

---

### Writer Agent – stitches all summaries into a polished report

After the parallel searches finish, their bullet summaries are concatenated and handed to the writer, which creates a multi-page markdown report plus follow-up questions for the reader.

```python
# research_bot/agents/writer_agent.py
from pydantic import BaseModel
from agents import Agent

class ReportData(BaseModel):
    short_summary: str
    markdown_report: str
    follow_up_questions: list[str]

writer_agent = Agent(
    name="WriterAgent",
    instructions=(
        "You are a senior analyst. Combine the provided research summaries "
        "into a coherent, well-structured report (5-10 pages of markdown). "
        "Begin with a one-paragraph executive summary, then the full report, "
        "and end with 3-5 thoughtful follow-up questions."
    ),
    model="o3-mini",
    output_type=ReportData,
)
```

With these three purpose-built agents in place, the orchestration layer can chain them into a fast, traceable research pipeline.

### Orchestrating the workflow

`ResearchManager` ties everything together:

```python
# research_bot/manager.py
import asyncio
from agents import Runner
from tracing import trace, gen_trace_id

class ResearchManager:
    async def run(self, query: str) -> None:
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            plan    = await self._plan_searches(query)
            results = await self._perform_searches(plan)
            report  = await self._write_report(query, results)
            print(report.markdown_report)

    async def _plan_searches(self, query: str):
        result = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output.searches

    async def _perform_searches(self, searches):
        tasks = [asyncio.create_task(self._search(item)) for item in searches]
        return [await t for t in asyncio.as_completed(tasks)]

    async def _search(self, item):
        res = await Runner.run(search_agent, item.query)
        return res.final_output

    async def _write_report(self, query: str, summaries):
        joined = "\n".join(summaries)
        output = await Runner.run(writer_agent,
            f"Original query: {query}\nResearch:\n{joined}"
        )
        return output.final_output
```

Run the research bot:

```bash
python -m examples.research_bot.main
# Then enter your query, e.g., "artificial photosynthesis"
```

**Key Takeaways:**

- `Runner.run` executes an agent and returns typed output.
- The manager controls handoffs; each agent remains single-purpose.
- Parallelism via `asyncio.as_completed` avoids bottlenecks.
- Built-in tracing (`trace`, `custom_span`) integrates with OpenAI Traces UI.

---

### Real-World Multi-Agent Systems

Multi-agent systems are scalable and great for enterprise. Here are some real-world examples:

1. **Customer-Support Copilot – Pets at Home (Microsoft Copilot Studio)**
    
    UK retailer *Pets at Home* is an early adopter of Microsoft’s Copilot Studio “AI employees.” Their deployment uses a **router agent** to triage incoming chats, then hands off to either a **Billing Bot** or **Tech-Support Bot**, while a **Tone-Critic agent** polishes replies before they’re sent to customers. [The Guardian](https://www.theguardian.com/technology/2024/oct/21/microsoft-launches-ai-employees-that-can-perform-some-business-tasks)
    
2. **Retail Pricing Pipeline – Revionics Multi-Agent AI Pricing System**
    
    Revionics (an Aptos company) unveiled a Vertex AI–powered platform where an **Ingest Bot** pulls competitive price data, a **Clean Bot** normalises product fields, a **Pricing Bot** forecasts margin impact, and a **QA Bot** validates rule compliance—all orchestrated as cooperating agents to let retailers roll out real-time price changes at scale. [Mass Market Retailers](https://massmarketretailers.com/revionics-unveils-multi-agent-ai-pricing-system/)
    
3. **Self-Driving Simulation – Waymo Waymax Library**
    
    Waymo’s open-source **Waymax** simulator runs hierarchical agents: a **Route-Planner** sets the trajectory, **Vision/Behavior agents** predict surrounding vehicles, a **Control agent** generates steering commands, and built-in **Safety agents** monitor collisions and off-road risk during every step of the closed-loop rollout—enabling large-scale testing of autonomous-driving policies. [waymo.com](https://waymo.com/research/waymax/)
    

### Build It With Us: From Idea to Production 🚀

In this bootcamp, you will:

1. **Design** a custom multi-agent workflow tailored to a real-world problem.
2. **Implement** and test agents using the OpenAI Agents SDK and tracing tools.
3. **Deploy** your multi-agent system and monitor performance with real-time traces.

By Week 6, you’ll deliver a production-grade pipeline that integrates with live APIs, handles errors gracefully, and demonstrates ROI with dashboard metrics.
