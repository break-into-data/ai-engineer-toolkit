This module will help you get fully set up with your developer environment, regardless of your technical background, critical for success in modern AI engineering.

## 🎯 Learning Objectives

By completing this module, you'll be able to:

- Set up and navigate a professional development environment
- Understand and utilize version control with Git and GitHub
- Install and leverage Cursor IDE's AI-powered features
- Apply best practices for code management and collaboration
- Brief overview into advanced CI/CD and deployment topics

# DAY 8: Development Environment Setup (Github, Cursor)

## 📚 Section 1: Setting Up Your Development Environment

### GitHub Setup

**1. Create a GitHub Account**

- Register at [github.com](https://github.com/)
- Choose a free plan
- 🔗 [Learn the basics of Github](https://docs.github.com/en/get-started/start-your-journey)
- 🔗 GitHub Docs: [Hello World](https://docs.github.com/en/get-started/quickstart/hello-world)
- [Optional] [Set up two-factor authentication (2FA) for security](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication)

**2. Configure SSH/HTTPs for GitHub**

- 📹 [Connecting GitHub to your local environment (via HTTPS/SSH)](https://www.google.com/search?q=Connecting+GitHub+to+your+local+environment+(via+HTTPS%2FSSH)&oq=Connecting+GitHub+to+your+local+environment+(via+HTTPS%2FSSH)&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQIRifBTIHCAIQIRifBTIHCAMQIRifBTIHCAQQIRifBdIBBzQ4OWowajeoAgCwAgA&sourceid=chrome&ie=UTF-8#fpstate=ive&vld=cid:1c41ebf3,vid:Msw7WJPqS34,st:0)
- Test your connection to GitHub
    - **SSH**:
    
    ```bash
    ssh -T git@github.com
    ```
    
    - **HTTPS**:
    
    ```bash
    curl -I https://github.com
    ```
    
    ✅ If the connection is successful, you'll see either a greeting (SSH) or a response like `HTTP/2 200`(HTTPS).
    

### Terminal Setup

The terminal is your command center. It lets you interact directly with your computer’s operating system, manage files, run programs, and most importantly — work with Git. Here are the foundational commands you need to know.

**1. Choose & Configure Your Terminal**

- **Windows**: Install Windows Terminal or Git Bash
- **macOS**: Use Terminal or install iTerm2
- **Linux**: Use your distribution's terminal

**2. Essential Terminal Commands**

- **Navigation Commands:**

These help you move around your file system quickly and see what’s inside each folder.

| Command | Purpose | Example |
| --- | --- | --- |
| `cd` | **Change directory** – move between folders. | `cd my-project` |
| `ls` | **List contents** of a directory. | `ls` or `ls -la` |
| `pwd` | **Print working directory** – shows your current location in the system. | `pwd` |
- **File and Folder Management:**

When coding, you’ll constantly be adding, renaming, and organizing files. Mastering these saves time and keeps your project neat.

| Command | Purpose | Example |
| --- | --- | --- |
| `mkdir` | **Make directory** – create a new folder. | `mkdir src` |
| `touch` | **Create a file** quickly. | `touch index.ts` |
| `rm` | **Remove file or folder** (`-r` for folders). Be careful! | `rm oldfile.txt` or `rm -r old_folder` |
| `cp` | **Copy files** or directories. | `cp main.py backup.py` |
| `mv` | **Move or rename** files. | `mv temp.txt notes.txt` |

## 📚 Section 2: Version Control with Git

### Git Fundamentals

**1. What is Version Control?**

**The Problem Version Control Solves**

- **Code History & Tracking**: Ever saved multiple versions of a file like "final.doc", "final_v2.doc", "really_final.doc"? Version control eliminates this by tracking all changes in a structured way.
- **Collaboration Challenges**: Without version control, team members might overwrite each other's work or struggle to merge changes from multiple contributors.
- **Backup & Recovery**: Provides a complete history that serves as both documentation and backup, allowing you to recover previous states if something goes wrong.
- **Experimentation Safety**: Enables developers to try new ideas without fear, as they can always revert to previous working versions.

![ChatGPT Image May 1, 2025, 02_12_01 PM](https://github.com/user-attachments/assets/d0b8c29f-463d-4cfd-8828-fdd66d3df784)

**2. How Git Tracks Changes Over Time**

- **Snapshots, Not Differences**: Unlike other systems that store differences between files, Git takes a "snapshot" of all files at each commit
- **The Three States of Git**:
    - **Working Directory**: Where you modify files
    - **Staging Area** (Index): Where you prepare changes for a commit
    - **Repository**: The .git directory storing all versions
- **Commit Hash**: Every commit gets a unique identifier (hash) based on its contents
- **Branching Model**: Git uses lightweight branches that make parallel development easy

*Main and Development Branches*

![ChatGPT Image May 1, 2025, 02_22_51 PM](https://github.com/user-attachments/assets/bf6ca8da-4a4b-4053-adfb-efa65a3474b8)

*Image Resource: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow*



### Installing Git

**1. Installation Instructions by Operating System**

**For Windows:**

1. Download the installer from [git-scm.com](https://git-scm.com/)
2. Run the installer with default options (customize if needed)
3. Important options to consider:
    - Default editor (recommend VS Code or Notepad++ for beginners)
    - PATH environment (recommend "Git from the command line and also from 3rd-party software")

**For macOS:**

1. **Option 1 - Homebrew** (recommended):

```bash

brew install git
```

1. **Option 2 - Standalone Installer**:
    - Download from [git-scm.com](https://git-scm.com/)
    - Run the .dmg installer and follow prompts
2. **Option 3 - Command Line Tools**:

```bash
xcode-select --install
```

**2. Initial Git Configuration**

After installing Git, set up your identity with the following commands:

```bash

# Set your name (appears in commit history)
git config --global user.name "Your Name"

# Set your email (links commits to your GitHub account)
git config --global user.email "your.email@example.com"
```

**3. Verifying Your Installation**

Check that Git is properly installed by running:

```bash

git --version
```

You should see something like:

```

git version 2.41.0
```

View your configuration settings:

```bash
git config --list
```

Basic test to ensure Git is working:

```bash

# Create a test repository
mkdir git-test
cd git-test
git init

# You should see a message about initializing a repository# and a .git directory will be created
```

**Common Installation Troubleshooting:**

- **"Command not found"**: Git isn't in your PATH. Try restarting your terminal or adding Git to your PATH manually.
- **Permission issues**: Try running the commands with administrator privileges (sudo on Mac/Linux).
- **SSL certificate problems**: May need to disable SSL verification temporarily or update certificates.

**Resources for Further Help:**

- Official Git documentation: [git-scm.com/doc](https://git-scm.com/doc)
- GitHub's Git guides: [docs.github.com/en/get-started](https://docs.github.com/en/get-started)

With Git properly installed and configured, you're ready to start tracking changes and collaborating on projects!

**📝 Core Git Commands**

```bash
git clone <repo_url>
git status
git add .
git commit -m "Your message"
git push origin main
git pull origin main
```

### Essential Git Commands

**1. Repository Management**

- `git init`: Creates a new Git repository in the current directory, adding a hidden .git folder to track changes.
- `git clone [url]`: Downloads a complete copy of an existing repository, including all files and history.
- `git remote`: Lists, adds, or removes connections to other repositories (like GitHub) for sharing code.

**2. Tracking Changes**

- `git status`: Shows which files are modified, staged, or untracked in your working directory.
- `git add [file]`: Adds changes from your working directory to the staging area, preparing them for commit.
- `git commit -m "message"`: Records staged changes to the repository with a descriptive message.
- `git diff`: Displays line-by-line changes between your working directory and the last commit.

**3. Branching & Merging**

- `git branch [name]`: Creates a new branch to develop features or fix bugs independently from the main codebase.
- `git checkout [branch]`/`git switch [branch]`: Switches your working directory to a different branch.
- `git merge [branch]`: Integrates changes from one branch into your current branch.
- Resolving merge conflicts: Manually editing files where Git can't automatically combine different changes.

**4. Remote Operations**

- `git fetch`: Downloads objects and refs from a remote repository without merging changes into your branches.
- `git pull`: Fetches changes from a remote repository and automatically merges them into your current branch.
- `git push`: Uploads your local commits to a remote repository, sharing your changes with others.
- `git pull origin main` fetches the latest changes from the `main` branch on GitHub and merges them into your local code.

[Day 9 - Set up Cursor and General Practice](https://www.notion.so/Day-9-Set-up-Cursor-and-General-Practice-1e4b8a917a9980c78f09ff398328daf7?pvs=21)

[Git Command Cheatsheet](https://www.notion.so/Git-Command-Cheatsheet-1d9b8a917a99806ebc7ed6934c3b547b?pvs=21)

![image (15)](https://github.com/user-attachments/assets/f0007400-45b0-4cfc-9d66-65bbcebd3bf0)

*Image Resource: https://dzone.com/articles/git-tutorial-commands-and-operations-in-git*

## Additional software engineering practice concepts

### ⚙️ CI/CD – *Continuous Integration & Continuous Deployment*

**Goal:** Automate building, testing, and deploying your app to reduce errors and speed up development.

🔹 **Continuous Integration (CI)**

- Automatically run tests when code is pushed to a shared repo (like GitHub).
- Ensures new code **doesn't break** the existing app.
- Common tools: **GitHub Actions, GitLab CI**

Think of this like a spell-checker that auto-checks your writing before you share it.

---

🔹 **Continuous Deployment (CD)**

- Automatically deploys your code to production **after it passes tests**.
- Can be:
    - **Continuous Delivery** (manual deploy after approval)
    - **Continuous Deployment** (fully automatic)

Think of this like hitting “publish” on a blog that instantly updates the live website after spell-check.

🔗 [CI/CD in 100 seconds](https://www.youtube.com/watch?v=scEDHsr3APg)

### 🕵️ Observability – *Understanding What’s Happening in Your App*

**Goal:** Know when something breaks, why it broke, and how to fix it.

🔸 1. **Logging**

- Records events (e.g., “User X sent request Y”)
- Helps debug when something goes wrong.

🔸 2. **Monitoring**

- Tracks system health (CPU, memory, API uptime)
- Real-time alerts if something fails.

🔸 3. **Tracing**

- Tracks **how a request flows** through your system (frontend → backend → DB)
- Useful in microservices or distributed AI pipelines.

---
