'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/stores/auth-store'
import { Briefcase, Clock, CheckCircle, Shield, PlusCircle, Upload, FileText, ChevronRight, TrendingUp, Activity, X, File, Loader2 } from 'lucide-react'
import { StatCard } from '@/components/shared/stat-card'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { RiskBadge } from '@/components/shared/risk-badge'
import { StatusBadge } from '@/components/shared/status-badge'
import { Button } from '@/components/ui/button'
import { LivePipelineTracker } from '@/components/shared/live-pipeline-tracker'
import Link from 'next/link'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { delay, duration: 0.4, ease: 'easeOut' as const } }
})

export default function OfficerDashboard() {
  const router = useRouter()
  const user = useAuthStore(state => state.user)
  const token = useAuthStore(state => state.token)
  const [dragOver, setDragOver] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [uploadState, setUploadState] = useState<'idle' | 'uploading' | 'processing' | 'done' | 'error'>('idle')
  const [uploadError, setUploadError] = useState('')

  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'
  const todayDate = new Date().toLocaleDateString('en-IN', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })

  const alerts = [
    { id: 'TL-20250115-0847', name: 'Rajesh Kumar', loan: 'Home Loan', amount: '₹45,00,000', score: 18, risk: 'HIGH' as const, findings: ['3 tampering indicators detected', '6 cross-document mismatches', 'Fraud DNA match found'], time: '3 hours ago' },
    { id: 'TL-20250115-0851', name: 'Sunita Devi', loan: 'Personal Loan', amount: '₹28,00,000', score: 62, risk: 'MEDIUM' as const, findings: ['Income mismatch in ITR', 'Suspicious metadata on PAN'], time: '5 hours ago' }
  ]

  const recentCases = [
    { id: 'TL-20250115-0847', name: 'Rajesh Kumar', loan: 'Home Loan', amount: '₹45,00,000', score: 18, risk: 'HIGH', status: 'Analyzed', time: '3h ago', triage: 'PRIORITY' },
    { id: 'TL-20250115-0851', name: 'Sunita Devi', loan: 'Personal Loan', amount: '₹28,00,000', score: 62, risk: 'MEDIUM', status: 'Analyzed', time: '5h ago', triage: 'WATCH' },
    { id: 'TL-20250115-0855', name: 'Amit Sharma', loan: 'Business Loan', amount: '₹75,00,000', score: null, risk: 'LOW', status: 'Analyzing', time: 'Now', triage: 'ROUTINE' },
    { id: 'TL-20250114-0834', name: 'Priya Patel', loan: 'Home Loan', amount: '₹52,00,000', score: 89, risk: 'LOW', status: 'Approved', time: '1d ago', triage: 'ROUTINE' },
    { id: 'TL-20250114-0828', name: 'Vikram Kumar', loan: 'Vehicle Loan', amount: '₹15,00,000', score: 91, risk: 'LOW', status: 'Approved', time: '1d ago', triage: 'ROUTINE' },
  ]

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const files = Array.from(e.dataTransfer.files).filter(f =>
      ['application/pdf', 'image/jpeg', 'image/png'].includes(f.type)
    )
    if (files.length) {
      setUploadedFiles(prev => [...prev, ...files])
    }
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      setUploadedFiles(prev => [...prev, ...files])
    }
  }

  const removeFile = (i: number) => setUploadedFiles(prev => prev.filter((_, idx) => idx !== i))

  const handleAnalyse = async () => {
    if (!uploadedFiles.length || !token) return
    setUploadState('uploading')
    setUploadError('')

    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const headers = { Authorization: `Bearer ${token}` }

      // 1. Validate at least 3 documents
      if (uploadedFiles.length < 3) {
        throw new Error('Please upload a minimum of 3 documents for a complete analysis.')
      }

      // 2. Create a temporary case
      const caseRes = await fetch(`${BASE}/api/v1/cases`, {
        method: 'POST',
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ applicant_name: 'Instant Analysis', loan_type: 'general', loan_amount: 0 })
      })
      if (!caseRes.ok) throw new Error('Failed to create case')
      const caseData = await caseRes.json()
      const caseId: string = caseData.id

      // 3. Upload all files to the new case in a single request
      const form = new FormData()
      for (const file of uploadedFiles) {
        form.append('files', file)
      }
      
      const docRes = await fetch(`${BASE}/api/v1/cases/${caseId}/documents`, {
        method: 'POST',
        headers,
        body: form
      })
      if (!docRes.ok) throw new Error('Failed to upload documents')
      
      // 4. Redirect to analysis page
      setUploadState('done')
      router.push(`/cases/${caseId}/analyze`)

    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Upload failed'
      setUploadError(msg)
      setUploadState('error')
    }
  }

  const handleReset = () => {
    setUploadedFiles([])
    setUploadState('idle')
    setUploadError('')
  }

  return (
    <div className="space-y-8 max-w-[1600px] mx-auto pb-10">

      {/* Header */}
      <motion.div {...fadeUp(0)}
        className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
            {greeting}, <span className="text-primary-700">{user?.full_name?.split(' ')[0] || 'Officer'}</span>
          </h1>
          <p className="text-slate-500 mt-1">{todayDate} · <span className="font-semibold text-slate-700 capitalize">{user?.role || 'Credit Officer'}</span></p>
        </div>
        <Link href="/cases/new">
          <Button className="bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-700 hover:to-indigo-700 text-white rounded-xl shadow-lg hover:shadow-primary-500/30 transition-all duration-300 gap-2">
            <PlusCircle className="w-5 h-5" /> Create New Case
          </Button>
        </Link>
      </motion.div>

      {/* Stats Row */}
      <motion.div {...fadeUp(0.07)}
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Assigned Cases" value="24" change="+3 this week" trend="up" icon={Briefcase} iconColor="text-blue-300" className="bg-gradient-to-br from-blue-900 via-indigo-900 to-indigo-950" />
        <StatCard title="Pending Review" value="5" subtext="Awaiting your action" icon={Clock} iconColor="text-amber-300" className="bg-gradient-to-br from-amber-900/90 via-orange-900/90 to-red-950" />
        <StatCard title="Analyzed Today" value="12" subtext="3 flagged · 8 approved · 1 rejected" icon={CheckCircle} iconColor="text-emerald-300" className="bg-gradient-to-br from-emerald-900 via-teal-900 to-slate-900" />
        <StatCard title="Fraud Prevented (Month)" value="₹1.2 Cr" subtext="From 8 flagged cases" icon={Shield} iconColor="text-fuchsia-300" className="bg-gradient-to-br from-fuchsia-900 via-purple-900 to-indigo-950" />
      </motion.div>

      {/* Main Grid */}
      <div className="flex flex-col gap-8">
        <div className="space-y-8">

          {/* ── Document Upload Section ── */}
          <motion.section {...fadeUp(0.14)}
            className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="p-6 border-b border-slate-100 bg-gradient-to-r from-indigo-50 via-blue-50 to-slate-50 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <div className="p-1.5 bg-indigo-600 rounded-lg">
                    <Upload className="w-4 h-4 text-white" />
                  </div>
                  Upload Documents for Analysis
                </h2>
                <p className="text-sm text-slate-500 mt-1">Drag & drop ITR, bank statements, PAN, sale deeds — AI will analyse instantly</p>
              </div>
              <Link href="/cases/new">
                <Button variant="outline" size="sm" className="text-indigo-700 border-indigo-200 hover:bg-indigo-50 rounded-lg text-xs">
                  Full Upload Flow
                </Button>
              </Link>
            </div>

            <div className="p-6 space-y-4">
              {/* Drop Zone */}
              <div
                onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
                className={`relative rounded-xl border-2 border-dashed transition-all duration-300 p-8 text-center cursor-pointer
                  ${dragOver ? 'border-indigo-500 bg-indigo-50 scale-[1.01]' : 'border-slate-200 hover:border-indigo-300 hover:bg-slate-50/70'}`}
              >
                <input
                  type="file"
                  multiple
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={handleFileInput}
                  className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
                />
                <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 transition-all duration-300 ${dragOver ? 'bg-indigo-100 rotate-6 scale-110' : 'bg-slate-100'}`}>
                  <Upload className={`w-7 h-7 ${dragOver ? 'text-indigo-600' : 'text-slate-400'}`} />
                </div>
                <p className="font-semibold text-slate-700">{dragOver ? 'Release to upload' : 'Drop documents here'}</p>
                <p className="text-sm text-slate-400 mt-1">Supports PDF, JPG, PNG · Max 10MB per file</p>
                <div className="mt-4 inline-flex items-center gap-2 text-xs bg-white border border-slate-200 rounded-full px-4 py-1.5 text-slate-600 shadow-sm">
                  <FileText className="w-3.5 h-3.5 text-indigo-500" /> Accepted: ITR, Bank Statement, PAN Card, Sale Deed, Balance Sheet
                </div>
              </div>

              {/* File List */}
              {uploadedFiles.length > 0 && (
                <div className="space-y-2">
                  {uploadedFiles.map((f, i) => (
                    <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                      className="flex items-center justify-between bg-slate-50 rounded-xl border border-slate-200 px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-indigo-100 rounded-lg">
                          <File className="w-4 h-4 text-indigo-600" />
                        </div>
                        <div>
                          <p className="text-sm font-medium text-slate-800 truncate max-w-[280px]">{f.name}</p>
                          <p className="text-xs text-slate-400">{(f.size / 1024).toFixed(1)} KB · {f.type.split('/')[1].toUpperCase()}</p>
                        </div>
                      </div>
                      {uploadState === 'processing' ? (
                        <Loader2 className="w-4 h-4 text-indigo-500 animate-spin" />
                      ) : uploadState === 'done' ? (
                        <span className="text-xs bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full font-semibold">✓ Queued</span>
                      ) : (
                        <button onClick={() => removeFile(i)} className="text-slate-400 hover:text-red-500 transition-colors p-1">
                          <X className="w-4 h-4" />
                        </button>
                      )}
                    </motion.div>
                  ))}

                  {uploadState !== 'done' && (
                    <div className="flex gap-3 pt-2">
                      <Button onClick={handleAnalyse} disabled={uploadState === 'uploading'}
                        className="bg-gradient-to-r from-indigo-600 to-primary-600 hover:from-indigo-700 hover:to-primary-700 text-white rounded-xl flex-1 gap-2 shadow-md hover:shadow-indigo-500/20 transition-all">
                        {uploadState === 'uploading' ? (
                          <><Loader2 className="w-4 h-4 animate-spin" /> Uploading & Creating Case...</>
                        ) : (
                          <><Activity className="w-4 h-4" /> Start AI Analysis</>
                        )}
                      </Button>
                      <Button variant="outline" onClick={() => setUploadedFiles([])} disabled={uploadState === 'uploading'} className="rounded-xl text-slate-600 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition-colors">
                        Clear All
                      </Button>
                    </div>
                  )}
                </div>
              )}

              {/* Error state */}
              {uploadState === 'error' && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-center justify-between">
                  <p className="text-sm text-red-700 font-semibold">{uploadError || 'Upload failed. Please try again.'}</p>
                  <Button variant="outline" onClick={handleReset} className="text-xs rounded-lg border-red-200 text-red-600 hover:bg-red-50">Retry</Button>
                </div>
              )}

              {/* Pipeline Steps — shown only when idle */}
              {uploadState === 'idle' && (
              <div className="pt-2">
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">How it works</p>
                <div className="grid grid-cols-4 gap-2">
                  {[
                    { step: '01', label: 'Upload Docs', icon: Upload, color: 'text-indigo-600', bg: 'bg-indigo-50' },
                    { step: '02', label: 'OCR Extraction', icon: FileText, color: 'text-amber-600', bg: 'bg-amber-50' },
                    { step: '03', label: 'AI Analysis', icon: Activity, color: 'text-purple-600', bg: 'bg-purple-50' },
                    { step: '04', label: 'Risk Report', icon: TrendingUp, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                  ].map((s, i) => (
                    <div key={i} className="flex flex-col items-center text-center gap-1.5 p-3 rounded-xl bg-slate-50 border border-slate-100">
                      <div className={`p-2 rounded-lg ${s.bg}`}>
                        <s.icon className={`w-4 h-4 ${s.color}`} />
                      </div>
                      <span className="text-[10px] font-bold text-slate-400">{s.step}</span>
                      <span className="text-xs font-semibold text-slate-700 leading-tight">{s.label}</span>
                    </div>
                  ))}
                </div>
              </div>
              )}
            </div>
          </motion.section>

          {/* Recent Cases Table */}
          <motion.section {...fadeUp(0.28)}
            className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
              <h2 className="text-lg font-bold text-slate-900">Your Recent Cases</h2>
              <Link href="/cases">
                <Button variant="outline" size="sm" className="text-slate-600 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors">
                  View All Cases
                </Button>
              </Link>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-500 bg-slate-50 uppercase font-semibold">
                  <tr>
                    <th className="px-6 py-4">Case ID</th>
                    <th className="px-6 py-4">Applicant</th>
                    <th className="px-6 py-4">Amount</th>
                    <th className="px-6 py-4">Triage</th>
                    <th className="px-6 py-4">Trust Score</th>
                    <th className="px-6 py-4">Risk</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4">Created</th>
                    <th className="px-6 py-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {recentCases.map((c, i) => (
                    <motion.tr key={i} {...fadeUp(0.35 + i * 0.05)}
                      className="hover:bg-blue-50/40 transition-colors group">
                      <td className="px-6 py-4 font-mono font-medium text-primary-700 text-xs">{c.id}</td>
                      <td className="px-6 py-4 font-medium text-slate-900">{c.name}<div className="text-xs text-slate-500 font-normal">{c.loan}</div></td>
                      <td className="px-6 py-4 text-slate-700 font-semibold">{c.amount}</td>
                      <td className="px-6 py-4">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase ${
                          c.triage === 'PRIORITY' ? 'bg-red-50 text-red-700 border-red-200' :
                          c.triage === 'WATCH' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                          'bg-slate-50 text-slate-500 border-slate-200'
                        }`}>
                          {c.triage}
                        </span>
                      </td>
                      <td className="px-6 py-4"><TrustScoreGauge score={c.score} size="sm" /></td>
                      <td className="px-6 py-4"><RiskBadge risk={c.risk} /></td>
                      <td className="px-6 py-4"><StatusBadge status={c.status} /></td>
                      <td className="px-6 py-4 text-slate-400 text-xs">{c.time}</td>
                      <td className="px-6 py-4 text-right">
                        <Link href={`/cases/${c.id}`} className="inline-flex items-center text-xs font-semibold text-primary-600 hover:text-primary-800 transition-colors bg-primary-50 group-hover:bg-primary-100 px-3 py-1.5 rounded-lg">
                          Open →
                        </Link>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.section>
        </div>
      </div>
    </div>
  )
}
