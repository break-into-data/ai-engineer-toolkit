# An AI agent, that helps with resume screening

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-00A67E.svg)](https://openai.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a Streamlit app that uses an AI agent to process a job description and candidate resumes, score the candidates, and generate custom email templates.

![Ai Agent](images/arch-diagram.png "Title")

## Setup

### 1. Create a Virtual Environment

Open a terminal and navigate to the project directory. Then run:

```bash
# Create a virtual environment in the "venv" folder
python -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate
```

### 2. Install Requirements

Install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory and add your API keys:

```dotenv
# .env file
FIRECRAWL_API_KEY=fc-YOUR_FIRECRAWL_API_KEY
OPENAI_API_KEY=sk-YOUR_OPENAI_API_KEY
```

### 4. Run the Streamlit App

Run the app with the following command:

```bash
streamlit run app.py
```

Your app should now be running locally.

### How It Works

![flowchart](images/hiring-process-flowchart.png "Flowchart")


**User Input**

- Job Description: Enter text or provide a URL.
- Resumes: Upload PDF/Word files.

**Ingestion**

- Inputs are read and processed.
- Job description URLs are scraped for content.

**Parsing**

- The job description is analyzed by an LLM (GPT-4) to extract essential details.
- Resumes are processed to extract candidate profiles.

**Scoring and Ranking**

- Candidates are scored on relevance, experience, and skills.
- An average score is computed, and candidates are sorted in descending order.


**Email Generation**

- Custom email templates are created for top candidates and for rejections.


This pipeline uses Streamlit for the interface and LLM-powered functions for text extraction, evaluation, and communication, automating the resume screening process.