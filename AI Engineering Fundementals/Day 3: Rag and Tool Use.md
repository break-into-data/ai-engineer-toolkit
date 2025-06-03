# Day 3: Rag and Tool Use

Generative AI is powerful, but today we’re diving into two capabilities that make it *practical*: **Retrieval-Augmented Generation (RAG)** and **Tool Use**. These are the keys to grounding your agents in real-world data—and letting them take real-world actions.

Let’s start with RAG—the secret sauce for making AI more accurate and reliable.

**Retrieval-Augmented Generation** bridges the gap between static LLM knowledge and up-to-date, relevant information. Instead of relying only on what the model was trained on, RAG lets your agent pull in current, domain-specific data at runtime.

**How it works:**

1. **Indexing**: External data is embedded and stored in a vector database.
2. **Retrieval**: When a query is made, relevant docs are pulled based on similarity.
3. **Augmentation**: Those results are added to the LLM’s prompt.
4. **Generation**: The model creates a response using both training and retrieved data.

**Why it matters:**

- Reduces hallucinations
- Answers with up-to-date info
- Uses internal company data
- Supports citations
- Avoids retraining models

### A Real Example: Grocery Search with RAG

To see RAG in action, let’s look at this example

![image (11)](https://github.com/user-attachments/assets/013d624c-e556-4a29-8c94-56e052943475)

This diagram shows the core flow of Retrieval-Augmented Generation: a user submits a query, the system retrieves relevant data from connected sources, then combines that data with the query and passes it to the LLM. The model uses both the question and the retrieved context to generate a grounded, accurate response—closing the loop by sending the answer back to the user.

RAG isn’t just about tossing queries into a vector store—it’s a full **search strategy**. It starts by retrieving relevant content from external data sources, then feeds both the query and retrieved info into the LLM. The result? Answers grounded in real, up-to-date knowledge. It’s not just about finding similar text—it’s about combining metadata filtering, semantic search, and reranking to deliver context-rich, accurate responses.

### What Is Tool Use?

RAG is about knowing more. But what about *doing* more?

That’s where **Tool Use** comes in. Tool use lets your agent move from being a smart assistant to an *action-taker*. It can fetch live data, call APIs, run code, or interact with software—all automatically.

**Two common patterns:**

- **Chains**: Pre-set sequences of tool use.
- **Agents**: Decide dynamically which tools to use and when.

**Typical process:**

- Define the tool (function/API)
- Parse the LLM output
- Execute the tool with structured input

### Built-In Tools: Out-of-the-Box Power

OpenAI's Agent SDK comes equipped with several hosted tools that empower agents to perform complex tasks without extensive setup:

- **WebSearchTool**: Enables agents to fetch real-time information from the internet, providing up-to-date responses.
- **FileSearchTool**: Allows agents to retrieve information from OpenAI Vector Stores, facilitating access to proprietary or domain-specific knowledge. [OpenAI GitHub](https://openai.github.io/openai-agents-python/tools/?utm_source=chatgpt.com)
- **ComputerTool**: Grants agents the ability to perform tasks on a computer, such as file manipulation or executing commands, enhancing automation capabilities. [OpenAI GitHub](https://openai.github.io/openai-agents-python/tools/?utm_source=chatgpt.com)

These tools are designed to work seamlessly with OpenAI models, streamlining the development of sophisticated AI agents.

### Using Hosted Tools in Your Agent

Here’s a quick example of how to equip your agent with **hosted tools** using the OpenAI SDK:

```jsx
from agents import Agent, FileSearchTool, Runner, WebSearchTool

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["VECTOR_STORE_ID"],
        ),
    ],
)

async def main():
    result = await Runner.run(agent, "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?")
    print(result.final_output)

```

This agent is equipped with two powerful tools—**WebSearchTool** and **FileSearchTool**. When given a natural language prompt, it can pull live data from the web and context from a vector store to generate a personalized answer. It’s a prime example of RAG and Tool Use working together in action

### Your Journey Starts Here

You’ve just leveled up your agents with two game-changing capabilities—RAG and tool use—turning them into systems that can access real-time information and take meaningful action.
Tomorrow, we’ll explore another critical ingredient: memory. You’ll learn how to teach your agents to remember past interactions, retain long-term context, and build smarter, more personal experiences.

