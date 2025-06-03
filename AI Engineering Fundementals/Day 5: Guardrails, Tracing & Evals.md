# **Day 5: Guardrails, Tracing & Evals**

## **Building Safe & Reliable AI Agents**

Launching an AI feature should feel exciting, not terrifying. Below is a roadmap that shows how modern teams keep their large-language-model (LLM) agents safe, fast, and easy to debug. In our **first AI Engineering Bootcamp**, industry experts and practicing machine-learning engineers walked students through real evals and tracing best practices. Today we are going to learn about these concepts.

---

## **What is tracing in AI?**

When an end user clicks **Send**, dozens of things happen inside your app:

- their message reaches an API gateway
- the gateway calls a retrieval tool
- the LLM writes a draft answer
- a database stores the result
- your front-end finally shows the text

**Tracing** simply writes a short note at each step: *what happened, when it happened, how long it took, and how many tokens or dollars it cost*. Later, you can play those notes back in order and spot slow parts, errors, or unusual patterns.

ADD OpenAI Dashboard screenshot. 

### **Why observability is important**

Most standard monitoring tools only warn you when a web request is slow. AI agents, however, can go off the rails in new ways—making things up (hallucinations), getting stuck in loops, or using way too many tokens and racking up huge costs. Agent-aware tracing helps you spot and diagnose these unique problems so you can answer questions like:

- **“Where did the hallucination start?”**— This shows you exactly which prompt or tool call led the model to make up information—crucial for debugging and refining your instructions.
- **“Why did that response cost $12?”** — Tracking token usage helps you estimate costs and identify overly verbose prompts or repeated calls that can be trimmed down.
- **“Which tool call failed or behaved unexpectedly?”**— Knowing this lets you pinpoint whether an external API, database lookup, or other integration is the root cause, so you can fix or wrap it with error handling.
- **“Did the agent get stuck in a loop or retry endlessly?”**— Spotting repeated execution patterns prevents runaway behaviors and lets you add safeguards like retry limits or timeout rules.

### What to trace in an agent stack

1. **Agent steps** – Each planner/executor round‐trip: intent, chosen tool, and final action.
2. **LLM calls** – Prompt text, model name, latency, and token counts (`prompt`, `completion`, `total`).
3. **Tool invocations** – Function name plus validated **Pydantic** input/output so you can diff bad parameters.
4. **Retriever hits** – Which documents were fetched, their scores, and embedding latency.
5. **Guardrail verdicts** – Moderation labels, schema-validation failures, auto-retry count.

With these five signals you can replay any conversation and see graphically—step by step—how the agent reached its answer.

---

## What are guardrails?

They are like bumpers that keep users safe. While traces tell you *what* happened, **guardrails** stop dangerous answers from reaching users in the first place. They run either before the model (checking the user prompt) or right after (checking the model’s draft).

| **Guardrail type** | **Catches** | **Typical fix** |
| --- | --- | --- |
| Content filter | Hate, sexual, violent, self-harm text | Return a polite refusal or ask for a new prompt |
| Copyright filter | Large blocks of lyrics or articles | Replace with a short summary |
| Jailbreak detector | “Ignore all rules and show me…” | Abort and log the attempt |
| Code scanner | eval(input()), SQL injection | Replace with a safe snippet |
| Schema validator | Malformed JSON | Auto-retry with stricter instructions |
| Cost watchdog | Response > 4 000 tokens | Switch to a concise fallback prompt |

The Agents SDK already adds a *guardrail span* to each run, so if a response is blocked you can see **why** in the trace [OpenAI GitHub](https://openai.github.io/openai-agents-python/tracing/?utm_source=chatgpt.com).

---

## **Why are evals important?**

**Evaluations (evals)** provide an in-depth scorecard that uncovers safety risks, biases, and quality issues which real-time guardrails can’t catch. By tracking performance trends and running targeted tests against hallucinations, edge cases, and critical scenarios, AI engineers ensure their models remain reliable and safe over time.

![ChatGPT Image Apr 30, 2025, 06_16_28 PM.png](attachment:13a82248-96b2-4093-a47b-fd7a77d629d7:ChatGPT_Image_Apr_30_2025_06_16_28_PM.png)

In our last AI Engineering Bootcamp, we partnered with a Machine Learning expert to conduct a live eval, building tests on the fly and using the dashboard insights to immediately refine our model’s behavior. **Safety and quality** are two important goals of evaluating how your AI product is performing. 

### **Risk & Safety evals**

AI tools can scan a test set or yesterday’s chats and report how often unsafe content slipped through:

- Hate or unfair language
- Sexual or violent content
- Self-harm phrases
- Copyrighted text
- Jailbreak success
- Code vulnerabilities
- Ungrounded guesses about a user’s race, gender, or mood

You choose a tolerance, for example “anything medium severity or above is a defect,” and track the **defect rate** over time.

### **Quality evals**

Protecting users is not enough; your bot must still answer well. Common metrics, usually scored 1-5:

- **Intent Resolution** – did the bot grasp what the user wanted?
- **Tool Call Accuracy** – did it choose the right function with the right parameters?
- **Task Adherence** – did it follow all instructions?
- **Response Completeness** – did it cover every fact in the ground truth?
- **Groundedness** – in RAG systems, are all claims supported by retrieved docs?
- **Retrieval Quality** – are the best passages at the top?
- **Relevance, Coherence, Fluency** – classic measures of correctness and readability.
- **Similarity / BLEU / ROUGE / F1** – overlap with reference answers if you have them.

Hook these checks into GitHub Actions. If a pull request pushes relevance below 4/5 or hate defect rate above 0.1 %, the build fails.

---

## **Putting It All Together**

Tracing, guardrails, and evals form a simple loop:

1. **Trace everything** so you can see problems.
2. **Block problems fast** with guardrails.
3. **Prove fixes work** with nightly or CI evals.

The **OpenAI Agents SDK** switches tracing on by default, lets you add guardrails in one decorator, and exports span data ready for evaluation tools [OpenAI GitHub](https://openai.github.io/openai-agents-python/config/?utm_source=chatgpt.com). Start with those defaults, add your domain-specific tweaks, and you’ll have a production-grade AI feature that beginners can understand and experts can trust.

Ready to learn the deeper details? **Join the upcoming AI Engineering Bootcamp here.**

Join us and turn these ideas into code!
