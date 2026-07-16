import os

files = {
    "app/(protected)/cases/[id]/page.tsx": """'use client'

import { useState } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronRight, Download, Printer, Mic, FileText, CheckCircle2, AlertTriangle, AlertCircle, Scan, Brain, ExternalLink, Network, FileCheck, Landmark, Search, Grid, List, Check, X, Flag, MessageSquare } from 'lucide-react'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { Button } from '@/components/ui/button'

const TABS = ['Overview', 'Documents', 'Analysis (7 Layers)', 'Mismatches', 'Fraud DNA', 'Compliance', 'Report', 'Decision']

export default function CaseDetailPage({ params }: { params: { id: string } }) {
  const [activeTab, setActiveTab] = useState('Overview')
  const [docView, setDocView] = useState<'grid' | 'list'>('grid')

  return (
    <div className="max-w-[1400px] mx-auto pb-24">
      {/* Header Breadcrumbs */}
      <div className="mb-4">
        <Link href={`/cases`} className="text-sm text-slate-500 hover:text-primary flex items-center font-medium transition-colors w-max">
          Cases <ChevronRight className="w-4 h-4 mx-1" /> Case {params.id}
        </Link>
      </div>

      {/* Case Header Card */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-8 mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-red-500/5 rounded-full blur-[80px] pointer-events-none"></div>
        
        <div className="relative z-10 flex-1">
          <div className="flex items-center gap-4 mb-3">
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight">{params.id}</h1>
            <span className="bg-slate-100 text-slate-700 text-xs font-bold px-3 py-1 rounded border border-slate-200">Analyzed 15m ago</span>
          </div>
          <h2 className="text-2xl font-bold text-slate-800 mb-2">Rajesh Kumar</h2>
          <p className="text-slate-500 font-medium flex items-center gap-2 mb-4">
            <HomeIcon className="w-4 h-4" /> Home Loan • ₹45,00,000 • 20 years
          </p>
          
          <div className="flex flex-wrap gap-3">
            <Button className="bg-white text-slate-700 border-slate-200 shadow-sm hover:bg-slate-50">
              <Download className="w-4 h-4 mr-2" /> PDF Report
            </Button>
            <Button variant="outline" className="border-slate-200 text-slate-700 hover:bg-slate-50">
              <GitCompareIcon className="w-4 h-4 mr-2" /> Compare Docs
            </Button>
            <Button variant="outline" className="border-slate-200 text-slate-700 hover:bg-slate-50">
              <Network className="w-4 h-4 mr-2" /> Fraud Network
            </Button>
            <div className="w-px h-10 bg-slate-200 mx-1"></div>
            <Button variant="ghost" size="icon" className="text-slate-500 hover:text-primary"><Mic className="w-5 h-5" /></Button>
            <Button variant="ghost" size="icon" className="text-slate-500 hover:text-primary"><Printer className="w-5 h-5" /></Button>
          </div>
        </div>

        <div className="relative z-10 flex items-center gap-6 bg-slate-50 p-6 rounded-2xl border border-slate-100 min-w-[300px]">
          <div className="flex-1">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Overall Trust Score</p>
            <h3 className="text-xl font-bold text-slate-900 mb-2">Critical Fraud Risk</h3>
            <span className="inline-flex items-center gap-1.5 bg-red-100 text-red-700 text-xs font-bold px-2.5 py-1 rounded text-center">
              <AlertTriangle className="w-3.5 h-3.5" /> REJECT RECOMMENDED
            </span>
          </div>
          <div className="shrink-0">
            <TrustScoreGauge score={18} size="lg" />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200 mb-8 sticky top-0 bg-slate-50/80 backdrop-blur-md z-30 pt-2 -mx-4 px-4 sm:mx-0 sm:px-0">
        <nav className="flex space-x-1 sm:space-x-8 overflow-x-auto custom-scrollbar pb-px">
          {TABS.map((tab) => {
            const isActive = activeTab === tab
            const hasBadge = tab === 'Mismatches' || tab === 'Fraud DNA' || tab === 'Compliance'
            const badgeCount = tab === 'Mismatches' ? '6' : tab === 'Fraud DNA' ? '1' : '5'
            
            return (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`whitespace-nowrap py-4 px-3 sm:px-1 border-b-2 font-medium text-sm transition-colors relative
                  ${isActive ? 'border-primary text-primary-700' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`}
              >
                {tab}
                {hasBadge && (
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
                      <li className="p-5 hover:bg-slate-50 transition-colors flex gap-4 items-start">
                        <div className="bg-red-100 p-2 rounded shrink-0"><AlertTriangle className="w-4 h-4 text-red-600" /></div>
                        <div>
                          <p className="text-sm font-bold text-slate-900 mb-1">Sale deed PDF modified 3 days before submission despite being dated 2019</p>
                          <div className="flex gap-2 items-center text-xs">
                            <span className="text-slate-500 font-medium">Source: Document Forensics (ELA)</span>
                            <span className="w-1 h-1 bg-slate-300 rounded-full"></span>
                            <span className="text-red-600 font-bold">96% Confidence</span>
                          </div>
                        </div>
                      </li>
                      <li className="p-5 hover:bg-slate-50 transition-colors flex gap-4 items-start">
                        <div className="bg-red-100 p-2 rounded shrink-0"><AlertTriangle className="w-4 h-4 text-red-600" /></div>
                        <div>
                          <p className="text-sm font-bold text-slate-900 mb-1">Land area mismatch: 5 acres in deed vs 1.8 acres in revenue record</p>
                          <div className="flex gap-2 items-center text-xs">
                            <span className="text-slate-500 font-medium">Source: Cross-Document Consistency</span>
                            <span className="w-1 h-1 bg-slate-300 rounded-full"></span>
                            <Link href={`/cases/${params.id}/compare`} className="text-primary hover:underline font-bold">View Comparison</Link>
                          </div>
                        </div>
                      </li>
                      <li className="p-5 hover:bg-slate-50 transition-colors flex gap-4 items-start">
                        <div className="bg-red-100 p-2 rounded shrink-0"><AlertTriangle className="w-4 h-4 text-red-600" /></div>
                        <div>
                          <p className="text-sm font-bold text-slate-900 mb-1">ITR income ₹5 lakh vs bank credits ₹48 lakh (860% deviation)</p>
                          <div className="flex gap-2 items-center text-xs">
                            <span className="text-slate-500 font-medium">Source: ITR Special Verification</span>
                          </div>
                        </div>
                      </li>
                      <li className="p-5 hover:bg-slate-50 transition-colors flex gap-4 items-start">
                        <div className="bg-amber-100 p-2 rounded shrink-0"><AlertCircle className="w-4 h-4 text-amber-600" /></div>
                        <div>
                          <p className="text-sm font-bold text-slate-900 mb-1">Fraud Pattern Match: "Income Inflation Type-B"</p>
                          <div className="flex gap-2 items-center text-xs">
                            <span className="text-slate-500 font-medium">Source: Fraud DNA Network</span>
                            <span className="w-1 h-1 bg-slate-300 rounded-full"></span>
                            <span className="text-amber-600 font-bold">Matches 3 past cases</span>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>
                </div>

                {/* Score Breakdown (Simulated Radar Chart) */}
                <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                  <h3 className="font-bold text-slate-900 mb-6">Score Breakdown (The 7 Layers)</h3>
                  <div className="space-y-4">
                    {[
                      { name: 'Document Authenticity', score: 34, color: 'bg-red-500' },
                      { name: 'Cross-Document Consistency', score: 23, color: 'bg-red-500' },
                      { name: 'ITR Validity', score: 28, color: 'bg-red-500' },
                      { name: 'Compliance Checks', score: 45, color: 'bg-amber-500' },
                      { name: 'OCR Quality', score: 96, color: 'bg-emerald-500' },
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
                    <div className="inline-block bg-red-500/20 text-red-400 font-bold border border-red-500/30 px-3 py-1 rounded mb-4 text-sm">
                      FLAG FOR REVIEW
                    </div>
                    <p className="text-slate-300 text-sm leading-relaxed mb-6">
                      Multiple critical fraud indicators detected. Cross-document analysis reveals significant inconsistencies in income declarations and property details. Document forensics identified tampering with high confidence.
                    </p>
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
          
          {/* Placeholder for other tabs during demo */}
          {activeTab !== 'Overview' && activeTab !== 'Documents' && activeTab !== 'Decision' && (
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
    </div>
  )
}

function HomeIcon({ className }: { className?: string }) {
  return <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
}
function GitCompareIcon({ className }: { className?: string }) {
  return <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M11 18H8a2 2 0 0 1-2-2V9"/></svg>
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
    print("Scaffolded Case Detail Page.")
