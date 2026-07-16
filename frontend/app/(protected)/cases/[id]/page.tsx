'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronRight, Download, Printer, Mic, FileText, CheckCircle2, AlertTriangle, AlertCircle, Scan, Brain, ExternalLink, Network, FileCheck, Landmark, Search, Grid, List, Check, X, Flag, MessageSquare, Fingerprint } from 'lucide-react'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { Button } from '@/components/ui/button'
import { FraudNetworkGraph } from '@/components/case/fraud-network-graph'
import { CaseChat, CaseChatButton } from '@/components/case/case-chat'
import { useAuthStore } from '@/stores/auth-store'

const TABS = ['Overview', 'Documents', 'Analysis (7 Layers)', 'Mismatches', 'Fraud DNA', 'Network Intelligence', 'Compliance', 'Report', 'Decision']

export default function CaseDetailPage({ params }: { params: { id: string } }) {
  const [activeTab, setActiveTab] = useState('Overview')
  const [docView, setDocView] = useState<'grid' | 'list'>('grid')
  const [isChatOpen, setIsChatOpen] = useState(false)
  const token = useAuthStore(state => state.token)
  
  const [caseData, setCaseData] = useState<any>(null)
  const [reportData, setReportData] = useState<any>(null)
  
  useEffect(() => {
    async function fetchData() {
      if (!token) return
      try {
        const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        
        // Fetch case info
        const caseRes = await fetch(`${BASE}/api/v1/cases/${params.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (caseRes.ok) setCaseData(await caseRes.json())
        
        // Fetch AI full report
        const reportRes = await fetch(`${BASE}/api/v1/cases/${params.id}/full-report`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (reportRes.ok) setReportData(await reportRes.json())

      } catch (e) {
        console.error('Failed to load case data', e)
      }
    }
    fetchData()
  }, [params.id, token])

  const formatAmount = (n: number) => n ? '₹' + new Intl.NumberFormat('en-IN').format(n) : '₹0'

  const score = reportData?.risk_scores?.composite || caseData?.risk_score || 0
  const isHighRisk = score > 60

  return (
    <div className="max-w-[1400px] mx-auto pb-24">
      {/* Header Breadcrumbs */}
      <div className="mb-4">
        <Link href={`/cases`} className="text-sm text-slate-500 hover:text-primary flex items-center font-medium transition-colors w-max">
          Cases <ChevronRight className="w-4 h-4 mx-1" /> Case {caseData?.case_number || params.id}
        </Link>
      </div>

      {/* Case Header Card */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-8 mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-red-500/5 rounded-full blur-[80px] pointer-events-none"></div>
        
        <div className="relative z-10 flex-1">
          <div className="flex items-center gap-4 mb-3">
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight">{caseData?.case_number || params.id}</h1>
            <span className={`bg-slate-100 text-slate-700 text-xs font-bold px-3 py-1 rounded border border-slate-200 uppercase tracking-wide`}>
              {caseData?.status || 'Analyzing'}
            </span>
          </div>
          <h2 className="text-2xl font-bold text-slate-800 mb-2">
            {caseData?.applicant_name || 'Loading...'}
          </h2>
          <p className="text-slate-500 font-medium flex items-center gap-2 mb-4">
            <Landmark className="w-4 h-4" /> {caseData?.loan_type || 'Loan'} • {formatAmount(caseData?.loan_amount)}
          </p>
          
          <div className="flex flex-wrap gap-3">
            <a href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/cases/${params.id}/report.pdf`} target="_blank" rel="noreferrer">
              <Button className="bg-white text-slate-700 border-slate-200 shadow-sm hover:bg-slate-50">
                <Download className="w-4 h-4 mr-2" /> PDF Report
              </Button>
            </a>
            <Button variant="outline" className="border-slate-200 text-slate-700 hover:bg-slate-50">
              <GitCompareIcon className="w-4 h-4 mr-2" /> Compare Docs
            </Button>
            <Button variant="outline" className="border-slate-200 text-slate-700 hover:bg-slate-50" onClick={() => setActiveTab('Network Intelligence')}>
              <Network className="w-4 h-4 mr-2" /> Fraud Network
            </Button>
            <div className="w-px h-10 bg-slate-200 mx-1"></div>
            <Button variant="ghost" size="icon" className="text-slate-500 hover:text-primary"><Printer className="w-5 h-5" /></Button>
          </div>
        </div>

        <div className="relative z-10 flex items-center gap-6 bg-slate-50 p-6 rounded-2xl border border-slate-100 min-w-[300px]">
          <div className="flex-1">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Overall Trust Score</p>
            <h3 className="text-xl font-bold text-slate-900 mb-2">{isHighRisk ? 'Critical Fraud Risk' : 'Low Fraud Risk'}</h3>
            <span className={`inline-flex items-center gap-1.5 text-xs font-bold px-2.5 py-1 rounded text-center
              ${isHighRisk ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'}`}>
              <AlertTriangle className="w-3.5 h-3.5" /> {isHighRisk ? 'REJECT RECOMMENDED' : 'APPROVE RECOMMENDED'}
            </span>
          </div>
          <div className="shrink-0">
            <TrustScoreGauge score={score} size="lg" />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200 mb-8 sticky top-0 bg-slate-50/80 backdrop-blur-md z-30 pt-2 -mx-4 px-4 sm:mx-0 sm:px-0">
        <nav className="flex space-x-1 sm:space-x-8 overflow-x-auto custom-scrollbar pb-px">
          {TABS.map((tab) => {
            const isActive = activeTab === tab
            const hasBadge = tab === 'Mismatches' || tab === 'Fraud DNA' || tab === 'Compliance'
            let badgeCount = 0
            if (reportData) {
              if (tab === 'Mismatches') badgeCount = reportData.mismatches?.length || 0
              if (tab === 'Fraud DNA') badgeCount = reportData.fraud_dna?.length || 0
              if (tab === 'Compliance') badgeCount = reportData.compliance?.length || 0
            }

            // Report tab navigates to the full dedicated CRAG report page
            if (tab === 'Report') {
              return (
                <Link
                  key={tab}
                  href={`/cases/${params.id}/report`}
                  className={`whitespace-nowrap py-4 px-3 sm:px-1 border-b-2 font-medium text-sm transition-colors relative flex items-center gap-1.5
                    border-transparent text-blue-600 hover:text-blue-700 hover:border-blue-400`}
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
                  {tab}
                  <span className="text-[9px] font-black bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded-full ml-1">AI</span>
                </Link>
              )
            }

            return (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`whitespace-nowrap py-4 px-3 sm:px-1 border-b-2 font-medium text-sm transition-colors relative
                  ${isActive ? 'border-primary text-primary-700' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}
              >
                {tab}
                {hasBadge && badgeCount > 0 && (
                  <span className={`ml-2 inline-flex items-center justify-center w-5 h-5 text-[10px] font-bold rounded-full
                    ${isActive ? 'bg-primary-100 text-primary-700' : 'bg-slate-100 text-slate-600'}`}>
                    {badgeCount}
                  </span>
                )}
              </button>
            )
          })}
        </nav>

      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === 'Network Intelligence' && token && (
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden p-6">
              <FraudNetworkGraph caseId={params.id} token={token} />
            </div>
          )}

          {activeTab === 'Overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Left Column (Main Stats) */}
              <div className="lg:col-span-2 space-y-6">
                
                {/* Findings Card */}
                <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                  <div className="p-5 border-b border-slate-100 bg-red-50/50">
                    <h3 className="font-bold text-slate-900 flex items-center gap-2">
                      <AlertTriangle className="w-5 h-5 text-red-500" /> Critical Findings Requiring Attention
                    </h3>
                  </div>
                  <div className="p-0">
                    <ul className="divide-y divide-slate-100">
                      {reportData?.mismatches?.map((m: any, i: number) => (
                        <li key={`mis-${i}`} className="p-5 hover:bg-slate-50 transition-colors flex gap-4 items-start">
                          <div className="bg-red-100 p-2 rounded shrink-0"><AlertTriangle className="w-4 h-4 text-red-600" /></div>
                          <div>
                            <p className="text-sm font-bold text-slate-900 mb-1">{m.field} mismatch: {m.doc1} vs {m.doc2}</p>
                            <div className="flex gap-2 items-center text-xs">
                              <span className="text-slate-500 font-medium">Source: Cross-Document Consistency</span>
                            </div>
                          </div>
                        </li>
                      ))}
                      {reportData?.compliance?.map((c: any, i: number) => (
                        <li key={`comp-${i}`} className="p-5 hover:bg-slate-50 transition-colors flex gap-4 items-start">
                          <div className="bg-red-100 p-2 rounded shrink-0"><AlertTriangle className="w-4 h-4 text-red-600" /></div>
                          <div>
                            <p className="text-sm font-bold text-slate-900 mb-1">Compliance Failure: {c.rule}</p>
                            <div className="flex gap-2 items-center text-xs">
                              <span className="text-slate-500 font-medium">Details: {c.details}</span>
                            </div>
                          </div>
                        </li>
                      ))}
                      {reportData?.fraud_dna?.map((f: any, i: number) => (
                        <li key={`dna-${i}`} className="p-5 hover:bg-slate-50 transition-colors flex gap-4 items-start">
                          <div className="bg-amber-100 p-2 rounded shrink-0"><AlertCircle className="w-4 h-4 text-amber-600" /></div>
                          <div>
                            <p className="text-sm font-bold text-slate-900 mb-1">Fraud Pattern Match: {f.pattern}</p>
                            <div className="flex gap-2 items-center text-xs">
                              <span className="text-slate-500 font-medium">Source: Fraud DNA Network</span>
                              <span className="w-1 h-1 bg-slate-300 rounded-full"></span>
                              <span className="text-amber-600 font-bold">{Math.round(f.confidence * 100)}% Confidence</span>
                            </div>
                          </div>
                        </li>
                      ))}
                      {(!reportData || (!reportData.mismatches?.length && !reportData.compliance?.length && !reportData.fraud_dna?.length)) && (
                        <li className="p-5 text-slate-500 text-sm">No critical findings detected.</li>
                      )}
                    </ul>
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                  <h3 className="font-bold text-slate-900 mb-6">Score Breakdown (The 7 Layers)</h3>
                  <div className="space-y-4">
                    {[
                      { name: 'Document Authenticity', score: reportData?.risk_scores?.composite || 0, color: 'bg-red-500' },
                      { name: 'Cross-Document Consistency', score: reportData?.risk_scores?.composite || 0, color: 'bg-red-500' },
                      { name: 'Compliance Checks', score: reportData?.risk_scores?.composite || 0, color: 'bg-amber-500' },
                    ].map(layer => (
                      <div key={layer.name}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="font-medium text-slate-700">{layer.name}</span>
                          <span className="font-bold text-slate-900">{layer.score}/100</span>
                        </div>
                        <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                          <div className={`h-full ${layer.color}`} style={{ width: `${layer.score}%` }}></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                
                {/* AI Recommendation */}
                <div className="bg-gradient-to-b from-slate-900 to-[#0B1121] rounded-2xl shadow-lg border border-slate-800 p-6 text-white relative overflow-hidden">
                  <div className="absolute top-0 right-0 p-4 opacity-10"><Brain className="w-24 h-24" /></div>
                  <div className="relative z-10">
                    <div className="flex items-center gap-2 text-primary-400 font-bold text-sm uppercase tracking-wider mb-2">
                      <Brain className="w-4 h-4" /> AI Recommendation
                    </div>
                    <div className={`inline-block font-bold border px-3 py-1 rounded mb-4 text-sm ${isHighRisk ? 'bg-red-500/20 text-red-400 border-red-500/30' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'}`}>
                      {reportData?.final_decision?.decision?.toUpperCase() || (isHighRisk ? 'REJECT' : 'APPROVE')}
                    </div>
                    <ul className="text-slate-300 text-sm leading-relaxed mb-6 list-disc list-inside">
                      {reportData?.final_decision?.reasoning?.map((reason: string, idx: number) => (
                        <li key={idx}>{reason}</li>
                      ))}
                    </ul>
                    <Button onClick={() => setActiveTab('Decision')} className="w-full bg-primary hover:bg-primary-600 text-white border-0">
                      Make Final Decision
                    </Button>
                  </div>
                </div>

                {/* Timeline */}
                <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                  <h3 className="font-bold text-slate-900 mb-6">Case Timeline</h3>
                  <div className="relative border-l-2 border-slate-100 ml-3 space-y-6">
                    <div className="relative">
                      <div className="absolute -left-[29px] bg-emerald-100 border-2 border-white rounded-full p-1"><CheckCircle2 className="w-4 h-4 text-emerald-600" /></div>
                      <p className="text-sm font-bold text-slate-900 ml-4">Case Created</p>
                      <p className="text-xs text-slate-500 ml-4">Jan 15, 2025 at 10:30 AM</p>
                    </div>
                    <div className="relative">
                      <div className="absolute -left-[29px] bg-emerald-100 border-2 border-white rounded-full p-1"><CheckCircle2 className="w-4 h-4 text-emerald-600" /></div>
                      <p className="text-sm font-bold text-slate-900 ml-4">8 Documents Uploaded</p>
                      <p className="text-xs text-slate-500 ml-4">Jan 15, 2025 at 10:35 AM</p>
                    </div>
                    <div className="relative">
                      <div className="absolute -left-[29px] bg-emerald-100 border-2 border-white rounded-full p-1"><CheckCircle2 className="w-4 h-4 text-emerald-600" /></div>
                      <p className="text-sm font-bold text-slate-900 ml-4">AI Analysis Complete</p>
                      <p className="text-xs text-slate-500 ml-4">Duration: 87 seconds</p>
                    </div>
                    <div className="relative">
                      <div className="absolute -left-[29px] bg-slate-100 border-2 border-white rounded-full p-1"><div className="w-4 h-4 bg-slate-300 rounded-full m-1"></div></div>
                      <p className="text-sm font-bold text-slate-900 ml-4">Awaiting Decision</p>
                      <p className="text-xs text-slate-500 ml-4">Assigned to Rahul S.</p>
                    </div>
                  </div>
                </div>
              </div>
              
            </div>
          )}
          
          {activeTab === 'Documents' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input type="text" placeholder="Search files..." className="pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm outline-none focus:border-primary" />
                  </div>
                  <select className="border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-700 outline-none focus:border-primary">
                    <option>All Types</option>
                    <option>ITR</option>
                    <option>Sale Deed</option>
                  </select>
                </div>
                <div className="flex items-center bg-slate-100 rounded-lg p-1 border border-slate-200">
                  <button onClick={() => setDocView('grid')} className={`p-1.5 rounded ${docView === 'grid' ? 'bg-white shadow-sm' : 'text-slate-500'}`}><Grid className="w-4 h-4" /></button>
                  <button onClick={() => setDocView('list')} className={`p-1.5 rounded ${docView === 'list' ? 'bg-white shadow-sm' : 'text-slate-500'}`}><List className="w-4 h-4" /></button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  { id: 'doc-1', name: 'rajesh_itr_2024.pdf', type: 'ITR', size: '2.4 MB', issues: 1, score: 28 },
                  { id: 'doc-2', name: 'sale_deed_signed.pdf', type: 'Sale Deed', size: '5.1 MB', issues: 3, score: 12 },
                  { id: 'doc-3', name: 'bank_statement_6m.pdf', type: 'Bank Statement', size: '1.2 MB', issues: 0, score: 98 },
                  { id: 'doc-4', name: 'pan_card_front.jpg', type: 'PAN Card', size: '0.8 MB', issues: 0, score: 100 },
                ].map(doc => (
                  <Link href={`/cases/${params.id}/documents/${doc.id}`} key={doc.id}>
                    <div className="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md hover:border-primary/50 transition-all cursor-pointer group flex flex-col h-full overflow-hidden">
                      <div className="h-32 bg-slate-100 flex items-center justify-center border-b border-slate-200 relative">
                        <FileText className="w-12 h-12 text-slate-300" />
                        {doc.issues > 0 && (
                          <div className="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded shadow-sm">
                            {doc.issues} Issues
                          </div>
                        )}
                      </div>
                      <div className="p-4 flex-1 flex flex-col">
                        <div className="flex justify-between items-start mb-2">
                          <span className="text-xs font-bold bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-100">{doc.type}</span>
                          <span className={`text-xs font-bold px-2 py-0.5 rounded border ${doc.score > 80 ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-red-50 text-red-700 border-red-100'}`}>Score: {doc.score}</span>
                        </div>
                        <h4 className="text-sm font-bold text-slate-900 truncate mb-1 group-hover:text-primary">{doc.name}</h4>
                        <p className="text-xs text-slate-500 mt-auto">{doc.size} • Processed</p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'Decision' && (
            <div className="max-w-4xl mx-auto space-y-8">
              <div className="text-center mb-10">
                <h2 className="text-3xl font-bold text-slate-900 mb-3">Make Final Decision</h2>
                <p className="text-slate-500">Review the AI recommendations and finalize the application status.</p>
              </div>

              <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-8 text-center">
                <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-3" />
                <h3 className="text-xl font-bold text-red-900 mb-2">AI Recommends: REJECT</h3>
                <p className="text-red-700 text-sm max-w-2xl mx-auto">Critical forgery detected in primary collateral (Sale Deed). Extensive cross-document mismatches indicate systematic misrepresentation of financial capacity.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Approve */}
                <div className="bg-white rounded-2xl border border-slate-200 p-6 opacity-60 hover:opacity-100 transition-opacity flex flex-col h-full cursor-not-allowed">
                  <div className="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mb-4"><Check className="w-6 h-6 text-emerald-600" /></div>
                  <h3 className="text-lg font-bold text-slate-900 mb-2">Approve</h3>
                  <p className="text-sm text-slate-500 mb-6 flex-1">Approve the loan application and proceed to disbursement.</p>
                  <Button disabled className="w-full bg-slate-100 text-slate-400">Override & Approve</Button>
                </div>

                {/* Flag */}
                <div className="bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-md transition-shadow flex flex-col h-full hover:border-amber-300">
                  <div className="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center mb-4"><Flag className="w-6 h-6 text-amber-600" /></div>
                  <h3 className="text-lg font-bold text-slate-900 mb-2">Flag for Review</h3>
                  <p className="text-sm text-slate-500 mb-6 flex-1">Escalate to field investigation team or request physical originals.</p>
                  <Button className="w-full bg-amber-500 hover:bg-amber-600 text-white">Escalate Case</Button>
                </div>

                {/* Reject */}
                <div className="bg-white rounded-2xl border-2 border-red-500 p-6 shadow-md flex flex-col h-full relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/10 rounded-full blur-2xl pointer-events-none"></div>
                  <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mb-4"><X className="w-6 h-6 text-red-600" /></div>
                  <h3 className="text-lg font-bold text-slate-900 mb-2">Reject</h3>
                  <p className="text-sm text-slate-500 mb-4 flex-1">Deny the application based on fraudulent documentation.</p>
                  
                  <select className="w-full text-sm border border-slate-200 rounded-lg p-2 mb-4 outline-none focus:border-red-500 bg-slate-50">
                    <option>Select Reason...</option>
                    <option selected>Fraudulent/Forged Documents</option>
                    <option>Income Misrepresentation</option>
                  </select>
                  
                  <Button className="w-full bg-red-600 hover:bg-red-700 text-white shadow-lg shadow-red-500/30">Confirm Rejection</Button>
                </div>
              </div>
              
              <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm mt-8">
                <h4 className="font-bold text-slate-900 mb-3 flex items-center gap-2"><MessageSquare className="w-4 h-4 text-slate-400" /> Officer Notes (Internal)</h4>
                <textarea className="w-full border border-slate-200 rounded-lg p-3 text-sm min-h-[100px] outline-none focus:border-primary resize-none bg-slate-50" placeholder="Enter justification for decision..."></textarea>
              </div>
            </div>
          )}
          
          {activeTab === 'Network Intelligence' && (
            <div className="space-y-6">
              <div className="mb-4">
                <h2 className="text-2xl font-bold text-slate-900">Fraud Syndicate Intelligence</h2>
                <p className="text-slate-500">Cross-referencing entities against known fraud rings and historical cases.</p>
              </div>
              <FraudNetworkGraph caseId={params.id} token={token || ''} />
            </div>
          )}

          {activeTab === 'Fraud DNA' && (
            <div className="space-y-6 max-w-4xl mx-auto py-8">
              <div className="text-center mb-10">
                <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Fingerprint className="w-8 h-8 text-indigo-600" />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">Template Genetic Fingerprinting</h2>
                <p className="text-slate-500">Detecting serialized fraud by matching blank document structural layouts.</p>
              </div>
              
              <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
                <div className="flex items-center justify-between mb-6 border-b border-slate-100 pb-4">
                  <h3 className="font-bold text-slate-900 flex items-center gap-2"><Scan className="w-4 h-4 text-indigo-500" /> Layout pHash Analysis</h3>
                  <span className="bg-red-50 text-red-700 text-xs font-bold px-2 py-1 rounded border border-red-200">1 Match Found</span>
                </div>
                
                <div className="grid grid-cols-2 gap-8">
                  <div>
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Current Document (Sale Deed)</p>
                    <div className="aspect-[1/1.4] bg-slate-100 border-2 border-slate-200 rounded-lg relative overflow-hidden flex flex-col p-4 opacity-50">
                      <div className="w-full h-8 bg-slate-300 rounded mb-4" />
                      <div className="w-3/4 h-4 bg-slate-300 rounded mb-2" />
                      <div className="w-5/6 h-4 bg-slate-300 rounded mb-2" />
                      <div className="w-full h-40 bg-slate-300 rounded mt-4" />
                      <div className="absolute inset-0 bg-indigo-500/10 flex items-center justify-center backdrop-blur-[1px]">
                         <span className="bg-white px-3 py-1 rounded-full text-xs font-bold shadow text-indigo-700 font-mono">Hash: a4c3e8...</span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Known Fraud Template (Case TL-8891)</p>
                    <div className="aspect-[1/1.4] bg-red-50 border-2 border-red-200 rounded-lg relative overflow-hidden flex flex-col p-4 opacity-50">
                      <div className="w-full h-8 bg-red-300 rounded mb-4" />
                      <div className="w-3/4 h-4 bg-red-300 rounded mb-2" />
                      <div className="w-5/6 h-4 bg-red-300 rounded mb-2" />
                      <div className="w-full h-40 bg-red-300 rounded mt-4" />
                      <div className="absolute inset-0 bg-red-500/10 flex items-center justify-center backdrop-blur-[1px]">
                         <span className="bg-white px-3 py-1 rounded-full text-xs font-bold shadow text-red-700 font-mono">Hash: a4c3e8...</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-bold text-amber-900 text-sm">Serial Fraud Template Detected</h4>
                    <p className="text-sm text-amber-800 mt-1">The structural layout of this document is a <span className="font-bold">99.8% match</span> to a known forged template used by &quot;Fraud Ring Alpha&quot;. The text contents have been altered, but the base template is identical.</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Placeholder for other tabs during demo */}
          {activeTab !== 'Overview' && activeTab !== 'Documents' && activeTab !== 'Decision' && activeTab !== 'Network Intelligence' && activeTab !== 'Fraud DNA' && (
            <div className="py-20 text-center">
              <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Scan className="w-8 h-8 text-slate-400" />
              </div>
              <h3 className="text-xl font-bold text-slate-700 mb-2">{activeTab} View</h3>
              <p className="text-slate-500">Select a specific document or comparison to view detailed intelligence.</p>
            </div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Floating Chat Components */}
      {token && (
        <>
          <CaseChat 
            caseId={params.id} 
            token={token} 
            isOpen={isChatOpen} 
            onClose={() => setIsChatOpen(false)} 
          />
          <CaseChatButton 
            isOpen={isChatOpen} 
            onClick={() => setIsChatOpen(!isChatOpen)} 
          />
        </>
      )}
    </div>
  )
}

function HomeIcon({ className }: { className?: string }) {
  return <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
}
function GitCompareIcon({ className }: { className?: string }) {
  return <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M11 18H8a2 2 0 0 1-2-2V9"/></svg>
}
