import { CheckCircle, Circle, Loader2, ChevronDown, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ProgressTrackerProps {
  currentStage: number
  stepOutputs: Record<number, any>
  expandedStep: number | null
  onToggleExpand: (step: number) => void
  isComplete: boolean
}

export function ProgressTracker({
  currentStage,
  stepOutputs,
  expandedStep,
  onToggleExpand,
  isComplete,
}: ProgressTrackerProps) {
  const stages = ["Processing Inputs", "Parsing Job Description", "Parsing Resumes", "Scoring Resumes", "Ranking Resumes"]

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">{isComplete ? "Processing Complete" : "Processing Resumes"}</h2>
      <div className="space-y-4">
        {stages.map((stage, index) => {
          const hasOutput = stepOutputs[index] !== undefined
          const isExpanded = expandedStep === index

          return (
            <div key={index} className="space-y-2">
              <div className="flex items-center">
                <div className="flex items-center space-x-3 flex-1">
                  {index < currentStage || isComplete ? (
                    <CheckCircle className="h-6 w-6 text-green-500 flex-shrink-0" />
                  ) : index === currentStage ? (
                    <Loader2 className="h-6 w-6 text-primary animate-spin flex-shrink-0" />
                  ) : (
                    <Circle className="h-6 w-6 text-gray-300 flex-shrink-0" />
                  )}
                  <span
                    className={`
                    ${index < currentStage || isComplete ? "text-gray-700" : ""}
                    ${index === currentStage && !isComplete ? "font-medium text-primary" : ""}
                    ${index > currentStage && !isComplete ? "text-gray-400" : ""}
                  `}
                  >
                    {stage}
                  </span>
                </div>

                {hasOutput && (
                  <Button variant="ghost" size="sm" className="ml-auto" onClick={() => onToggleExpand(index)}>
                    {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                    <span className="ml-1 text-xs">{isExpanded ? "Hide Output" : "Show Output"}</span>
                  </Button>
                )}
              </div>

              {hasOutput && isExpanded && (
                <div className="ml-9 mt-2">
                  <div className="bg-gray-50 p-3 rounded border overflow-x-auto">
                    <pre className="text-xs text-gray-700 whitespace-pre-wrap">
                      {JSON.stringify(stepOutputs[index], null, 2)}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

