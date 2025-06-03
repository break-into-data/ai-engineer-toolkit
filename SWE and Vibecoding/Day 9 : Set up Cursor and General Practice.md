Today you’ll get hands-on with Cursor, an AI-powered coding environment that streamlines your development process. You’ll also explore everyday practices used by professional software engineers—like writing clean code, using version control effectively, and reviewing code with confidence. Building on yesterday’s GitHub setup, this will make you feel at home in your dev environment and ready for more advanced workflows.

### Set up Cursor IDE

**1. Download & Install**

- Visit [https://www.cursor.so](https://www.cursor.so/) and download the version for your operating system (macOS, Windows, or Linux).
- Sign in using your GitHub account to unlock full project sync capabilities.
- System Requirements:
    - macOS 11 or later
    - Windows 10 or later
    - Linux: Ubuntu 20.04+ recommended
- Installation walkthrough:
    - macOS: Drag Cursor to Applications folder
    - Windows: Run the `.exe` installer
    - Linux: Use `.AppImage` or `.deb` package

**2. Cursor IDE Configuration**

**2.1. Initial Setup & AI Integration**

- **API Key Configuration**:
    - On first launch, you'll be prompted to log in or create a Cursor account
    - Grant the required permissions for Git integration.
    - Choose your preferred AI model integration:
        - **OpenAI Integration**:
            - Required for GPT-4 models
            - Requires an OpenAI API key from [platform.openai.com](https://platform.openai.com/)
            - Enter your key in Settings → OpenAI API Key
        - **Claude Integration**:
            - Recommended for more detailed code explanations and reasoning
            - Requires an Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
            - Enter your key in Settings → Anthropic API Key
        - **Default Models**: Uses Cursor's built-in models (no external API key required)
    - Test your connection by pressing Ctrl+K (Cmd+K on Mac) and typing "Hello"

**2.2. Model Considerations & Selection**

- **Model Selection**:
    - Navigate to Settings → Model selection
    - Choose from available options:
        - **Cursor Basic**: Free built-in model (good for simple completions)
        - **GPT-3.5 Turbo**: Balanced speed/quality for most coding tasks
        - **GPT-4**: Most capable for complex coding tasks (higher token cost)
        - **Claude 3.7 Sonnet**: Excellent reasoning and explanation capabilities
    - Consider the pros and cons of each model:
        
        ![Screenshot 2025-04-18 at 11.07.24 AM.png](attachment:e8d7c982-7d78-4dbd-b5c4-357c748f5590:Screenshot_2025-04-18_at_11.07.24_AM.png)
        

**2.3. Installing Essential Extensions**

- Open Extensions panel (Ctrl+Shift+X or Cmd+Shift+X on Mac)
- **Recommended Extensions**:
    - **GitLens**: Enhanced Git capabilities
    - **Prettier**: Code formatting
    - **ESLint**: JavaScript/TypeScript linting
    - **Python**: Python language support
- Extensions from VS Code marketplace are compatible with Cursor

### Best Practices When Using Cursor

**1. Effective AI Prompting**

- **Be Specific and Clear**:
    - Use detailed instructions: "Create a React component that displays a sortable table with pagination" vs "Make a table"
    - Specify language, frameworks, and libraries: "Using TypeScript and React hooks..."
    - Include requirements and constraints: "Must handle error states and follow accessibility guidelines"
- **Context-Aware Prompts**:
    - Select relevant code before asking questions
    - Reference specific files or functions in your prompts
    - Use "I want to..." or "Help me..." to clarify your intent

**2. Setting Up System Rules**

- Navigate to Settings → System Rules

![Screenshot 2025-04-18 at 10 52 02 AM](https://github.com/user-attachments/assets/09a832f9-4a6d-4f68-a099-3141876a0f7a)

- Create custom system rules for consistent coding:
    
    ```
    
    When writing TypeScript code:
    - Add types to all variables and function parameters
    - Use meaningful variable and function names
    - Include comments for any complex logic
    - Break down complex functions into smaller, simpler ones
    - Use console.log() statements to help with debugging
    - Remember to handle potential errors with try/catch blocks
    - Add // TODO: comments for incomplete sections
    
    ```
    
- Create project-specific rules:
    
    ```
    
    For this TypeScript AI application:
    - Store API keys in .env files (never commit these to GitHub)
    - Create separate files for different features
    - Use simple interfaces to define AI response structures
    - Include examples in comments for how functions should be used
    - Add basic error messages for users when AI calls fail
    - Start with simple AI features before adding complex ones
    - Test your code with sample inputs before connecting to real AI APIs
    - Keep AI prompt templates in a separate config file for easy updates
    
    ```
    

**3. Token Usage Optimization**

- **Monitor Usage**:
    - Check token usage in Settings → AI → Usage
    - Free tier typically offers ~500K tokens/month
    - Pro tier (~$20/month) provides significantly higher limits
- **Conservation Strategies**:
    - Select specific code segments instead of entire files
    - Break large tasks into smaller, focused prompts
    - Use Cursor's "Continue" feature instead of new prompts
    - Clear chat context when switching between unrelated tasks

**4. AI-Enhanced Git Workflow**

- Use AI to help write meaningful commit messages:

```markdown
Prompt: "Summarize the changes I've made as a concise commit message”
```

- Get help reviewing pull requests:

```markdown
Prompt: "Review these changes and identify potential issues or improvements"
```

- Generate documentation for your code:

```markdown
Prompt: "Create a README.md file explaining this project's structure and setup"
```

**5. Keyboard Shortcuts for Maximum Efficiency**

- **Essential Shortcuts**:
    - `Ctrl+K` / `Cmd+K`: Open AI Command palette
    - `Ctrl+L` / `Cmd+L`: Open AI Chat panel
    - `Alt+\` / `Option+\`: Generate code completion
    - `Ctrl+Shift+L` / `Cmd+Shift+L`: Explain selected code
    - `F1` or `Ctrl+Shift+P` / `Cmd+Shift+P`: Command palette
- Create a custom keyboard shortcut cheat sheet for your workflow

🔗 Cursor Docs: [Getting Started](https://docs.cursor.so/)

[Cursor IDE AI Features Guide](https://www.notion.so/Cursor-IDE-AI-Features-Guide-1d9b8a917a9980c497a1e9019d1f8fb4?pvs=21)

## 🧑‍💻 Guided Hands-On - Build Your First GitHub Project with Cursor

### 🎯 Objective

By the end of this exercise, you’ll:

- Set up and clone a new GitHub repo
- Create and edit files using Cursor IDE
- Practice basic Git commands
- Make and push commits
- Open and merge a pull request

---

### 🧱 Starter Project Structure

We’ll be creating this simple folder:

```

📦 my-first-repo
├── 📁 src
│   └── main.py / index.ts
├── 📄 .gitignore
├── 📄 README.md
```

You’ll choose either `main.py` (Python) or `index.ts` (TypeScript) depending on your preference.

---

### 🛠 Step-by-Step Instructions

### ✅ 1. Create a GitHub Repo

- Go to [GitHub](https://github.com/)
- Click `+` → **New repository**
- Name it `my-first-repo`
- Select **Public** (or Private)
- **DO NOT** initialize with a README
- Click **Create repository**

---

### 🖥️ 2. Clone it Locally

Open Cursor IDE terminal or your native terminal and run:

```bash
git clone https://github.com/your-username/my-first-repo.git
cd my-first-rep
```

---

### 🧾 3. Add Your Files

Inside the project directory:

```bash
mkdir src
touch README.md
touch .gitignore
touch src/main.py     # Or use src/index.ts for TS
```

✏️ Edit `README.md` to include:

```markdown
# My First Repo

Tech Stack: Python / TypeScript
Author: [Your Name]

## Setup

1. Clone this repo
2. Run the main file
```

✏️ (If using Python) Edit `main.py` to include :

```python
def greet(name):
return f"Hello, {name}! Welcome to your first project."
print(greet("Bootcamper"))
```

✏️ (If using Typescript) Edit `index.ts` to include :

```tsx
function greet(name: string): string {
return Hello, ${name}! Welcome to your first project.;
}
console.log(greet("Bootcamper"));
```

✏️ In `.gitignore`, add common ignores:

- Python: `__pycache__`, `.env`
- TypeScript: `node_modules`, `.env`
- Add files and folders you want git to ignore

For Example:

```
# Node.js
node_modules/
.env

# Python
__pycache__/
*.pyc

# macOS
.DS_Store
```

This helps keep your repository clean and free from sensitive or system-specific files.

---

### 🌿 4. Initialize Git Locally

```bash
git init
git add .
git commit -m "init: create project structure"
git branch -M main
git remote add origin https://github.com/your-username/my-first-repo.git
git push -u origin mai
```

---

### 🌱 5. Create a Feature Branch

```bash
git checkout -b feature/update-readme
```

Edit the `README.md` to add a new section like:

```markdown
## Features

- Sample AI tool coming soon!
```

Then:

```bash
git add README.md
git commit -m "docs: update README with features section"
git push origin feature/update-readme

```

---

### Pro Tips

- **Use semantic commit messages**: These messages follow a convention to describe the type and purpose of a commit.
    - Example: `feat: add search bar` — This means you added a new feature.
    - Common prefixes:
        - `feat:` for a new feature
        - `fix:` for a bug fix
        - `docs:` for documentation changes
        - `refactor:` for code improvements without changing behavior

### 🔄 6. Open a Pull Request (PR)

- Go to GitHub repo
- You’ll see a suggestion to open a PR → Click “Compare & pull request”
- Add a title + description, then click **Create Pull Request**
- Click **Merge Pull Request** → **Confirm**

### 🧠 7. Bonus: Use Cursor IDE AI

Try asking Cursor:

- “Generate a Python function that returns the current date”
- “Write a TypeScript function that capitalizes all letters in a string”
- “Explain this code” (select any line)

## 🚀 Next Steps: Your AI Product Engineering Journey

This simple exercise is just the beginning of what you'll build in our AI Product Engineering Bootcamp! Building on these fundamental skills, you'll soon:

### Through the Bootcamp, you’ll gain a hands-on understanding of:

- **Full-stack AI applications** that leverage modern LLMs
- **Intelligent chatbots** with memory and context awareness
- **Vector databases** for semantic search and recommendation systems
- **RAG** (Retrieval Augmented Generation) tools
- **Production-ready AI systems** with proper authentication and security
