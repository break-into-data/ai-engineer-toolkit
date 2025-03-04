export async function scoreResumes(processedResumes: any[], jobRequirements: any) {
  // Simulate processing time
  await new Promise((resolve) => setTimeout(resolve, 2000))

  // Mock scoring logic
  return processedResumes.map((resume) => {
    const skillsScore = calculateSkillsScore(resume.parsed_content.skills, jobRequirements.extracted_skills)
    const experienceScore = calculateExperienceScore(
      resume.parsed_content.years_of_experience,
      jobRequirements.required_experience,
    )
    const educationScore = calculateEducationScore(resume.parsed_content.education)

    const totalScore = skillsScore * 0.5 + experienceScore * 0.3 + educationScore * 0.2

    return {
      ...resume,
      scores: {
        skills: skillsScore,
        experience: experienceScore,
        education: educationScore,
        total: totalScore,
      },
    }
  })
}

function calculateSkillsScore(candidateSkills: string[], requiredSkills: string[]) {
  const matchedSkills = candidateSkills.filter((skill) => requiredSkills.includes(skill))
  return (matchedSkills.length / requiredSkills.length) * 100
}

function calculateExperienceScore(candidateExperience: number, requiredExperience: string) {
  const requiredYears = Number.parseInt(requiredExperience)
  if (candidateExperience >= requiredYears) return 100
  return (candidateExperience / requiredYears) * 100
}

function calculateEducationScore(education: string) {
  switch (education) {
    case "PhD":
      return 100
    case "Master's Degree":
      return 90
    case "Bachelor's Degree":
      return 80
    default:
      return 70
  }
}

