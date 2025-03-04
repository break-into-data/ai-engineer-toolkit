import ResumeScreeningApp from "@/components/resume-screening-app"

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold text-center mb-8">Resume Screening Assistant</h1>
        <ResumeScreeningApp />
      </div>
    </main>
  )
}

