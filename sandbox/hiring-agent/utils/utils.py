# utils/utils.py
import os
from typing import List, Dict, Any
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import json
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio

load_dotenv()
import tempfile
import PyPDF2


app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)


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


async def ingest_inputs(
    job_description: str, resume_files: List[Any]
) -> Dict[str, Any]:
    """
    Ingests the job description and resume files.

    Parameters:
        job_description (str): The job description text or URL.
        resume_files (List[Any]): List of uploaded resume files.

    Returns:
        dict: A dictionary with two keys:
              - "job_description": The processed job description (in markdown).
              - "resumes": A list of resume file names.
    """
    # Determine if job_description is a URL.
    if job_description.startswith("http"):
        try:
            result = app.scrape_url(job_description, params={"formats": ["markdown"]})
            # Check if markdown data is present in the result.
            if not result or "markdown" not in result:
                raise ValueError("Scraping did not return markdown data.")
            job_desc_text = result.get("markdown", "")
        except Exception as e:
            raise Exception(f"Failed to scrape the job description URL: {e}")
    else:
        job_desc_text = job_description
    resumes = [file.name for file in resume_files]
    return {"job_description": job_desc_text, "resumes": resumes}


def call_llm(messages: list, response_fromat: None) -> str:
    """
    Calls the OpenAI GPT-4 model with the provided prompt and returns the response text.

    Parameters:
        prompt (str): The prompt to send to the LLM.

    Returns:
        str: The LLM's response.
    """

    params = {"model": "gpt-4o-2024-08-06", "messages": messages}

    if response_fromat:
        params["response_format"] = response_fromat

    response = openai_client.beta.chat.completions.parse(**params)

    return response.choices[0].message.content


