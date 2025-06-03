# Day 1: What are AI Agents?

Welcome to Day 1 of the AI Agent Bootcamp—where we go beyond the hype and get hands-on with the next generation of AI systems.

AI agents aren’t just a trend—they’re quickly becoming the foundation of modern business operations. According to [*AI Agents Statistics: Usage and Market Insights (2025)* by Litslink](https://litslink.com/blog/ai-agent-statistics), **85% of enterprises are projected to use AI agents this year**, with the global market expected to hit **$7.63 billion**. What’s driving the surge? Advances in automation, more powerful AI models, and deep integration into enterprise workflows and consumer products. In short: **agents are no longer optional—they’re essential**.

Here’s a look at what we’ll cover over the next two weeks in the bootcamp. 

### Module 1: Foundations of Agent Design

- **Day 1: What Are AI Agents?**
    
    Understand what agents are, how they work, and why they’re transforming AI.
    
- **Day 2: Agents vs Workflows**
    
    Learn the architectural differences and when to use each.
    
- **Day 3: RAG & Tool Use**
    
    Make your agents smarter and more useful with retrieval and tool execution.
    
- **Day 4: Memory – Teaching Agents to Remember**
    
    Explore short-term and long-term memory strategies for personalized, context-aware agents.
    
- **Day 5: Guardrails & Tracing**
    
    Build safer, more reliable agents with validation, monitoring, and observability tools.
    
- **Day 6: Prompt Engineering**
    
    Master the art of structuring prompts to guide agent behavior and reasoning.
    
- **Day 7: Tool-Calling & Orchestration**
    
    Coordinate tools, models, and workflows to create robust, multi-step systems.
    

### Module 2: Building and Shipping Agents

- **Day 8: GitHub Dev Setup**
    
    Set up your agent development environment using GitHub.
    
- **Day 9: Cursor & Practice**
    
    Learn and practice building agents in Cursor with real-world tasks.
    
- **Day 10: Deploying with Vercel**
    
    Deploy your agent as a web app using Vercel’s serverless infrastructure.
    
- **Day 11: Model Pricing**
    
    Understand token usage, cost estimation, and how to build budget-aware agents.
    
- **Day 12: Web App Fundamentals**
    
    Cover the basics of building interactive, agent-powered web applications.
    
- **Day 13: TypeScript Crash Course**
    
    Learn enough TypeScript to confidently build and debug your agent frontends.
    
- **Day 14: APIs & Web Communication**
    
    Connect agents to external data and services via APIs and HTTP requests.
    

Today, we’re diving into the core question: *What exactly is an AI agent?* And more importantly—*why should you care?* 

We are basing this information off our AI Engineering Bootcamp. 

### The Agent Boom Is Real

Let’s talk about *why now*—the numbers say it all.

The **global Agentic AI market** is set to grow from **$5.2B in 2024** to **$196.6B by 2034** (CAGR: **43.8%**).

What’s driving this?

- **Ready-to-Deploy Agents**: Plug-and-play AI assistants for fast adoption.
- **Build-Your-Own Frameworks**: Custom agents for devs and orgs with unique needs.

In a few years, agents won’t just assist—they’ll run operations, manage workflows, and enhance products across industries.

Whether you’re building tools or exploring the space—now’s the time to learn.

### What is an AI Agent?

Let’s unpack the term.

> AI agents take vague goals and figure out how to achieve them.
> 

You don’t write prompts—you give them objectives like “Book a flight + hotel,” and they figure it out.

Anthropic offers a helpful breakdown:

> “Workflows follow fixed steps, with tools orchestrated by code.
> 
> 
> *Agents* decide *how* to use tools and act dynamically to hit goals.”
> 

In short: If it follows a script, it’s a *workflow*. If it figures it out on the fly, it’s an *agent*.

### Autonomy, but With Guardrails

How *autonomous* are these agents?

They still need a **human-in-the-loop**—you decide when they should ask for help or confirm before acting.

The goal? Eliminate rigid prompting. Agents should just *do the task*.

Vellum AI describes six levels of autonomy:

| Level | Role | Behavior |
| --- | --- | --- |
| L0 | Follower | Executes fixed rules |
| L1 | Executor | Responds to input, no planning |
| L2 | Actor | Uses tools when prompted |
| L3 | Operator | Plans and adjusts actions |
| L4 | Autonomous | Sets goals, adapts |
| L5 | Innovator | Creates novel solutions |

Most agents today live in **L2–L3** territory. **L4+** is where real autonomy starts.

### From Theory to Practice: Real-World Use Cases

Agents are already in the wild—doing useful stuff across industries:

| Use Case | Example |
| --- | --- |
| Medical AI | Suggesting meds from patient history |
| Travel | Booking flights + hotels from vague queries |
| Sales | Automating lead enrichment and follow-ups |
| Stock Trading | Executing trades and monitoring markets |
| Customer Support | Resolving tickets 24/7 |
| Doc Editing | Rewriting tone, fixing grammar |
| AI Tutoring | Guiding learning journeys |
| Robotics | Making real-time physical decisions |
| Trust & Safety | Moderating based on nuanced context |

### Picking Your Tools: Agent Frameworks

**What is an agent framework?**

An agent framework is a set of tools and abstractions that helps you design, build, and manage AI agents. It takes care of the infrastructure—like tool use, memory, and planning—so you can focus on building smarter, task-driven systems.

Choosing the right agent framework depends on what you need under the hood. Some prioritize **streaming** for real-time feedback, while others focus on integrations like a **code interpreter** or support built-in **tracing platforms** for observability. For now, **optimization features** like memory-efficient execution aren’t yet standard across the board—but expect this to evolve. Here’s a quick look at how some of the top frameworks compare:

| Characteristic | LangGraph | Agents SDK | Mastra | CrewAI |
| --- | --- | --- | --- | --- |
| Streaming | ✅ | ✅ | ✅ | ✅ |
| Optimization | ❌ | ❌ | ❌ | ❌ |
| Code interpreter | ❌ | ✅ | ❌ | ✅ |
| Tracing Platform | ✅ | ✅ | ❌ | ❌ |

**For this course, we’ll be using the OpenAI SDK for all examples**—so you can follow along and start building immediately.

These frameworks make it easier to structure agents—but behind every framework is the same powerful core: the large language model. Let’s break down how LLM agents actually think, plan, and act.

### Under the Hood: How LLM Agents Actually Work

Lilian Weng’s agent framework highlights 3 core parts:

- **Planning**: Breaks down tasks into smaller goals. Think: Chain-of-Thought reasoning.
- **Memory**: Short-term (in prompt) + long-term (external store) for context retention. We will talk more about this on Day 4.
- **Tool Use**: Connects to APIs, code interpreters, search, calculators, etc.

Together, these make agents flexible and capable of complex, real-time decision-making.

![image (4)](https://github.com/user-attachments/assets/98506998-45b9-41bf-b059-d7373ff3ce27)
