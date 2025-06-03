# **Day 6: Prompt Engineering**

## Prompt Engineering – Turning Instructions into Reliable Code

Building on yesterday’s lesson where we dove into tracing, guardrails, and evaluation metrics to keep our LLM agents safe, fast, and easy to debug—today we shift our focus to prompt engineering. In the first **AI Engineering bootcamp**, industry experts guided us through real-world examples of instrumenting traces and setting up eval pipelines to catch errors early and ensure consistent performance.

**Prompt engineering** is the art of structuring your inputs to coax reliable, accurate, and well-formatted outputs from large language models—a foundational skill for shipping dependable AI features. Below, you’ll find core best practices—drawn from OpenAI’s official guide—each illustrated with Python code snippets using the OpenAI client.

## Use the Latest Model

Newer models are generally more capable and easier to prompt effectively. Whenever performance and capability are critical, specify the most recent model in your API call. [OpenAI Help Center](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

```bash
import openai

response = openai.ChatCompletion.create(
    model="gpt-o3-mini",                # use the latest available model
    messages=[{"role": "user", 
               "content": "Summarize key takeaways from the following text."}],
    temperature=0.7,
    max_tokens=150
)
print(response.choices[0].message.content)
```

## Put Instructions First and Use Delimiters

Lead with a clear instruction, then separate your context using `###`, triple quotes (`"""`), or other delimiters. This reduces ambiguity about what part of the prompt is actionable. [OpenAI Help Center](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

```bash
import openai

prompt = """
Summarize the text below as a bullet-point list of the most important points.

Text: """
prompt += '"""' + long_document + '"""'

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)
print(response.choices[0].message.content)
```

## Be Specific About Context, Outcome, and Style

Clearly state any requirements—length, tone, focus areas, or style—to guide the model toward your intended result. [OpenAI Help Center](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

```python

import openai

prompt = """
Write a short, inspiring poem about OpenAI’s recent DALL·E launch,
in the style of Emily Dickinson, using no more than 6 lines.
"""

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8,
    max_tokens=80
)
print(response.choices[0].message.content)

```

## Iterate: Zero-Shot → Few-Shot → Fine-Tune

1. **Zero-shot**: Ask directly.
2. **Few-shot**: Provide 1–3 examples in the prompt.
3. **Fine-tune**: If neither suffices, prepare a labelled dataset and fine-tune. [OpenAI Help Center](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

```python
python
CopyEdit
# Zero-shot example
prompt_zero = "Extract keywords from the text below.\n\nText: " + text

# Few-shot example
prompt_few = """
Text 1: Stripe provides APIs...
Keywords 1: Stripe, APIs, payment processing
##
Text 2: OpenAI offers...
Keywords 2: OpenAI, language models, API
##
Text 3: """ + text + """
Keywords 3:
"""

for prompt in (prompt_zero, prompt_few):
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )
    print(resp.choices[0].message.content)

```

## Tune Core Parameters

- **model**: pick the most capable.
- **temperature**: 0 for factual tasks; 0.7–1.0 for creativity.
- **max_tokens**: hard cap on output length.
- **stop**: define end sequences to prevent overrun. [OpenAI Help Center](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

```python
python
CopyEdit
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"Generate three blog post titles on AI in healthcare."}],
    temperature=0.5,              # moderate creativity
    max_tokens=50,
    stop=["\n"]                   # stop after a newline
)
print(response.choices[0].message.content)

```

---

## Real-World Example: Leverage Structured Outputs

When your application needs to display or act on pieces of the model’s output (e.g. step-by-step tutoring), ask the API to return a strict JSON schema. Here’s a full Python example that wraps a “math tutor” prompt in a JSON-schema response format:

```bash
from textwrap import dedent
import openai

openai.api_key = "YOUR_API_KEY"
MODEL = "gpt-4o-mini"

math_tutor_prompt = '''
You are a helpful math tutor. You will be provided with a math problem,
and your goal will be to output a step by step solution, along with a final answer.
For each step, just provide the output as an equation; use the explanation field to detail the reasoning.
'''

def get_math_solution(question: str):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": dedent(math_tutor_prompt)
            },
            {
                "role": "user",
                "content": question
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "math_reasoning",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": "string"},
                                    "output":      {"type": "string"}
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False
                            }
                        },
                        "final_answer": {"type": "string"}
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )
    # The model’s reply is guaranteed to conform to the schema
    return response.choices[0].message.content

# Example usage:
question = "How can I solve 8x + 7 = -23?"
result_json = get_math_solution(question)
print(result_json)
```

**What happens under the hood:**

- **`response_format.type="json_schema"`** tells the API you want machine-readable output.
- You supply a full **JSON Schema** describing exactly the fields and types you expect.
- **`strict: True`** enforces no extra properties—if the model deviates, you’ll get a parsing error instead of malformed JSON.

The returned JSON might look like:

```bash
{
  "steps": [
    {
      "explanation": "Start by isolating the term with the variable. Subtract 7 from both sides.",
      "output":      "8x + 7 - 7 = -23 - 7"
    },
    {
      "explanation": "Simplify both sides: left side 7−7=0, right side −23−7=−30.",
      "output":      "8x = -30"
    },
    {
      "explanation": "Divide both sides by 8 to solve for x.",
      "output":      "8x/8 = -30/8"
    },
    {
      "explanation": "Reduce the fraction, dividing numerator and denominator by 2.",
      "output":      "x = -15/4"
    }
  ],
  "final_answer": "x = -15/4"
}
```

You can now loop over `steps` in your UI, showing one equation and its explanation at a time—perfect for guided tutoring.

---
