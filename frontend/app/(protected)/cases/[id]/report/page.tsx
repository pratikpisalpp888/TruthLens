'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft, Download, Printer, Share2, Brain, ShieldAlert, ShieldCheck,
  AlertTriangle, CheckCircle2, Fingerprint, GitCompare, Scale, Gavel,
  BookOpen, Sparkles, ChevronDown, ChevronUp, RefreshCw, Info, FileText,
  Clock, TrendingUp, AlertCircle, Scan
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/auth-store'
import { InterrogatorPanel } from '@/components/case/interrogator-panel'

const iconMap: Record<string, any> = {
  brain: Brain,
  fingerprint: Fingerprint,
  'git-compare': GitCompare,
  scale: Scale,
  gavel: Gavel,
}

const qualityConfig = {
  relevant: { label: 'Verified from Knowledge Base', color: 'text-emerald-600 bg-emerald-50 border-emerald-200', dot: 'bg-emerald-500' },
  corrected: { label: 'CRAG-Corrected Search', color: 'text-amber-600 bg-amber-50 border-amber-200', dot: 'bg-amber-500' },
  irrelevant: { label: 'General AI Response', color: 'text-slate-500 bg-slate-50 border-slate-200', dot: 'bg-slate-400' },
  unavailable: { label: 'Unavailable', color: 'text-red-600 bg-red-50 border-red-200', dot: 'bg-red-500' },
}

function RiskMeter({ score }: { score: number }) {
  const color = score > 70 ? '#ef4444' : score > 40 ? '#f59e0b' : '#22c55e'
  const label = score > 70 ? 'HIGH RISK' : score > 40 ? 'MEDIUM RISK' : 'LOW RISK'
  const rotation = -135 + (score / 100) * 270

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-40 h-20 overflow-hidden">
        <svg viewBox="0 0 100 50" className="w-full h-full">
          <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#f1f5f9" strokeWidth="10" strokeLinecap="round" />
          <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke={color} strokeWidth="10" strokeLinecap="round"
            strokeDasharray={`${(score / 100) * 126} 126`} />
          <circle cx="50" cy="50" r="4" fill={color} />
          <line x1="50" y1="50" x2="50" y2="14"
            stroke={color} strokeWidth="2.5" strokeLinecap="round"
            transform={`rotate(${rotation}, 50, 50)`} />
        </svg>
      </div>
      <div className="text-4xl font-black mt-1" style={{ color }}>{score}</div>
      <div className="text-[10px] font-black tracking-widest mt-1" style={{ color }}>{label}</div>
    </div>
  )
}

