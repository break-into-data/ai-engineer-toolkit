from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from firecrawl import FirecrawlApp
import asyncio
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
import io
import base64

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
firecrawl_app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

def call_llm(messages: list, response_format: Any) -> str:
    params = {"model": "gpt-4o-2024-08-06", "messages": messages}
    if response_format:
        params["response_format"] = response_format

    response = openai_client.beta.chat.completions.parse(**params)
    return response.choices[0].message.content

class JobDescription(BaseModel):
    text: str

class ResumeFile(BaseModel):
    filename: str
    content: str

class IngestInputsRequest(BaseModel):
    job_description: JobDescription
    resume_files: List[ResumeFile]


class CandidateScore(BaseModel):
    name: str = Field(..., description="Candidate's name")
    relevance: int = Field(
        ...,
        description="How relevant the candidate's resume is to the job description (0-100)",
    )
    experience: int = Field(
        ..., description="Candidate's match in terms of work experience (0-100)"
    )
    skills: int = Field(..., description="Candidate's match based on skills (0-100)")
    overall: int = Field(..., description="Overall score (0-100)")
    comment: str = Field(
        ..., description="A cbrief omment explaining the rationale behind the scores"
    )


class Resume(BaseModel):
    name: str = Field(..., description="Candidate's full name")
    work_experiences: List[str] = Field(..., description="List of work experiences")
    location: str = Field(..., description="Candidate's location")
    skills: List[str] = Field(..., description="List of candidate's skills")
    education: List[str] = Field(..., description="Educational background")
    summary: Optional[str] = Field(
        None, description="A short summary or objective statement"
    )
    certifications: Optional[List[str]] = Field(
        None, description="List of certifications"
    )
    languages: Optional[List[str]] = Field(
        None, description="Languages spoken by the candidate"
    )


class JobDescription(BaseModel):
    title: str
    company: str
    location: str
    requirements: list[str]
    responsibilities: list[str]

@app.post("/ingest_inputs")
async def ingest_inputs(request: IngestInputsRequest):
    job_desc_text = request.job_description.text

    # If the job description is a URL, scrape it for markdown data
    if job_desc_text.startswith("http"):
        try:
            result = firecrawl_app.scrape_url(job_desc_text, params={"formats": ["markdown"]})
            if not result or "markdown" not in result:
                raise ValueError("Scraping did not return markdown data.")
            job_desc_text = result.get("markdown", "")
        except Exception as e:
            raise Exception(f"Failed to scrape the job description URL: {e}")

    resumes = []
    for file in request.resume_files:
        # Remove the Base64 prefix if it exists
        base64_str = file.content
        if base64_str.startswith("data:"):
            base64_str = base64_str.split(",")[1]
        try:
            pdf_bytes = base64.b64decode(base64_str)
        except Exception as e:
            resumes.append({
                "filename": file.filename,
                "error": f"Base64 decoding error: {e}",
            })
            continue

        # Use a BytesIO stream instead of writing to disk
        pdf_io = io.BytesIO(pdf_bytes)
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_io)
            pdf_text = " ".join(page.extract_text() or "" for page in pdf_reader.pages)
        except Exception as e:
            pdf_text = f"Error processing PDF: {e}"
        resumes.append({
            "filename": file.filename,
            "text": pdf_text,
        })
    return {"job_description": job_desc_text, "resumes": resumes}

@app.post("/parse_job_description")
async def parse_job_description(data: dict):
    job_text = data.get("job_description", "")
    if not job_text:
        raise ValueError("No job description text provided.")

    prompt = (
        "Extract the key job information from the text below. Return only valid JSON "
        "with the following keys: title, company, location, requirements, responsibilities, benefits, experience. "
        "Do not include any extraneous information.\n\n"
        "Job description:\n" + job_text
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that extracts key job description information from text. "
                "Return only the job details in valid JSON format using the keys: "
                "title, company, location, requirements (as a list), responsibilities (as a list), "
                "benefits (as a list), and experience."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    try:
        llm_output = call_llm(messages, response_format=JobDescription)
        structured_jd = json.loads(llm_output)
    except Exception as e:
        raise Exception(f"Error parsing job description: {e}")

    return structured_jd

@app.post("/parse_resumes")
async def parse_resumes(data: dict):
    resume_files = data.get("resume_files", [])
    parsed_resumes = []

    for resume in resume_files:
        
        pdf_text = resume['text']
        print(pdf_text)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts candidate resume details. "
                    "Extract only the information following this JSON schema: "
                    "{ name: string, work_experiences: string[], location: string, "
                    "skills: string[], education: string[], summary?: string, "
                    "certifications?: string[], languages?: string[] }"
                ),
            },
            {
                "role": "user",
                "content": f"Extract resume details from the following resume text:\n\n{pdf_text}",
            },
        ]

        try:
            llm_response = call_llm(messages, response_format=Resume)
            parsed_resume = json.loads(llm_response)
        except Exception as e:
            parsed_resume = {"error": f"Failed to parse resume using LLM: {e}"}

        parsed_resumes.append(parsed_resume)

    return {"parsed_resumes": parsed_resumes}

