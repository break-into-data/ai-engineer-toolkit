import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Check, X } from "lucide-react"

interface ResultsTableProps {
  results: any[]
  onEmailClick: (candidate: any, type: "accept" | "reject") => void
}

export function ResultsTable({ results, onEmailClick }: ResultsTableProps) {
  return (
    <div className="overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[180px]">Candidate Name</TableHead>
            <TableHead className="w-[100px] text-center">Score</TableHead>
            <TableHead>Notes</TableHead>
            <TableHead className="w-[200px] text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {results.map((candidate) => (
            <TableRow key={candidate.id}>
              <TableCell className="font-medium">{candidate.name}</TableCell>
              <TableCell className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100">
                  <span className={`text-sm font-semibold ${getScoreColor(candidate.overall)}`}>{candidate.overall}</span>
                </div>
              </TableCell>
              <TableCell>{candidate.comment}</TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end space-x-2">
                  <Button
                    size="sm"
                    variant="outline"
                    className="flex items-center space-x-1 border-green-500 text-green-600 hover:bg-green-50"
                    onClick={() => onEmailClick(candidate, "accept")}
                  >
                    <Check className="h-4 w-4" />
                    <span>Accept</span>
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    className="flex items-center space-x-1 border-red-500 text-red-600 hover:bg-red-50"
                    onClick={() => onEmailClick(candidate, "reject")}
                  >
                    <X className="h-4 w-4" />
                    <span>Reject</span>
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

function getScoreColor(score: number) {
  if (score >= 80) return "text-green-600"
  if (score >= 70) return "text-blue-600"
  if (score >= 60) return "text-amber-600"
  return "text-red-600"
}