function SectionCard({ section, index }: { section: any; index: number }) {
  const [expanded, setExpanded] = useState(true)
  const Icon = iconMap[section.icon] || Brain
  const quality = qualityConfig[section.retrieval_quality as keyof typeof qualityConfig] || qualityConfig.unavailable
  const confidence = Math.round(section.confidence * 100)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden"
    >
      {/* Card Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-6 text-left hover:bg-slate-50 transition-colors"
      >
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-50 to-indigo-100 border border-blue-200 rounded-xl flex items-center justify-center shrink-0">
            <Icon className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">{section.section}</h3>
            <div className="flex items-center gap-2 mt-1">
              <span className={`inline-flex items-center gap-1.5 text-[10px] font-bold px-2 py-0.5 rounded border ${quality.color}`}>
                <span className={`w-1.5 h-1.5 rounded-full ${quality.dot}`} />
                {quality.label}
              </span>
              <span className="text-[10px] text-slate-400 font-medium">Confidence: {confidence}%</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0 ml-4">
          {/* Confidence Ring */}
          <div className="relative w-10 h-10">
            <svg className="transform -rotate-90 w-full h-full">
              <circle cx="20" cy="20" r="16" fill="transparent" stroke="#f1f5f9" strokeWidth="4" />
              <circle cx="20" cy="20" r="16" fill="transparent" stroke={confidence > 70 ? '#22c55e' : confidence > 40 ? '#f59e0b' : '#94a3b8'}
                strokeWidth="4" strokeDasharray={`${100.5 * confidence / 100} 100.5`} strokeLinecap="round" />
            </svg>
            <span className="absolute inset-0 flex items-center justify-center text-[9px] font-black text-slate-700">{confidence}%</span>
          </div>
          {expanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
        </div>
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-6 pb-6 pt-2 border-t border-slate-100">
              {/* AI Answer */}
              <div className="bg-gradient-to-br from-slate-50 to-blue-50/30 rounded-xl p-5 mb-4 border border-slate-100">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles className="w-4 h-4 text-blue-500" />
                  <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">CRAG Analysis</span>
                </div>
                <p className="text-sm text-slate-700 leading-relaxed font-medium">{section.answer}</p>
              </div>

              {/* Sources */}
              {section.sources && section.sources.length > 0 && (
                <div>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5" /> Knowledge Sources
                  </p>
                  <div className="space-y-2">
                    {section.sources.map((src: any, i: number) => (
                      <div key={i} className="flex items-center justify-between bg-white border border-slate-100 rounded-lg px-3 py-2">
                        <div className="flex items-center gap-2">
                          <FileText className="w-3.5 h-3.5 text-slate-400" />
                          <span className="text-xs text-slate-700 font-medium truncate max-w-[300px]">{src.file || 'Banking Guidelines'}</span>
                        </div>
                        <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100 shrink-0 ml-2">
                          {Math.round(src.relevance * 100)}% match
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {section.was_corrected && (
                <div className="mt-3 flex items-start gap-2 text-xs text-amber-700 bg-amber-50 border border-amber-100 rounded-lg p-3">
                  <Info className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                  <span>CRAG performed a corrective search — original query was refined to improve retrieval quality.</span>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

export default function AIReportPage({ params }: { params: { id: string } }) {
  const token = useAuthStore(state => state.token)
  const [report, setReport] = useState<any>(null)
  const [caseData, setCaseData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function fetchReport() {
    if (!token) return
    setLoading(true)
    setError(null)
    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || ''
      const headers = { Authorization: `Bearer ${token}` }

      const [caseRes, reportRes] = await Promise.all([
        fetch(`${BASE}/api/v1/cases/${params.id}`, { headers }),
        fetch(`${BASE}/api/v1/cases/${params.id}/ai-report`, { headers })
      ])

      if (caseRes.ok) setCaseData(await caseRes.json())
      if (reportRes.ok) {
        const data = await reportRes.json()
        setReport(data)
      } else {
        setError('Failed to generate AI report. Run AI Analysis first.')
      }
    } catch (e) {
      setError('Network error while fetching report.')
    } finally {
      setLoading(false)
    }
  }

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { fetchReport() }, [params.id, token])

  const score = report?.risk_scores?.composite || 0
  const decision = report?.decision?.decision || 'pending'
  const decisionColor = decision === 'approved' ? 'text-emerald-600 bg-emerald-50 border-emerald-300'
    : decision === 'rejected' ? 'text-red-600 bg-red-50 border-red-300'
    : 'text-amber-600 bg-amber-50 border-amber-300'
  const decisionIcon = decision === 'approved' ? ShieldCheck : decision === 'rejected' ? ShieldAlert : AlertTriangle

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-100 to-slate-50 -mx-6 -my-8 absolute inset-0 top-16 z-40 overflow-auto">

      {/* Sticky Toolbar */}
      <div className="sticky top-0 z-50 bg-white/90 backdrop-blur-xl border-b border-slate-200 px-6 py-3 shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href={`/cases/${params.id}`} className="text-slate-400 hover:text-blue-600 transition-colors p-1 rounded-lg hover:bg-slate-100">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-500" />
              CRAG-Powered AI Report
            </h1>
            <p className="text-xs text-slate-500 font-mono">Case {caseData?.case_number || params.id}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {caseData?.documents && caseData.documents.length > 0 && (
            <Link href={`/cases/${params.id}/documents/${caseData.documents[0].id}`}>
              <Button size="sm" className="h-8 text-xs bg-indigo-600 hover:bg-indigo-700 text-white gap-2 shadow-lg shadow-indigo-500/20">
                <Scan className="w-3.5 h-3.5" /> View Annotated Doc
              </Button>
            </Link>
          )}
          <Button variant="outline" size="sm" onClick={fetchReport} className="h-8 text-xs border-slate-200 gap-2">
            <RefreshCw className="w-3.5 h-3.5" /> Regenerate
          </Button>
          <Button variant="outline" size="sm" className="h-8 text-xs border-slate-200 gap-2">
            <Printer className="w-3.5 h-3.5" /> Print
          </Button>
          <a href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/cases/${params.id}/report.pdf`} target="_blank">
            <Button size="sm" className="h-8 text-xs bg-blue-600 hover:bg-blue-700 text-white gap-2">
              <Download className="w-3.5 h-3.5" /> PDF
            </Button>
          </a>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-32 gap-6">
            <div className="relative">
              <div className="w-20 h-20 rounded-full border-4 border-blue-100 border-t-blue-600 animate-spin" />
              <Brain className="w-8 h-8 text-blue-600 absolute inset-0 m-auto" />
            </div>
            <div className="text-center">
              <h3 className="text-xl font-bold text-slate-900 mb-1">Running CRAG Analysis</h3>
              <p className="text-sm text-slate-500">Querying knowledge base with Corrective RAG...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {!loading && error && (
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <div className="w-16 h-16 rounded-2xl bg-red-50 border border-red-200 flex items-center justify-center">
              <AlertCircle className="w-8 h-8 text-red-500" />
            </div>
            <div className="text-center">
              <h3 className="text-lg font-bold text-slate-900 mb-1">Report Unavailable</h3>
              <p className="text-sm text-slate-500 max-w-sm">{error}</p>
            </div>
            <Link href={`/cases/${params.id}/analyze`}>
              <Button className="bg-blue-600 text-white hover:bg-blue-700 gap-2">
                <Brain className="w-4 h-4" /> Run AI Analysis First
              </Button>
            </Link>
          </div>
        )}

        {/* Report Content */}
        {!loading && report && (
          <>
            {/* Hero Card */}
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-gradient-to-br from-slate-900 to-[#0f172a] rounded-3xl p-8 text-white relative overflow-hidden shadow-2xl"
            >
              {/* Background decorations */}
              <div className="absolute top-0 right-0 w-80 h-80 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
              <div className="absolute bottom-0 left-0 w-60 h-60 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />

              <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center gap-8">
                {/* Risk Meter */}
                <div className="shrink-0 bg-white/5 border border-white/10 rounded-2xl p-6">
                  <RiskMeter score={Math.round(score)} />
                </div>

                {/* Details */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                      <span className="text-white font-black text-sm">TL</span>
                    </div>
                    <div>
                      <p className="text-blue-400 text-xs font-bold uppercase tracking-widest">TruthLens AI</p>
                      <h2 className="text-xl font-bold text-white">CRAG Intelligence Report</h2>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mt-5">
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <p className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">Applicant</p>
                      <p className="text-white font-bold text-sm">{caseData?.applicant_name || '—'}</p>
                    </div>
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <p className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">Loan Amount</p>
                      <p className="text-white font-bold text-sm">
                        ₹{caseData?.loan_amount ? new Intl.NumberFormat('en-IN').format(caseData.loan_amount) : '—'}
                      </p>
                    </div>
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <p className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">AI Decision</p>
                      <span className={`inline-flex items-center gap-1.5 text-xs font-black px-3 py-1.5 rounded-lg border ${decisionColor}`}>
                        {decision.toUpperCase()}
                      </span>
                    </div>
                    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                      <p className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">Generated</p>
                      <p className="text-white font-medium text-xs flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        {report.generated_at ? new Date(report.generated_at).toLocaleString() : 'Now'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* AI Confidence Bar */}
              <div className="relative z-10 mt-6 pt-6 border-t border-white/10">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-blue-400" />
                    <span className="text-xs font-bold text-slate-300">Overall CRAG Confidence</span>
                  </div>
                  <span className="text-sm font-black text-white">{Math.round((report.avg_confidence || 0) * 100)}%</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(report.avg_confidence || 0) * 100}%` }}
                    transition={{ duration: 1.2, delay: 0.5, ease: 'easeOut' }}
                    className="h-full bg-gradient-to-r from-blue-400 to-purple-400 rounded-full"
                  />
                </div>
              </div>
            </motion.div>

            {/* Decision Reasoning */}
            {report.decision?.reasoning && report.decision.reasoning.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className={`rounded-2xl border p-6 ${decision === 'rejected' ? 'bg-red-50 border-red-200' : decision === 'approved' ? 'bg-emerald-50 border-emerald-200' : 'bg-amber-50 border-amber-200'}`}
              >
                <div className="flex items-start gap-4">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${decision === 'rejected' ? 'bg-red-100' : decision === 'approved' ? 'bg-emerald-100' : 'bg-amber-100'}`}>
                    {React.createElement(decisionIcon, { className: `w-5 h-5 ${decision === 'rejected' ? 'text-red-600' : decision === 'approved' ? 'text-emerald-600' : 'text-amber-600'}` })}
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-900 mb-2">AI Decision Reasoning</h3>
                    <ul className="space-y-1">
                      {report.decision.reasoning.map((r: string, i: number) => (
                        <li key={i} className="text-sm text-slate-700 flex items-start gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-slate-400 shrink-0 mt-2" />
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Stats Row */}
            <div className="grid grid-cols-4 gap-4">
              {[
                { label: 'Risk Score', value: `${Math.round(score)}/100`, icon: TrendingUp, color: 'text-red-600', bg: 'bg-red-50 border-red-100' },
                { label: 'CRAG Sections', value: report.total_sections || 0, icon: BookOpen, color: 'text-blue-600', bg: 'bg-blue-50 border-blue-100' },
                { label: 'Avg Confidence', value: `${Math.round((report.avg_confidence || 0) * 100)}%`, icon: Sparkles, color: 'text-purple-600', bg: 'bg-purple-50 border-purple-100' },
                { label: 'Risk Category', value: (report.risk_scores?.category || 'Low').toUpperCase(), icon: ShieldAlert, color: 'text-amber-600', bg: 'bg-amber-50 border-amber-100' },
              ].map((stat, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + i * 0.05 }}
                  className={`rounded-2xl border p-5 ${stat.bg}`}
                >
                  <div className={`flex items-center gap-2 mb-2 ${stat.color}`}>
                    <stat.icon className="w-4 h-4" />
                    <span className="text-xs font-bold uppercase tracking-wider">{stat.label}</span>
                  </div>
                  <p className={`text-2xl font-black ${stat.color}`}>{stat.value}</p>
                </motion.div>
              ))}
            </div>

            {/* CRAG Section Cards */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <Brain className="w-5 h-5 text-blue-600" />
                <h2 className="text-lg font-bold text-slate-900">AI Intelligence Sections</h2>
                <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full font-medium">
                  Powered by Corrective RAG
                </span>
              </div>
              <div className="space-y-4">
                {report.sections?.map((section: any, i: number) => (
                  <SectionCard key={i} section={section} index={i} />
                ))}
              </div>
            </div>

            {/* Footer Note */}
            <div className="text-center py-6 border-t border-slate-200">
              <p className="text-xs text-slate-400 font-medium">
                This report was generated by <span className="font-bold text-blue-600">TruthLens CRAG AI</span> and is for internal review only.
                Human verification is required before any final decision.
              </p>
            </div>
          </>
        )}
      </div>
      
      {/* AI Interrogator Chat */}
      <InterrogatorPanel caseId={params.id} />
    </div>
  )
}
