"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { X, Upload, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"

interface FileUploaderProps {
  files: File[]
  setFiles: (files: File[]) => void
  maxFiles?: number
  acceptedFileTypes?: string[]
}

export function FileUploader({ files, setFiles, maxFiles = 10, acceptedFileTypes = [".pdf"] }: FileUploaderProps) {
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setError(null)

      if (files.length + acceptedFiles.length > maxFiles) {
        setError(`You can only upload up to ${maxFiles} files`)
        return
      }

      // Filter for PDF files
      const pdfFiles = acceptedFiles.filter((file) =>
        acceptedFileTypes.some((type) => file.name.toLowerCase().endsWith(type.replace(".", ""))),
      )

      if (pdfFiles.length !== acceptedFiles.length) {
        setError(`Only ${acceptedFileTypes.join(", ")} files are accepted`)
      }

      setFiles([...files, ...pdfFiles])
    },
    [files, setFiles, maxFiles, acceptedFileTypes],
  )

  const removeFile = (index: number) => {
    const newFiles = [...files]
    newFiles.splice(index, 1)
    setFiles(newFiles)
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": acceptedFileTypes,
    },
  })

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
          ${isDragActive ? "border-primary bg-primary/5" : "border-gray-300 hover:border-primary/50"}`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center space-y-2">
          <Upload className="h-8 w-8 text-gray-500" />
          <p className="text-sm text-gray-600">
            {isDragActive ? "Drop the files here..." : "Drag & drop resume files here, or click to select files"}
          </p>
          <p className="text-xs text-gray-500">Only PDF files are accepted (max {maxFiles} files)</p>
          <Button type="button" variant="outline" size="sm" className="mt-2">
            Select Files
          </Button>
        </div>
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}

      {files.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium">Uploaded Files ({files.length})</p>
          <ul className="space-y-2">
            {files.map((file, index) => (
              <li key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded border">
                <div className="flex items-center space-x-2">
                  <FileText className="h-4 w-4 text-gray-500" />
                  <span className="text-sm truncate max-w-[250px]">{file.name}</span>
                </div>
                <Button variant="ghost" size="sm" onClick={() => removeFile(index)} className="h-8 w-8 p-0">
                  <X className="h-4 w-4" />
                  <span className="sr-only">Remove file</span>
                </Button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

