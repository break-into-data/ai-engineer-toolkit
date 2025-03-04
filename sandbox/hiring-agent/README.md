[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.78.0-blue.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-13.0+-000000.svg)](https://nextjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-00A67E.svg)](https://openai.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Resume Screening Application

This application helps recruiters screen and rank resumes based on job descriptions using AI.


![Ai Agent](images/arch-diagram.png "Title")




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

- Custom email is generated based on if you want to accept or reject the candidate



## Setup Instructions

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000

### Backend Setup

```bash
# Create and activate virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn main:app --reload
```

The backend API will be available at http://localhost:8000

## Environment Variables

Create a `.env` file in the `backend` directory with the following keys:

```
OPENAI_API_KEY=your_openai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

## Features

- Upload multiple resumes (PDF)
- Enter or paste job descriptions
- Automatic parsing of resumes and job descriptions
- AI-powered candidate ranking
- Generate personalized email templates for candidates

## Technologies

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, OpenAI API
- **Tools**: PDF parsing, AI text analysis



