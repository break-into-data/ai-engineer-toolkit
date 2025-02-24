from typing import List, Optional
from pydantic import BaseModel, Field
import tempfile
import os
import asyncio
import logging
from openai import AsyncOpenAI
from firecrawl import FirecrawlApp
import PyPDF2

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------
# Data Models with Pydantic
# --------------------------------------------------------------

class ResumeExtraction(BaseModel):
    experience: List[str] = Field(description="List of work experiences")
    skills: List[str] = Field(description="List of skills")
    education: List[str] = Field(description="List of education details")
    contact_info: str = Field(description="Contact information")

class JobExtraction(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    requirements: List[str] = Field(description="Job requirements")
    description: str = Field(description="Job description")

class CoverLetter(BaseModel):
    content: str = Field(description="Generated cover letter text")

# --------------------------------------------------------------
# Step 2. Create 3 functions 
# --------------------------------------------------------------

async def extract_resume_info(client: AsyncOpenAI, pdf_text: str) -> Optional[ResumeExtraction]:
    """First LLM call: Extract structured information from resume"""
    try:
        completion = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a resume parser. Return ONLY a JSON object with this structure:
                    {
                        "experience": ["list of work experiences"],
                        "skills": ["list of technical and soft skills"],
                        "education": ["list of education details"],
                        "contact_info": "full contact information"
                    }
                    IMPORTANT: Return ONLY valid JSON, no other text."""
                },
                {
                    "role": "user",
                    "content": pdf_text
                }
            ]
        )
        response_text = completion.choices[0].message.content.strip()
        logger.info(f"Resume LLM Response: {response_text}")
        return ResumeExtraction.model_validate_json(response_text)
    except Exception as e:
        logger.error(f"Resume extraction failed: {str(e)}")
        logger.error(f"Response was: {response_text if 'response_text' in locals() else 'No response'}")
        return None

async def extract_job_info(client: AsyncOpenAI, job_content: str) -> Optional[JobExtraction]:
    """Second LLM call: Extract structured information from job posting"""
    try:
        # Convert job_content to string and handle potential None
        job_text = str(job_content) if job_content is not None else ""
        logger.info(f"Job content type: {type(job_text)}")
        
        completion = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a job posting parser. Return ONLY a JSON object with this structure:
                    {
                        "title": "exact job title",
                        "company": "company name",
                        "requirements": ["list of key requirements"],
                        "description": "brief job description"
                    }
                    IMPORTANT: Return ONLY valid JSON, no other text."""
                },
                {
                    "role": "user",
                    "content": job_text
                }
            ]
        )
        response_text = completion.choices[0].message.content.strip()
        logger.info(f"Job LLM Response: {response_text}")
        return JobExtraction.model_validate_json(response_text)
    except Exception as e:
        logger.error(f"Job info extraction failed: {str(e)}")
        logger.error(f"Job content was: {job_text if 'job_text' in locals() else 'No content'}")
        return None

async def generate_cover_letter(
    client: AsyncOpenAI, 
    resume_info: ResumeExtraction, 
    job_info: JobExtraction
) -> Optional[str]:
    """Third LLM call: Generate the cover letter using the results from previous async calls"""
    try:
        completion = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Write a compelling cover letter following these guidelines:
                    1. Start with a strong hook about the company/role
                    2. Focus on relevant achievements matching job requirements
                    3. Use specific metrics from past experience
                    4. Keep it concise (300-400 words)
                    5. End with a confident call to action"""
                },
                {
                    "role": "user",
                    "content": f"Resume: {resume_info.model_dump()}\nJob: {job_info.model_dump()}"
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Cover letter generation failed: {str(e)}")
        return None

# --------------------------------------------------------------
# Main Processing Function
# --------------------------------------------------------------

async def process_cover_letter_request(
    pdf_file, 
    job_url: str, 
    openai_client: AsyncOpenAI, 
    firecrawl_client: FirecrawlApp
) -> Optional[str]:
    """Main async function that chains all the processing steps together"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_file.read())
            temp_path = temp_file.name

        # Extract text from PDF
        with open(temp_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_text = ' '.join(page.extract_text() for page in pdf_reader.pages)
            logger.info(f"Extracted PDF text length: {len(pdf_text)}")

        # Get job content
        try:
            job_content = firecrawl_client.scrape_url(job_url)
            if not isinstance(job_content, str):
                job_content = str(job_content)
            logger.info(f"Job content type after conversion: {type(job_content)}")
        except Exception as e:
            logger.error(f"Error scraping job URL: {str(e)}")
            return None

        # Process resume and job info in parallel
        resume_info, job_info = await asyncio.gather(
            extract_resume_info(openai_client, pdf_text),
            extract_job_info(openai_client, job_content)
        )

        if not resume_info or not job_info:
            logger.error("Failed to extract either resume or job information")
            return None

        # Generate cover letter
        cover_letter = await generate_cover_letter(openai_client, resume_info, job_info)
        
        if not cover_letter:
            return None

        return cover_letter

    except Exception as e:
        logger.error(f"Error processing cover letter request: {str(e)}")
        return None
    finally:
        if 'temp_path' in locals():
            os.unlink(temp_path)


