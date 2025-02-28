export async function processResumes(resumes: any[]) {
  // Simulate processing time
  await new Promise((resolve) => setTimeout(resolve, 1500))

  // Mock processing logic
  return resumes.map((resume) => ({
    id: resume.id,
    name: resume.name,
    parsed_content: {
      skills: ["JavaScript", "React", "Node.js", "TypeScript", "Python", "Java"].filter(() => Math.random() > 0.5),
      years_of_experience: Math.floor(Math.random() * 10) + 1,
      education: Math.random() > 0.7 ? "Master's Degree" : "Bachelor's Degree",
    },
  }))
}

