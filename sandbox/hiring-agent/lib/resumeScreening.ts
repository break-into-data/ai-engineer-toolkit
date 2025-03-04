import { OpenAI } from "openai"
import * as pdfjs from "pdfjs-dist"

// Load the worker from the CDN
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`

async function callLLM(messages: any[], responseFormat: any, apiKey: string) {
  const openai = new OpenAI({ apiKey })

  const params: any = {
    model: "gpt-4-turbo-preview",
    messages: messages,
  }

  if (responseFormat) {
    params.response_format = { type: "json_object" }
  }

  const response = await openai.chat.completions.create(params)

  return response.choices[0].message.content
}

export async function ingestInputs(jobDescription: string, resumeFiles: File[]) {
  let jobDescText = jobDescription

  if (jobDescription.startsWith("http")) {
    try {
      const response = await fetch(jobDescription)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      jobDescText = await response.text()
    } catch (error) {
      console.error("Error fetching job description:", error)
      throw new Error(`Failed to fetch the job description: ${error}`)
    }
  }

  const resumes = resumeFiles.map((file) => file.name)
  return { job_description: jobDescText, resumes }
}

export async function parseJobDescription(jobText: string, apiKey: string) {
  const messages = [
    {
      role: "system",
      content:
        "You are an assistant that extracts key job description information from text. Return only the job details in valid JSON format using the keys: title, company, location, requirements (as a list), responsibilities (as a list), benefits (as a list), and experience.",
    },
    {
      role: "user",
      content: `Extract the key job information from the text below. Return only valid JSON with the following keys: title, company, location, requirements, responsibilities, benefits, experience. Do not include any extraneous information.\n\nJob description:\n${jobText}`,
    },
  ]

  try {
    const llmOutput = await callLLM(messages, true, apiKey)
    return JSON.parse(llmOutput)
  } catch (error) {
    console.error("Error parsing job description:", error)
    throw new Error(`Error parsing job description: ${error}`)
  }
}

export async function parseResumes(resumeFiles: File[], apiKey: string) {
  const parsedResumes = []

  for (const resume of resumeFiles) {
    const arrayBuffer = await resume.arrayBuffer()
    const pdf = await pdfjs.getDocument({ data: arrayBuffer }).promise
    let pdfText = ""

    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i)
      const content = await page.getTextContent()
      pdfText += content.items.map((item: any) => item.str).join(" ")
    }

    const messages = [
      {
        role: "system",
        content:
          "You are an assistant that extracts candidate resume details. Extract only the information following this JSON schema: { name: string, work_experiences: string[], location: string, skills: string[], education: string[], summary?: string, certifications?: string[], languages?: string[] }",
      },
      {
        role: "user",
        content: `Extract resume details from the following resume text:\n\n${pdfText}`,
      },
    ]

    try {
      const llmResponse = await callLLM(messages, true, apiKey)
      const parsedResume = JSON.parse(llmResponse)
      parsedResumes.push(parsedResume)
    } catch (error) {
      console.error("Error parsing resume:", error)
      parsedResumes.push({ error: `Failed to parse resume: ${error}` })
    }
  }

  return { parsed_resumes: parsedResumes }
}

export async function scoreCandidates(parsedRequirements: any, parsedResumes: any, apiKey: string) {
  const candidateScores = []

  const jobDescriptionText = JSON.stringify(parsedRequirements)
  const resumeList = parsedResumes.parsed_resumes

  for (const candidate of resumeList) {
    const messages = [
      {
        role: "system",
        content:
          "You are an unbiased hiring manager. Compare the following job description with the candidate's resume and provide scores (0-100) for relevance, experience, and skills. Also compute an overall score that reflects the candidate's fit and provide a comment explaining your evaluation. Return only valid JSON using the following schema: { name: string, relevance: number, experience: number, skills: number, overall: number, comment: string }",
      },
      {
        role: "user",
        content: `Job Description:\n${jobDescriptionText}\n\nCandidate Resume:\n${JSON.stringify(candidate)}`,
      },
    ]

    try {
      const llmResponse = await callLLM(messages, true, apiKey)
      const scoreData = JSON.parse(llmResponse)
      scoreData.resume = candidate
      candidateScores.push(scoreData)
    } catch (error) {
      console.error("Error scoring candidate:", error)
      candidateScores.push({
        name: candidate.name || "Unknown",
        relevance: 0,
        experience: 0,
        skills: 0,
        overall: 0,
        comment: `Error during evaluation: ${error}`,
      })
    }
  }

  return candidateScores
}

export function rankCandidates(candidateScores: any[]) {
  return candidateScores
    .map((candidate) => ({
      ...candidate,
      avg_score: (candidate.relevance + candidate.experience + candidate.skills + candidate.overall) / 4.0,
    }))
    .sort((a, b) => b.avg_score - a.avg_score)
}

export async function generateEmailTemplates(
  rankedCandidates: any[],
  jobDescription: any,
  topX: number,
  apiKey: string,
) {
  const invitations = []
  const rejections = []

  for (let idx = 0; idx < rankedCandidates.length; idx++) {
    const candidate = rankedCandidates[idx]
    const candidateName = candidate.name || "Candidate"

    const messages = [
      {
        role: "system",
        content:
          "You are an unbiased HR professional. Your task is to craft clear, concise, and professional email responses to candidates based on the job description, the candidate's resume details, and evaluation scores. Return only the email body as plain text.",
      },
      {
        role: "user",
        content: `Job Description (structured):\n${JSON.stringify(jobDescription, null, 2)}\n\nCandidate Evaluation (structured):\n${JSON.stringify(candidate, null, 2)}\n\n`,
      },
    ]

    if (idx < topX) {
      messages.push({
        role: "assistant",
        content:
          "Please create an invitation email inviting the candidate for a quick call. The email should be friendly, professional, and include a scheduling request.",
      })
    } else {
      messages.push({
        role: "assistant",
        content:
          "Please create a polite rejection email. Include constructive feedback and key suggestions for improvement based on the candidate's evaluation.",
      })
    }

    try {
      const emailBody = await callLLM(messages, false, apiKey)
      const emailTemplate = { name: candidateName, email_body: emailBody }

      if (idx < topX) {
        invitations.push(emailTemplate)
      } else {
        rejections.push(emailTemplate)
      }
    } catch (error) {
      console.error("Error generating email:", error)
      const errorTemplate = { name: candidateName, email_body: `Error generating email: ${error}` }

      if (idx < topX) {
        invitations.push(errorTemplate)
      } else {
        rejections.push(errorTemplate)
      }
    }
  }

  return { invitations, rejections }
}

