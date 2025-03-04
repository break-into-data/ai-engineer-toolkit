export async function processJobDescription(jobDescription: string) {
  // Simulate processing time
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Mock processing logic
  const skills = ["JavaScript", "React", "Node.js", "TypeScript"].filter(() => Math.random() > 0.3)
  const experience = Math.floor(Math.random() * 5) + 1

  return {
    extracted_skills: skills,
    required_experience: `${experience}+ years`,
    job_type: Math.random() > 0.5 ? "Full-time" : "Contract",
    seniority: experience > 3 ? "Senior" : "Mid-level",
  }
}

