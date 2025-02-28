export async function rankCandidates(scoredResumes: any[]) {
  // Simulate processing time
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Sort candidates by total score
  const rankedCandidates = scoredResumes.sort((a, b) => b.scores.total - a.scores.total)

  // Assign ranks
  return rankedCandidates.map((candidate, index) => ({
    ...candidate,
    rank: index + 1,
  }))
}

