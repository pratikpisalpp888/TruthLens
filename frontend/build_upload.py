import os

files = {
    "app/(protected)/cases/[id]/upload/page.tsx": """'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowLeft, UploadCloud, FileText, CheckCircle2, AlertCircle, X, Loader2, Landmark, FileCheck, Home, CreditCard, Receipt } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function DocumentUploadPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [isDragging, setIsDragging] = useState(false)
  const [files, setFiles] = useState<{name: string, size: string, status: string, type: string}[]>([])

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") setIsDragging(true)
    else if (e.type === "dragleave") setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      // Mock upload process
      const newFiles = Array.from(e.dataTransfer.files).map(f => ({
        name: f.name,
        size: (f.size / (1024*1024)).toFixed(1) + ' MB',
        status: 'uploading',
        type: 'Unknown'
      }))
      setFiles(prev => [...prev, ...newFiles])
      
      // Simulate processing
      setTimeout(() => {
        setFiles(prev => prev.map(f => f.status === 'uploading' ? { ...f, status: 'completed', type: 'ITR Document' } : f))
      }, 1500)
    }
  }
  
  const handleStartAnalysis = () => {
    router.push(`/cases/${params.id}/analyze`)
  }

  return (
    <div className="max-w-[1200px] mx-auto pb-24">
      {/* Header */}
      <div className="mb-6">
        <Link href={`/cases`} className="text-sm text-slate-500 hover:text-primary flex items-center font-medium transition-colors mb-4 w-max">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Cases
        </Link>
        
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Upload Documents</h1>
              <span className="text-xs font-semibold bg-slate-100 text-slate-700 px-2.5 py-1 rounded-full border border-slate-200">{params.id}</span>
            </div>
            <p className="text-slate-500 text-sm">Rajesh Kumar • Home Loan • ₹45,00,000</p>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium">
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 rounded-full bg-emerald-500 text-white flex items-center justify-center mb-1"><CheckCircle2 className="w-5 h-5" /></div>
              <span className="text-emerald-700 text-xs">Created</span>
            </div>
            <div className="w-12 h-0.5 bg-primary rounded-full"></div>
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 rounded-full bg-primary text-white shadow-md shadow-primary/30 flex items-center justify-center mb-1 relative">
                <span className="absolute inset-0 rounded-full bg-primary opacity-30 animate-ping"></span>
                2
              </div>
              <span className="text-primary-700 text-xs">Upload Docs</span>
            </div>
            <div className="w-12 h-0.5 bg-slate-200 rounded-full"></div>
            <div className="flex flex-col items-center opacity-50">
              <div className="w-8 h-8 rounded-full bg-slate-100 text-slate-500 border border-slate-300 flex items-center justify-center mb-1">3</div>
              <span className="text-slate-500 text-xs">AI Analysis</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_350px] gap-8 mt-8">
        {/* Main Upload Area */}
        <div className="space-y-6">
          <div 
            className={`w-full h-80 rounded-2xl border-2 border-dashed flex flex-col items-center justify-center p-6 transition-all duration-300 ease-out cursor-pointer
              ${isDragging ? 'border-primary bg-primary-50 scale-[1.02]' : 'border-slate-300 bg-slate-50 hover:bg-slate-100'}`}
            onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}
          >
            <div className={`p-4 rounded-full mb-4 ${isDragging ? 'bg-primary-100 text-primary-600' : 'bg-slate-200 text-slate-500'}`}>
              <UploadCloud className="w-10 h-10" />
            </div>
            <h3 className="text-xl font-bold text-slate-800 mb-2">Drag & Drop Documents Here</h3>
            <p className="text-sm text-slate-500 mb-6 text-center">or click to browse from your computer<br/>Supported: PDF, JPG, PNG • Max 10MB per file</p>
            <Button variant="outline" className="bg-white pointer-events-none">Browse Files</Button>
          </div>

          {/* Uploaded Files */}
          {files.length > 0 && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
              <div className="flex justify-between items-end">
                <h3 className="text-lg font-bold text-slate-900">Uploaded Documents ({files.length})</h3>
                <button className="text-sm text-slate-500 hover:text-red-500 font-medium">Clear All</button>
              </div>
              
              <div className="grid gap-3">
                {files.map((file, i) => (
                  <div key={i} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between group hover:border-slate-300 transition-colors">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0">
                        <FileText className="w-6 h-6 text-blue-600" />
                      </div>
                      <div>
                        <p className="text-sm font-bold text-slate-900 mb-0.5">{file.name}</p>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-500">{file.size}</span>
                          <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                          {file.status === 'uploading' ? (
                            <span className="text-xs font-medium text-amber-600 flex items-center gap-1"><Loader2 className="w-3 h-3 animate-spin" /> Classifying...</span>
                          ) : (
                            <span className="text-xs font-medium bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded flex items-center gap-1"><CheckCircle2 className="w-3 h-3" /> {file.type} (95%)</span>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button variant="ghost" size="sm" className="h-8 w-8 p-0 text-slate-400 hover:text-primary"><FileText className="w-4 h-4" /></Button>
                      <Button variant="ghost" size="sm" className="h-8 w-8 p-0 text-slate-400 hover:text-red-500"><X className="w-4 h-4" /></Button>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </div>

        {/* Right Sidebar Checklist */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 sticky top-24">
            <h3 className="font-bold text-slate-900 mb-1">Required Documents</h3>
            <p className="text-xs text-slate-500 mb-4">Upload these for complete analysis</p>
            
            <div className="space-y-3 mb-6">
              {[
                { name: 'ITR (Last 3 years)', icon: FileText, req: true },
                { name: 'Bank Statement', icon: Landmark, req: true },
                { name: 'Sale Deed', icon: FileCheck, req: true },
                { name: 'Property Valuation', icon: Home, req: true },
                { name: 'PAN Card', icon: CreditCard, req: true },
                { name: 'Salary Slips', icon: Receipt, req: false },
              ].map((doc, i) => (
                <div key={i} className="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-50 transition-colors">
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 ${files.length > 0 && i < 2 ? 'border-emerald-500 bg-emerald-500' : 'border-slate-300'}`}>
                    {files.length > 0 && i < 2 && <CheckCircle2 className="w-3 h-3 text-white" />}
                  </div>
                  <div className="flex flex-col">
                    <span className={`text-sm ${files.length > 0 && i < 2 ? 'text-slate-900 font-medium line-through opacity-70' : 'text-slate-700 font-medium'}`}>{doc.name}</span>
                  </div>
                  <doc.icon className="w-4 h-4 ml-auto text-slate-400" />
                </div>
              ))}
            </div>

            <div className="bg-amber-50 border border-amber-100 rounded-lg p-3 flex items-start gap-3 mb-6">
              <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <p className="text-xs text-amber-800 font-medium">Missing 3 required documents. Partial analysis is possible but not recommended.</p>
            </div>
            
          </div>
        </div>
      </div>

      {/* Sticky Bottom Action Bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 p-4 z-40 md:ml-[260px] ml-[72px] transition-all shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <div className="max-w-[1200px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-sm font-medium text-slate-700">
            {files.length} documents uploaded • <span className="text-amber-600">Minimum requirements not fully met</span>
          </div>
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <Button variant="outline" className="w-full sm:w-auto text-slate-600 font-semibold border-slate-300">
              Save & Analyze Later
            </Button>
            <Button 
              onClick={handleStartAnalysis}
              className="w-full sm:w-auto bg-gradient-to-r from-primary-700 to-primary-600 hover:from-primary-800 hover:to-primary-700 text-white font-bold px-8 shadow-lg shadow-primary/20 relative group overflow-hidden"
            >
              <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></span>
              Start AI Analysis
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
"""
}

def scaffold():
    for path, content in files.items():
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
if __name__ == "__main__":
    scaffold()
    print("Scaffolded Document Upload page.")
