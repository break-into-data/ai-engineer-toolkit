"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { FileUploader } from "@/components/file-uploader"
import { ProgressTracker } from "@/components/progress-tracker"
import { ResultsTable } from "@/components/results-table"
import { EmailModal } from "@/components/email-modal"

// Utility to convert a file to a Base64 string
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
}



export default function ResumeScreeningApp() {
  const [jobDescription, setJobDescription] = useState("")
  const [jobUrl, setJobUrl] = useState("")
  const [files, setFiles] = useState<File[]>([])
  const [isScreening, setIsScreening] = useState(false)
  const [currentStage, setCurrentStage] = useState(0)
  const [results, setResults] = useState<any[]>([])
  const [emailModalOpen, setEmailModalOpen] = useState(false)
  const [emailType, setEmailType] = useState<"accept" | "reject">("accept")
  const [selectedCandidate, setSelectedCandidate] = useState<any>(null)
  const [emailContent, setEmailContent] = useState("")
  const [stepOutputs, setStepOutputs] = useState<Record<number, any>>({})
  const [expandedStep, setExpandedStep] = useState<number | null>(null)
  const [isEmailLoading, setIsEmailLoading] = useState(false)

  /**
   * Screens resumes by calling the resume screening API steps in order and updates the UI state accordingly.
   *
   * This function is responsible for calling the API endpoints in the correct order and updating the UI state.
   * It does not perform any actual resume screening logic.
   *
   * The function first ingests the job description and resume files, then parses the job description and
   * resumes, scores the candidates, ranks the candidates, and finally generates email templates.
   *
   * If any step fails, an error is logged to the console and an alert is shown to the user.
   *
   * The function takes no arguments and returns no value.
   */
  const handleScreenResumes = async () => {
    setIsScreening(true)
    setCurrentStage(0)
    setResults([])
    setStepOutputs({})
    setExpandedStep(null)

    try {
      // Step 1: Ingest inputs
      const ingestData = {
        job_description: { text: jobDescription || jobUrl },
        resume_files: await Promise.all(
          files.map(async (file) => ({
            filename: file.name,
            content: await fileToBase64(file), // Base64 encoded string
          }))
        ),
      }
      
      const ingestResponse = await fetch("http://localhost:8000/ingest_inputs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(ingestData),
      })
      const ingestResult = await ingestResponse.json()
      setStepOutputs((prev) => ({ ...prev, 0: ingestResult }))
      setCurrentStage(1)

      // Step 2: Parse job description
      const parseJobResponse = await fetch("http://localhost:8000/parse_job_description", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: ingestResult.job_description }),
      })
      const parsedJobDescription = await parseJobResponse.json()
      setStepOutputs((prev) => ({ ...prev, 1: parsedJobDescription }))
      setCurrentStage(2)

      // Step 3: Parse resumes
      const parseResumesResponse = await fetch("http://localhost:8000/parse_resumes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_files: ingestResult.resumes }),
      })
      const parsedResumes = await parseResumesResponse.json()
      setStepOutputs((prev) => ({ ...prev, 2: parsedResumes }))
      setCurrentStage(3)

      // Step 4: Score candidates
      const scoreCandidatesResponse = await fetch("http://localhost:8000/score_candidates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          parsed_requirements: parsedJobDescription,
          parsed_resumes: parsedResumes,
        }),
      })
      const candidateScores = await scoreCandidatesResponse.json()
      setStepOutputs((prev) => ({ ...prev, 3: candidateScores }))
      setCurrentStage(4)

      // Step 5: Rank candidates
      const rankCandidatesResponse = await fetch("http://localhost:8000/rank_candidates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ candidate_scores: candidateScores }),
      })
      const rankedCandidates = await rankCandidatesResponse.json()
      setStepOutputs((prev) => ({ ...prev, 4: rankedCandidates }))
      setCurrentStage(5)

      // // Step 6: Generate email templates
      // const generateEmailsResponse = await fetch("http://localhost:8000/generate_email_templates", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({
      //     ranked_candidates: rankedCandidates,
      //     job_description: parsedJobDescription,
      //     top_x: 3,
      //   }),
      // })
      // const emailTemplates = await generateEmailsResponse.json()
      // setStepOutputs((prev) => ({ ...prev, 5: emailTemplates }))

      setResults(rankedCandidates)
    } catch (error) {
      console.error("Error screening resumes:", error)
      alert(`Error screening resumes: ${error}`)
    } finally {
      setIsScreening(false)
    }
  }

  const handleScreenResumesAndScroll = async () => {
    await handleScreenResumes();
    // console.log("scrolling")
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });
  };
  
  const toggleExpandStep = (step: number) => {
    setExpandedStep(expandedStep === step ? null : step)
  }

  const isFormValid = () => {
    return (jobDescription || jobUrl) && files.length > 0
  }

  const handleEmailClick = async (candidate, type) => {
    setSelectedCandidate(candidate)
    setEmailType(type)
    setEmailModalOpen(true)
    setEmailContent("") // clear previous content
    setIsEmailLoading(true) // show loading state
  
    try {
      const response = await fetch("http://localhost:8000/generate_email_templates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate,
          email_type: type,
          job_description: stepOutputs[1], // parsed job description
        }),
      })
      const data = await response.json()
      setEmailContent(data.email_body)
    } catch (error) {
      setEmailContent(`Error generating email: ${error}`)
    } finally {
      setIsEmailLoading(false)
    }
  }
  
  

  return (
    <div className="space-y-8">
      <Card>
        <CardContent className="pt-6">
          <Tabs defaultValue="url">
            <TabsList className="mb-4">
              <TabsTrigger value="url">Job Description URL</TabsTrigger>
              <TabsTrigger value="text">Job Description Text</TabsTrigger>
            </TabsList>

            <TabsContent value="text" className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="job-description">Enter Job Description</Label>
                <Textarea
                  id="job-description"
                  placeholder="Paste the job description here..."
                  className="min-h-[200px]"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                />
              </div>
            </TabsContent>

            <TabsContent value="url" className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="job-url">Job Posting URL</Label>
                <Input
                  id="job-url"
                  type="url"
                  placeholder="https://example.com/job-posting"
                  value={jobUrl}
                  onChange={(e) => setJobUrl(e.target.value)}
                />
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            <Label>Upload Resumes (PDF)</Label>
            <FileUploader files={files} setFiles={setFiles} maxFiles={10} acceptedFileTypes={[".pdf"]} />
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-center">
        <Button size="lg" onClick={handleScreenResumesAndScroll} disabled={!isFormValid() || isScreening} className="px-8">
          Screen Resumes
        </Button>
      </div>

      {(isScreening || Object.keys(stepOutputs).length > 0) && (
        <Card>
          <CardContent className="pt-6">
            <ProgressTracker
              currentStage={currentStage}
              stepOutputs={stepOutputs}
              expandedStep={expandedStep}
              onToggleExpand={toggleExpandStep}
              isComplete={!isScreening && results.length > 0}
            />
          </CardContent>
        </Card>
      )}

      {results.length > 0 && (
        <Card>
          <CardContent className="pt-6">
            <h2 className="text-xl font-semibold mb-4">Screening Results</h2>
            <ResultsTable results={results} onEmailClick={handleEmailClick} />
          </CardContent>
        </Card>
      )}

<EmailModal
  isOpen={emailModalOpen}
  onClose={() => setEmailModalOpen(false)}
  emailContent={emailContent}
  emailType={emailType}
  candidateName={selectedCandidate?.name || ""}
  isLoading={isEmailLoading}
/>

    </div>
  )
}

