'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, UploadCloud, FileText, CheckCircle2, AlertCircle, X, Loader2, Landmark, FileCheck, Home, CreditCard, Receipt, Activity } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/auth-store'

interface CaseData {
  id: string
  applicant_name: string
  loan_type: string
  loan_amount: number
}

interface UploadedFile {
  name: string
  size: string
  status: 'uploading' | 'completed' | 'error'
  doc_type: string
  doc_id?: string
}

const REQUIRED_DOCS = [
  { name: 'ITR (Last 3 years)', icon: FileText },
  { name: 'Bank Statement', icon: Landmark },
  { name: 'Sale Deed', icon: FileCheck },
  { name: 'Property Valuation', icon: Home },
  { name: 'PAN Card', icon: CreditCard },
  { name: 'Salary Slips', icon: Receipt },
]

export default function DocumentUploadPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const token = useAuthStore(state => state.token)
  const [isDragging, setIsDragging] = useState(false)
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [caseData, setCaseData] = useState<CaseData | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  // Fetch real case data
  useEffect(() => {
    async function loadCase() {
      if (!token) return
      try {
        const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const res = await fetch(`${BASE}/api/v1/cases/${params.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (res.ok) {
          setCaseData(await res.json())
        }
      } catch (e) {
        console.error('Failed to load case', e)
      }
    }
    loadCase()
  }, [params.id, token])

  const uploadFile = useCallback(async (file: File) => {
    const entry: UploadedFile = {
      name: file.name,
      size: (file.size / (1024 * 1024)).toFixed(2) + ' MB',
      status: 'uploading',
      doc_type: 'Classifying…',
    }
    setFiles(prev => [...prev, entry])

    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const form = new FormData()
      form.append('files', file) // Backend expects 'files: List[UploadFile]'
      const res = await fetch(`${BASE}/api/v1/cases/${params.id}/documents`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: form,
      })

      if (!res.ok) throw new Error('Upload failed')
      const data = await res.json()
      // Backend returns an array: List[DocumentResponse]
      const doc = Array.isArray(data) ? data[0] : data
      
      setFiles(prev =>
        prev.map(f =>
          f.name === file.name && f.status === 'uploading'
            ? { ...f, status: 'completed', doc_type: doc?.document_type || 'Document', doc_id: doc?.id }
            : f
        )
      )
    } catch {
      setFiles(prev =>
        prev.map(f =>
          f.name === file.name && f.status === 'uploading'
            ? { ...f, status: 'error', doc_type: 'Upload Failed' }
            : f
        )
      )
    }
  }, [params.id, token])

  const processFiles = useCallback((rawFiles: FileList | File[]) => {
    const allowed = Array.from(rawFiles).filter(f =>
      ['application/pdf', 'image/jpeg', 'image/png'].includes(f.type)
    )
    allowed.forEach(uploadFile)
  }, [uploadFile])

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') setIsDragging(true)
    else if (e.type === 'dragleave') setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    if (e.dataTransfer.files.length) processFiles(e.dataTransfer.files)
  }

  const handleBrowse = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.multiple = true
    input.accept = '.pdf,.jpg,.jpeg,.png'
    input.onchange = () => { if (input.files?.length) processFiles(input.files) }
    input.click()
  }

  const removeFile = (name: string) => setFiles(prev => prev.filter(f => f.name !== name))

  const handleStartAnalysis = async () => {
    if (!token || files.length === 0) return
    setIsAnalyzing(true)
    router.push(`/cases/${params.id}/analyze`)
  }

  const completedCount = files.filter(f => f.status === 'completed').length
  const uploadingCount = files.filter(f => f.status === 'uploading').length

  const formatAmount = (amt: number) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(amt)

  return (
    <div className="max-w-[1200px] mx-auto pb-24">
      {/* Header */}
      <div className="mb-6">
        <Link href="/cases" className="text-sm text-slate-500 hover:text-primary flex items-center font-medium transition-colors mb-4 w-max">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Cases
        </Link>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Upload Documents</h1>
              <span className="text-xs font-semibold bg-slate-100 text-slate-700 px-2.5 py-1 rounded-full border border-slate-200">{params.id}</span>
            </div>
            {caseData ? (
              <p className="text-slate-500 text-sm">
                <span className="font-semibold text-slate-800">{caseData.applicant_name}</span>
                {' '}• {caseData.loan_type} • {formatAmount(caseData.loan_amount)}
              </p>
            ) : (
              <p className="text-slate-400 text-sm flex items-center gap-1.5"><Loader2 className="w-3.5 h-3.5 animate-spin" /> Loading case details…</p>
            )}
          </div>

          {/* Step Indicator */}
          <div className="flex items-center gap-4 text-sm font-medium">
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 rounded-full bg-emerald-500 text-white flex items-center justify-center mb-1"><CheckCircle2 className="w-5 h-5" /></div>
              <span className="text-emerald-700 text-xs">Created</span>
            </div>
            <div className="w-12 h-0.5 bg-primary rounded-full" />
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 rounded-full bg-primary text-white shadow-md shadow-primary/30 flex items-center justify-center mb-1 relative">
                <span className="absolute inset-0 rounded-full bg-primary opacity-30 animate-ping" />
                2
              </div>
              <span className="text-primary-700 text-xs">Upload Docs</span>
            </div>
            <div className="w-12 h-0.5 bg-slate-200 rounded-full" />
            <div className="flex flex-col items-center opacity-50">
              <div className="w-8 h-8 rounded-full bg-slate-100 text-slate-500 border border-slate-300 flex items-center justify-center mb-1">3</div>
              <span className="text-slate-500 text-xs">AI Analysis</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_350px] gap-8 mt-8">
        {/* Upload Area */}
        <div className="space-y-6">
          <div
            className={`w-full h-72 rounded-2xl border-2 border-dashed flex flex-col items-center justify-center p-6 transition-all duration-300 ease-out cursor-pointer
              ${isDragging ? 'border-primary bg-primary-50 scale-[1.02]' : 'border-slate-300 bg-slate-50 hover:bg-slate-100 hover:border-slate-400'}`}
            onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}
            onClick={handleBrowse}
          >
            <div className={`p-4 rounded-full mb-4 transition-colors ${isDragging ? 'bg-primary-100 text-primary-600' : 'bg-slate-200 text-slate-500'}`}>
              <UploadCloud className="w-10 h-10" />
            </div>
            <h3 className="text-xl font-bold text-slate-800 mb-2">Drag & Drop Documents Here</h3>
            <p className="text-sm text-slate-500 mb-6 text-center">
              or <span className="text-primary font-semibold underline cursor-pointer">click to browse from your computer</span>
              <br />Supported: PDF, JPG, PNG • Max 10MB per file
            </p>
            <Button variant="outline" className="bg-white pointer-events-none">Browse Files</Button>
          </div>

          {/* File List */}
          <AnimatePresence>
            {files.length > 0 && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-4">
                <div className="flex justify-between items-end">
                  <h3 className="text-lg font-bold text-slate-900">
                    Uploaded Documents ({completedCount}/{files.length})
                    {uploadingCount > 0 && <span className="ml-2 text-sm font-normal text-amber-600">• {uploadingCount} uploading…</span>}
                  </h3>
                  <button onClick={() => setFiles([])} className="text-sm text-slate-500 hover:text-red-500 font-medium transition-colors">Clear All</button>
                </div>

                <div className="grid gap-3">
                  {files.map((file, i) => (
                    <motion.div key={file.name + i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                      className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between group hover:border-slate-300 transition-colors">
                      <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-lg border flex items-center justify-center shrink-0 ${
                          file.status === 'completed' ? 'bg-emerald-50 border-emerald-100' :
                          file.status === 'error' ? 'bg-red-50 border-red-100' : 'bg-blue-50 border-blue-100'
                        }`}>
                          <FileText className={`w-6 h-6 ${
                            file.status === 'completed' ? 'text-emerald-600' :
                            file.status === 'error' ? 'text-red-500' : 'text-blue-600'
                          }`} />
                        </div>
                        <div>
                          <p className="text-sm font-bold text-slate-900 mb-0.5 truncate max-w-[280px]">{file.name}</p>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-500">{file.size}</span>
                            <span className="w-1 h-1 rounded-full bg-slate-300" />
                            {file.status === 'uploading' ? (
                              <span className="text-xs font-medium text-amber-600 flex items-center gap-1">
                                <Loader2 className="w-3 h-3 animate-spin" /> Uploading & Classifying…
                              </span>
                            ) : file.status === 'error' ? (
                              <span className="text-xs font-medium text-red-600 flex items-center gap-1">
                                <AlertCircle className="w-3 h-3" /> Upload Failed
                              </span>
                            ) : (
                              <span className="text-xs font-medium bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded flex items-center gap-1">
                                <CheckCircle2 className="w-3 h-3" /> {file.doc_type}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      <button onClick={() => removeFile(file.name)} className="text-slate-300 hover:text-red-500 transition-colors p-1 opacity-0 group-hover:opacity-100">
                        <X className="w-4 h-4" />
                      </button>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Sidebar Checklist */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 sticky top-24">
            <h3 className="font-bold text-slate-900 mb-1">Required Documents</h3>
            <p className="text-xs text-slate-500 mb-4">Upload these for complete analysis</p>

            <div className="space-y-3 mb-6">
              {REQUIRED_DOCS.map((doc, i) => {
                const done = i < completedCount
                return (
                  <div key={i} className="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-50 transition-colors">
                    <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 transition-colors ${done ? 'border-emerald-500 bg-emerald-500' : 'border-slate-300'}`}>
                      {done && <CheckCircle2 className="w-3 h-3 text-white" />}
                    </div>
                    <span className={`text-sm flex-1 ${done ? 'text-slate-400 line-through' : 'text-slate-700 font-medium'}`}>{doc.name}</span>
                    <doc.icon className="w-4 h-4 text-slate-400" />
                  </div>
                )
              })}
            </div>

            {completedCount < 3 && (
              <div className="bg-amber-50 border border-amber-100 rounded-lg p-3 flex items-start gap-3">
                <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <p className="text-xs text-amber-800 font-medium">Upload at least 3 documents for reliable fraud analysis.</p>
              </div>
            )}
            {completedCount >= 3 && (
              <div className="bg-emerald-50 border border-emerald-100 rounded-lg p-3 flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <p className="text-xs text-emerald-800 font-medium">Minimum requirements met! You can start AI analysis now.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Sticky Bottom Bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 p-4 z-40 md:ml-[260px] ml-[72px] shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <div className="max-w-[1200px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-sm font-medium text-slate-700">
            {completedCount} document{completedCount !== 1 ? 's' : ''} uploaded •{' '}
            {completedCount >= 3
              ? <span className="text-emerald-600 font-semibold">Ready for analysis</span>
              : <span className="text-amber-600">Minimum requirements not fully met</span>
            }
          </div>
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <Button variant="outline" className="w-full sm:w-auto text-slate-600 font-semibold border-slate-300"
              onClick={() => router.push('/cases')}>
              Save & Analyze Later
            </Button>
            <Button
              onClick={handleStartAnalysis}
              disabled={completedCount === 0 || uploadingCount > 0 || isAnalyzing}
              className="w-full sm:w-auto bg-gradient-to-r from-primary-700 to-primary-600 hover:from-primary-800 hover:to-primary-700 text-white font-bold px-8 shadow-lg shadow-primary/20 gap-2 disabled:opacity-60"
            >
              {isAnalyzing
                ? <><Loader2 className="w-4 h-4 animate-spin" /> Launching…</>
                : uploadingCount > 0
                  ? <><Loader2 className="w-4 h-4 animate-spin" /> Uploading…</>
                  : <><Activity className="w-4 h-4" /> Start AI Analysis</>
              }
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
