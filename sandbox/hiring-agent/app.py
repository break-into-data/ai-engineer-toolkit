# main.py
import streamlit as st
import pandas as pd
from utils.utils import (
    ingest_inputs,
    parse_job_description,
    parse_resumes,
    score_candidates,
    rank_candidates,
    generate_email_templates,
)
import asyncio


# Main App Title
st.title("Resume Screening Agent")

# Input section for job description
st.header("Job Description Input")
job_description = st.text_area("Paste the job description or URL", height=150)

# Input section for candidate resumes
st.header("Candidate Resumes")
resume_files = st.file_uploader(
    "Upload resume files (PDF/Word)",
    type=["pdf", "docx", "doc"],
    accept_multiple_files=True,
)

st.header("Candidates to Select")
num_candidates = st.slider(
    "Select the number of candidates to invite for an interview", 1, 4, 2
)


# Button to trigger the agent
if st.button("Run Agent"):
    if not job_description:
        st.error("Please provide a job description or URL.")
    elif not resume_files:
        st.error("Please upload at least one resume file.")
    else:
        st.markdown("### Your AI Agent is now processing your inputs...")
        status_text = st.empty()  # placeholder for status updates

        # Step 1: processing resumes
        with st.spinner("Step 1: Processing Inputs..."):
            # raw_data = ingest_inputs(job_description, resume_files)
            raw_data = asyncio.run(ingest_inputs(job_description, resume_files))
            status_text.text("Step 1 complete: Inputs processed.")
            with st.expander("View Processed Inputs", expanded=False):
                st.json(raw_data)

        # Step 2: processing Job description
        with st.spinner("Step 2: Processing Job Description & Resume..."):
            parsed_requirements = asyncio.run(parse_job_description(raw_data))
            parsed_resumes = asyncio.run(parse_resumes(resume_files))
            status_text.text("Step 2 complete: Job description & Resume processed.")
            with st.expander("View Parsed Job Description", expanded=False):
                st.json(parsed_requirements)
            with st.expander("View processed Resume", expanded=False):
                st.json(parsed_resumes)

        # Step 3: Score candidates based on the parsed data
        with st.spinner("Step 3: Scoring candidates..."):
            status_text.text("Step 3: Scoring candidates...")
            candidate_scores = asyncio.run(
                score_candidates(parsed_requirements, parsed_resumes)
            )
            status_text.text("Step 3 complete: Candidates scored.")
            with st.expander("View Resume Summaries", expanded=False):
                st.json(candidate_scores)

        # Step 4: Rank the candidates
        with st.spinner("Step 4: Ranking candidates..."):
            status_text.text("Step 4: Ranking candidates...")
            ranked_candidates = rank_candidates(candidate_scores)
            status_text.text("Step 4 complete: Candidates ranked.")
            with st.expander("View Ranked Candidates", expanded=False):
                st.json(ranked_candidates)

        # Step 5: Generate email templates for top candidates and others
        with st.spinner("Step 5: Generating email templates..."):
            status_text.text("Step 5: Generating email templates...")
            # 'num_candidates' is assumed to come from the frontend (e.g., top X candidates)
            email_templates = asyncio.run(
                generate_email_templates(
                    ranked_candidates, parsed_requirements, num_candidates
                )
            )
            status_text.text("Step 5 complete: Email templates generated.")
            with st.expander("View Email Templates", expanded=False):
                st.json(email_templates)

        # Final update
        status_text.text("Agent processing complete! Your results are ready.")