async def parse_job_description(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses the job description to extract key requirements in a structured format.

    This function takes the ingested job description (which might be scraped from a URL)
    and uses an LLM (GPT-4) to extract and return only the essential job details.
    Extraneous content from the scraped page is removed.

    Parameters:
        data (dict): Dictionary containing the job description details, with a key "job_description".

    Returns:
        dict: A dictionary with the structured job description containing keys:
              "title", "company", "location", "requirements", "responsibilities", "benefits", and "experience".

    Raises:
        Exception: If the LLM call fails or the returned JSON cannot be parsed.
    """
    job_text = data.get("job_description", "")
    if not job_text:
        raise ValueError("No job description text provided.")

    # Build the prompt for the LLM
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
        llm_output = call_llm(messages, response_fromat=JobDescription)
        # Parse the JSON returned by the LLM
        structured_jd = json.loads(llm_output)
    except Exception as e:
        raise Exception(f"Error parsing job description: {e}")

    return structured_jd


async def parse_resumes(resume_files: List[Any]) -> Dict[str, Any]:
    """
    Parses resume files to extract candidate information.

    This function reads each uploaded resume file and uses an LLM (via the call_llm helper)
    to extract candidate details. The LLM is asked to return only valid JSON following the
    schema defined by the Resume Pydantic model. The expected JSON should include keys such as:

        {
            "name": string,
            "work_experiences": list[string],
            "location": string,
            "skills": list[string],
            "education": list[string],
            "summary": string (optional),
            "certifications": list[string] (optional),
            "languages": list[string] (optional)
        }

    Parameters:
        resume_files (List[Any]): List of uploaded resume file objects (e.g., from Streamlit's file uploader).

    Returns:
        dict: A dictionary with a key "parsed_resumes" that is a list of parsed resume details.

    Raises:
        Exception: If any LLM call or JSON parsing fails.
    """
    parsed_resumes = []
    for resume in resume_files:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(resume.read())
            temp_path = temp_file.name

        # Extract text from PDF
        with open(temp_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_text = " ".join(page.extract_text() for page in pdf_reader.pages)
        # Build messages for the LLM.
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts candidate resume details. "
                    "Extract only the information following this JSON schema: "
                ),
            },
            {
                "role": "user",
                "content": f"Extract resume details from the following resume text:\n\n{pdf_text}",
            },
        ]

        try:
            # Call the LLM to process the resume text.
            # Pass the JSON schema (as a string) to instruct the LLM on the expected format.
            llm_response = call_llm(messages, response_fromat=Resume)
            # Parse the JSON response from the LLM.
            parsed_resume = json.loads(llm_response)
        except Exception as e:
            parsed_resume = {"error": f"Failed to parse resume using LLM: {e}"}

        parsed_resumes.append(parsed_resume)
    return {"parsed_resumes": parsed_resumes}


async def score_candidates(
    parsed_requirements: Dict[str, Any], parsed_resumes: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Scores candidates based on the parsed job description and resume data.
    Parameters:
        parsed_requirements (dict): Parsed job description data.
            Expected to have a key "parsed_requirements" with the job description details.
        parsed_resumes (dict): Parsed resume data.
            Expected to have a key "parsed_resumes" which is a list of candidate details.

    Returns:
        list: A list of dictionaries with candidate scores as per the CandidateScore model.

    Raises:
        Exception: If any LLM call or JSON parsing fails.
    """
    candidate_scores = []

    job_description_text = json.dumps(parsed_requirements)
    resume_list = parsed_resumes.get("parsed_resumes", [])
    for candidate in resume_list:
        # Build messages for the LLM.
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an unbiased hiring manager. Compare the following job description with the candidate's resume and provide "
                    "scores (0-100) for relevance, experience, and skills. Also compute an overall score that reflects the candidate's fit "
                    "and provide a comment explaining your evaluation. Return only valid JSON using the following schema: "
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
            llm_response = call_llm(messages, response_fromat=CandidateScore)
            score_data = json.loads(llm_response)
            score_data["resume"] = candidate
        except Exception as e:
            # In case of an error, record a default score with error comment.
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


def rank_candidates(candidate_scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ranks candidates based on the average of their overall scores.

    For each candidate, this function calculates the average score from the keys:
    "relevance", "experience", "skills", and "overall". It adds a new key "avg_score"
    to each candidate's dictionary and then returns the sorted list in descending order.

    Parameters:
        candidate_scores (list): List of candidate score dictionaries.

    Returns:
        list: Sorted list of candidate scores in descending order based on avg_score.
    """
    for candidate in candidate_scores:
        # Compute the average of the relevant scores.
        relevance = candidate.get("relevance", 0)
        experience = candidate.get("experience", 0)
        skills = candidate.get("skills", 0)
        overall = candidate.get("overall", 0)
        candidate["avg_score"] = (relevance + experience + skills + overall) / 4.0

    # Return the sorted list of candidates based on avg_score.
    return sorted(
        candidate_scores, key=lambda candidate: candidate["avg_score"], reverse=True
    )


async def generate_email_templates(
    ranked_candidates: List[Dict[str, Any]], job_description: Dict[str, Any], top_x: int
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generates custom email templates using an LLM for each candidate.
    Parameters:
        ranked_candidates (list): List of candidate score dictionaries.
        job_description (dict): The structured job description.
        top_x (int): Number of top candidates to invite for a call.

    Returns:
        dict: A dictionary with two keys:
              - "invitations": A list of dictionaries with candidate "name" and "email_body" for invitations.
              - "rejections": A list of dictionaries with candidate "name" and "email_body" for rejections.

    Raises:
        Exception: If the LLM call fails for any candidate.
    """
    invitations = []
    rejections = []

    for idx, candidate in enumerate(ranked_candidates):
        candidate_name = candidate.get("name", "Candidate")

        # Build the base messages for the LLM.
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an unbiased HR professional. Your task is to craft clear, concise, "
                    "and professional email responses to candidates based on the job description, "
                    "the candidate's resume details, and evaluation scores. "
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

        # Append specific instructions based on candidate ranking.
        if idx < top_x:
            messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "Please create an invitation email inviting the candidate for a quick call. "
                        "The email should be friendly, professional, and include a scheduling request."
                    ),
                }
            )
        else:
            messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "Please create a polite rejection email. Include constructive feedback and key "
                        "suggestions for improvement based on the candidate's evaluation."
                    ),
                }
            )

        try:
            email_body = call_llm(messages, response_fromat=None)
        except Exception as e:
            email_body = f"Error generating email: {e}"

        email_template = {"name": candidate_name, "email_body": email_body}
        if idx < top_x:
            invitations.append(email_template)
        else:
            rejections.append(email_template)

    return {"invitations": invitations, "rejections": rejections}
