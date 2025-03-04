import { NextResponse } from "next/server"
import { processJobDescription } from "@/lib/jobDescriptionProcessor"
import { processResumes } from "@/lib/resumeProcessor"
import { scoreResumes } from "@/lib/resumeScorer"
import { rankCandidates } from "@/lib/candidateRanker"

export async function POST(req: Request) {
  try {
    const { jobDescription, resumes } = await req.json()

    // Step 1: Process Job Description
    const jobDescriptionOutput = await processJobDescription(jobDescription)

    // Step 2: Process Resumes
    const processedResumes = await processResumes(resumes)

    // Step 3: Score Resumes
    const scoredResumes = await scoreResumes(processedResumes, jobDescriptionOutput)

    // Step 4: Rank Candidates
    const rankedCandidates = await rankCandidates(scoredResumes)

    return NextResponse.json({
      success: true,
      data: {
        jobDescriptionOutput,
        processedResumes,
        scoredResumes,
        rankedCandidates,
      },
    })
  } catch (error) {
    console.error("Error in resume screening process:", error)
    return NextResponse.json(
      { success: false, error: "An error occurred during the screening process" },
      { status: 500 },
    )
  }
}

