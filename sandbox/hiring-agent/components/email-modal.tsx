"use client"

import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Check, Copy } from "lucide-react"

interface EmailModalProps {
  isOpen: boolean
  onClose: () => void
  emailContent: string
  emailType: "accept" | "reject"
  candidateName: string
  isLoading?: boolean
}

export function EmailModal({
  isOpen,
  onClose,
  emailContent,
  emailType,
  candidateName,
  isLoading = false,
}: EmailModalProps) {
  const [copied, setCopied] = useState(false)
  const [content, setContent] = useState(emailContent)

  // Update local state when emailContent prop changes.
  useEffect(() => {
    setContent(emailContent)
  }, [emailContent])

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>
            {emailType === "accept" ? "Interview Invitation" : "Rejection Email"} for{" "}
            {candidateName}
          </DialogTitle>
        </DialogHeader>

        <div className="py-4">
          {isLoading ? (
            // Loading state (you can replace with a spinner or other indicator)
            <div className="flex justify-center items-center h-[300px]">
              <span className="text-lg font-medium">Loading email...</span>
            </div>
          ) : (
            <Textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="min-h-[300px] font-mono text-sm"
            />
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
          <Button onClick={handleCopy} className="flex items-center space-x-2">
            {copied ? (
              <>
                <Check className="h-4 w-4" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                <span>Copy to Clipboard</span>
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