@app.post("/score_candidates")
async def score_candidates(data: dict):
    parsed_requirements = data.get("parsed_requirements", {})
    parsed_resumes = data.get("parsed_resumes", {})
    candidate_scores = []

    job_description_text = json.dumps(parsed_requirements)
    resume_list = parsed_resumes.get("parsed_resumes", [])

    for candidate in resume_list:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an unbiased hiring manager. Compare the following job description with the candidate's resume and provide "
                    "scores (0-100) for relevance, experience, and skills. Also compute an overall score that reflects the candidate's fit "
                    "and provide a comment explaining your evaluation. Return only valid JSON using the following schema: "
                    "{ name: string, relevance: number, experience: number, skills: number, overall: number, comment: string }"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Job Description:\n{job_description_text}\n\n"
                    f"Candidate Resume:\n{json.dumps(candidate)}"
                ),
            },
        ]

        try:
            llm_response = call_llm(messages, response_format=CandidateScore)
            score_data = json.loads(llm_response)
            score_data["resume"] = candidate
        except Exception as e:
            score_data = {
                "name": candidate.get("name", "Unknown"),
                "relevance": 0,
                "experience": 0,
                "skills": 0,
                "overall": 0,
                "comment": f"Error during evaluation: {e}",
            }

        candidate_scores.append(score_data)

    return candidate_scores

@app.post("/rank_candidates")
async def rank_candidates(data: dict):
    candidate_scores = data.get("candidate_scores", [])
    for candidate in candidate_scores:
        relevance = candidate.get("relevance", 0)
        experience = candidate.get("experience", 0)
        skills = candidate.get("skills", 0)
        overall = candidate.get("overall", 0)
        candidate["avg_score"] = (relevance + experience + skills + overall) / 4.0

    return sorted(candidate_scores, key=lambda candidate: candidate["avg_score"], reverse=True)

@app.post("/generate_email_templates")
async def generate_email_templates(data: dict):
    candidate = data.get("candidate")
    job_description = data.get("job_description")
    email_type = data.get("email_type")
    
    if not candidate or not job_description or not email_type:
        raise HTTPException(
            status_code=400,
            detail="Missing one or more required fields: candidate, job_description, email_type"
        )

    candidate_name = candidate.get("name", "Candidate")
    
    # Build the messages for the LLM based on the email type
    messages = [
        {
            "role": "system",
            "content": (
                "You are an unbiased HR professional. Your task is to craft a clear, concise, and "
                "professional email response based on the provided job description and candidate evaluation. "
                "Return only the email body as plain text."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Job Description (structured):\n{json.dumps(job_description, indent=2)}\n\n"
                f"Candidate Evaluation (structured):\n{json.dumps(candidate, indent=2)}\n\n"
            ),
        },
    ]

    if email_type == "accept":
        messages.append(
            {
                "role": "assistant",
                "content": (
                    "Please create an invitation email inviting the candidate for a quick call. "
                    "The email should be friendly, professional, and include a scheduling request."
                ),
            }
        )
    elif email_type == "reject":
        messages.append(
            {
                "role": "assistant",
                "content": (
                    "Please create a polite rejection email. Include constructive feedback and key "
                    "suggestions for improvement based on the candidate's evaluation."
                ),
            }
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid email_type. Must be either 'accept' or 'reject'."
        )

    try:
        email_body = call_llm(messages, response_format=None)
    except Exception as e:
        raise Exception(f"Error generating email: {e}")

    return {"email_body": email_body}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

