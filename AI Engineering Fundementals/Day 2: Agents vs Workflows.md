# Day 2: Agents vs Workflows

### Agents vs. Workflows: The Core Difference

"Agent" and "workflow" get tossed around a lot—but they mean very different things.

According to Anthropic:

> Workflows follow predefined code paths to orchestrate LLMs and tools.
> 
> 
> **Agents** direct their own tool use and decision-making on the fly.
> 

Put simply:

- **Workflows** = scripted steps.
- **Agents** = dynamic, self-directed behavior.

Workflows are ideal for tasks that require precision and repetition. Agents thrive in complex, changing environments.

### When to Use Agents vs. Workflows

Choosing between an agent and a workflow depends on the complexity and variability of the task at hand. Anthropic suggests:

- **Opt for Workflows** when:
    - Tasks are repetitive and well-defined.
    - Consistency and speed are paramount.
    - There's minimal need for decision-making or adaptation.
- **Opt for Agents** when:
    - Tasks are complex and require adaptability.
    - The environment is dynamic, and decisions need to be made in real-time.
    - There's a need for the system to learn and evolve over time.

It's also worth noting that hybrid approaches can be effective, where workflows handle routine tasks, and agents take over when adaptability is required.

### From Theory to Execution: Building Effective Agents

Now that you understand the difference between agents and workflows, it’s time to put that knowledge into practice. In this next section, we’ll explore how to actually build an effective agent using OpenAI’s Agent SDK. You’ll also learn how to implement one of the five common workflow patterns called routing by leveraging built-in tools and modular agent design. Let’s get into how it all comes together.

## Building Blocks

The OpenAI Agent SDK introduces some old and some new concepts to define and manage agent workflows:

- Agents: LLMs configured with instructions, tools, guardrails, and handoffs
- Tools: Functions that agents can use to take actions beyond just generating text
- Handoffs: A specialized tool used for transferring control between agents
- Context: Memory of past actions and custom context passed to
- Guardrails: Configurable safety checks for input and output validation

*The Agent SDK also has a tracing module that allows you to view, debug, and optimize your workflows inside OpenAI’s developer dashboard. 

### **How to define agents in OpenAI SDK?**

```jsx
from agents import Agent

basic_agent = Agent(
   name="My First Agent",
   instructions="You are a helpful coding tutor.",
   model="gpt-4o"  # Optional: defaults to "gpt-4o" if not specified
)

```

                          **

![image.png](attachment:6554702d-8985-4abd-b3f6-03927f2ca03c:image.png)

*Agent as a feedback loop with access to your custom environment*

At the center of the OpenAI Agent SDK is the Agent class. It has 3 main components: **name, instructions, and model.**

Additionally, you can select and define more attributes, like *tools, output_type, and handoffs*. See the [**documentation**](https://openai.github.io/openai-agents-python/agents/?utm_source=breakintodata.beehiiv.com&utm_medium=newsletter&utm_campaign=build-effective-agents-with-openai-agents-sdk) for more details.

### Workflow Patterns You’ll Learn

A **workflow** is a structured system where an LLM or tool follows a predefined sequence of steps to complete a task. Unlike agents, which dynamically decide how to act, workflows operate on a fixed path—great for reliability, speed, and repeatability.

Anthropic outlines five powerful workflow patterns that help LLM systems scale with consistency and structure. Here’s what we’ll be exploring:

- **Prompt Chaining**
    
    Breaks down a complex task into multiple LLM calls, where the output of one step becomes the input for the next. Great for tasks that benefit from staged reasoning or transformation.
    
    ![image.png](attachment:c60f8d7e-4205-4a22-a1b2-f88a058043af:image.png)
    
- **Parallelization**
    
    Speeds things up by running multiple calls at once.
    
    - *Sectioning*: Breaks a task into independent pieces.
    - *Voting*: Runs the same task several times and picks the best answer.
    - 

![image.png](attachment:75b5b4bd-8591-4248-a32b-8baee41df794:image.png)

- **Orchestrator–Workers**
    
    A main LLM (the orchestrator) assigns subtasks to worker LLMs. Unlike parallelization, subtasks are generated dynamically, depending on what the input requires.
    
    ![image.png](attachment:a2c4ef0d-6712-4771-8592-ff9c82f2d854:image.png)
    
- **Evaluator–Optimizer**
    
    Think of this like peer review. One model generates, another evaluates, and the first improves its output based on feedback—just like a writer and editor.
    
    ![image.png](attachment:7694e9df-8cf9-4972-9b64-d101f000df3d:image.png)
    
- **Routing**
    
    Classifies the user’s input and sends it down the right specialized workflow. This keeps performance high by customizing how different input types are handled.
    
    ![image.png](attachment:25a2f368-a650-422b-98ad-eb3673cf4773:image.png)
    

You’ve just explored one of the most critical choices in modern AI systems—**agents vs. workflows**—and got a preview of the building blocks that bring them to life.

Tomorrow, we’ll dive into how to **build agents using the OpenAI SDK**, with a focus on **tool use and retrieval-augmented generation (RAG)** to supercharge your agent’s capabilities.

[**Join the Bootcamp Now**](https://www.notion.so/Day-1-What-are-AI-Agents-595fb7d80cc4474493498da663a3aca1?pvs=21) and start bringing your intelligent systems to life.

Let’s make agents that don’t just follow scripts—but lead.
