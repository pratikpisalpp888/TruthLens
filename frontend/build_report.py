import os

files = {
    "app/(protected)/cases/[id]/report/page.tsx": """'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, Download, Printer, Share2, FileSignature, ShieldAlert, CheckCircle2, AlertTriangle, Info, MapPin } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function AIReportPage({ params }: { params: { id: string } }) {

  return (
    <div className="min-h-screen bg-slate-100 pb-20 -mx-6 -my-8 absolute inset-0 top-16 z-40 overflow-auto">
      
      {/* Sticky Action Toolbar */}
      <div className="sticky top-0 z-50 bg-white border-b border-slate-200 px-6 py-3 shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href={`/cases/${params.id}`} className="text-slate-400 hover:text-primary transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-sm font-bold text-slate-900">Forensic Analysis Report</h1>
            <p className="text-xs text-slate-500">RPT-TL-{params.id}-001</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" className="h-8 text-xs font-medium border-slate-300">
            <Printer className="w-3.5 h-3.5 mr-2" /> Print
          </Button>
          <Button variant="outline" size="sm" className="h-8 text-xs font-medium border-slate-300">
            <Share2 className="w-3.5 h-3.5 mr-2" /> Share
          </Button>
          <Button size="sm" className="h-8 text-xs font-medium bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-md">
            <Download className="w-3.5 h-3.5 mr-2" /> Download PDF
          </Button>
        </div>
      </div>

      {/* A4 Document Container */}
      <div className="max-w-[850px] mx-auto mt-8 bg-white shadow-xl shadow-slate-200/50 border border-slate-200 font-serif">
        
        {/* Document Header */}
        <div className="border-b-4 border-slate-900 p-10 pb-6 flex justify-between items-end relative overflow-hidden">
          {/* Subtle watermark */}
          <div className="absolute top-0 right-0 -mr-20 -mt-10 opacity-5 pointer-events-none">
            <ShieldAlert className="w-96 h-96" />
          </div>
          
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-blue-600 rounded flex items-center justify-center shadow-lg">
                <span className="text-white font-sans font-black text-xl tracking-tighter">TL</span>
              </div>
              <div>
                <h2 className="text-2xl font-black font-sans text-slate-900 tracking-tight">TruthLens</h2>
                <p className="text-xs font-sans font-bold text-blue-600 uppercase tracking-widest">AI Forensics</p>
              </div>
            </div>
            
            <h1 className="text-3xl font-bold text-slate-900 mb-2">Forensic Analysis Report</h1>
            <p className="text-sm font-bold text-red-600 border border-red-200 bg-red-50 inline-block px-2 py-1 rounded">CONFIDENTIAL - RESTRICTED ACCESS</p>
          </div>

          <div className="text-right text-xs text-slate-600 space-y-1 relative z-10">
            <p><span className="font-bold text-slate-900">Report ID:</span> RPT-TL-{params.id}-001</p>
            <p><span className="font-bold text-slate-900">Generated:</span> Jan 15, 2025 at 11:47 AM</p>
            <p><span className="font-bold text-slate-900">Version:</span> 1.0 (Final)</p>
            <p><span className="font-bold text-slate-900">Institution:</span> Canara Bank, Pune</p>
          </div>
        </div>

        <div className="p-10 space-y-10 text-slate-800 text-[15px] leading-relaxed">
          
          {/* 1. Executive Summary */}
          <section>
            <h2 className="text-xl font-bold font-sans text-slate-900 border-b border-slate-200 pb-2 mb-4 uppercase tracking-wider">1. Executive Summary</h2>
            
            <div className="flex items-start gap-6 mb-6">
              <div className="flex-1 bg-slate-50 border border-slate-200 rounded p-4">
                <table className="w-full text-sm">
                  <tbody>
                    <tr><td className="py-1 font-bold w-1/3">Applicant:</td><td className="py-1">Rajesh Kumar</td></tr>
                    <tr><td className="py-1 font-bold">PAN Number:</td><td className="py-1 font-mono text-xs bg-slate-200 px-1 rounded">ABCXX****F</td></tr>
                    <tr><td className="py-1 font-bold">Loan Purpose:</td><td className="py-1">Home Loan (₹45,00,000)</td></tr>
                    <tr><td className="py-1 font-bold">Officer:</td><td className="py-1">Rahul Sharma</td></tr>
                  </tbody>
                </table>
              </div>
              
              <div className="w-48 bg-red-50 border-2 border-red-500 rounded p-4 text-center shrink-0">
                <p className="text-xs font-bold text-red-700 uppercase mb-1">AI Trust Score</p>
                <div className="text-4xl font-black text-red-600 mb-1">18<span className="text-xl text-red-400">/100</span></div>
                <div className="bg-red-600 text-white text-[10px] font-bold py-1 px-2 rounded-sm uppercase tracking-widest mt-2">Critical Risk</div>
              </div>
            </div>

            <p className="mb-4">
              This forensic analysis identifies critical fraud indicators in the loan application submitted by Rajesh Kumar. 
              The comprehensive multi-layer analysis reveals significant document tampering, cross-document inconsistencies, 
              and matches with established fraud patterns. Immediate action is recommended before any approval consideration.
            </p>

            <div className="bg-white border-l-4 border-red-500 p-4 shadow-sm mb-4">
              <h3 className="font-bold text-red-800 font-sans text-sm uppercase mb-2">Key Findings Summary:</h3>
              <ul className="list-disc pl-5 space-y-1 text-sm">
                <li>Sale deed modification detected 3 days prior to submission (Metadata anomaly).</li>
                <li>Income declaration shows 860% deviation from official bank transaction records.</li>
                <li>Property area discrepancy of 178% between sale deed and revenue records.</li>
                <li>Match with 3 previously confirmed fraud cases in Pune region (89% similarity).</li>
              </ul>
            </div>
            
            <div className="bg-red-600 text-white font-bold p-3 text-center rounded shadow-md uppercase tracking-wider text-sm">
              Flag for Review - Immediate Escalation Required
            </div>
          </section>

          {/* 2. Detailed Findings (Authenticity) */}
          <section>
            <h2 className="text-xl font-bold font-sans text-slate-900 border-b border-slate-200 pb-2 mb-4 uppercase tracking-wider">2. Document Authenticity Findings</h2>
            
            <div className="space-y-6">
              <div className="border border-slate-200 rounded-lg overflow-hidden page-break-inside-avoid">
                <div className="bg-slate-50 border-b border-slate-200 px-4 py-3 flex justify-between items-center">
                  <h3 className="font-bold text-slate-900">Finding 2.1: Sale Deed Metadata Anomaly</h3>
                  <span className="bg-red-100 text-red-700 text-xs font-bold px-2 py-0.5 rounded border border-red-200">Severity: CRITICAL</span>
                </div>
                <div className="p-4">
                  <p className="text-sm mb-3">
                    The submitted sale deed PDF metadata reveals a creation date of January 12, 2025, while the document is dated May 15, 2019. 
                    Additionally, the document was created using Adobe Photoshop, which is inconsistent with legitimate legal document preparation.
                  </p>
                  <div className="bg-slate-50 p-3 rounded border border-slate-200 text-sm font-mono mb-4">
                    <div className="grid grid-cols-2 gap-2">
                      <div className="text-slate-500">PDF Creation Date:</div><div className="text-red-600">2025-01-12 15:32:44</div>
                      <div className="text-slate-500">Document Claimed Date:</div><div>2019-05-15</div>
                      <div className="text-slate-500">Creator Software:</div><div className="text-red-600">Adobe Photoshop 24.0</div>
                    </div>
                  </div>
                  <div className="bg-blue-50 border border-blue-200 p-3 rounded-lg text-sm flex gap-3">
                    <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                    <div>
                      <p className="font-bold text-blue-900 mb-1 text-xs uppercase tracking-wider">Regulatory Citation (RAG System)</p>
                      <p className="text-blue-800 text-xs italic">
                        "Per RBI Master Direction on KYC (RBI/DBR/2015-16/18 Section 4.3), documents presenting physical or digital metadata inconsistencies require enhanced verification procedures."
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border border-slate-200 rounded-lg overflow-hidden page-break-inside-avoid">
                <div className="bg-slate-50 border-b border-slate-200 px-4 py-3 flex justify-between items-center">
                  <h3 className="font-bold text-slate-900">Finding 2.2: ELA Detected Editing (ITR)</h3>
                  <span className="bg-red-100 text-red-700 text-xs font-bold px-2 py-0.5 rounded border border-red-200">Severity: HIGH</span>
                </div>
                <div className="p-4">
                  <p className="text-sm mb-3">
                    Error Level Analysis (ELA) detected significant editing artifacts in the income field region of the ITR document. 
                    The pixel-level analysis reveals digital manipulation of the declared income figures.
                  </p>
                  <a href={`/cases/${params.id}/documents/doc-1`} className="text-sm font-bold text-primary hover:underline flex items-center gap-1">
                    View Forensic Heatmap Evidence <ArrowLeft className="w-3 h-3 rotate-[135deg]" />
                  </a>
                </div>
              </div>
            </div>
          </section>

          {/* 3. Detailed Findings (Consistency) */}
          <section>
            <h2 className="text-xl font-bold font-sans text-slate-900 border-b border-slate-200 pb-2 mb-4 uppercase tracking-wider">3. Cross-Document Verification</h2>
            
            <div className="border border-slate-200 rounded-lg overflow-hidden page-break-inside-avoid">
              <div className="bg-slate-50 border-b border-slate-200 px-4 py-3 flex justify-between items-center">
                <h3 className="font-bold text-slate-900">Finding 3.1: Massive Land Area Discrepancy</h3>
                <span className="bg-red-100 text-red-700 text-xs font-bold px-2 py-0.5 rounded border border-red-200">Severity: CRITICAL</span>
              </div>
              <div className="p-0">
                <table className="w-full text-sm text-left">
                  <thead className="bg-slate-100 text-slate-600">
                    <tr><th className="px-4 py-2 border-b border-slate-200">Field Tested</th><th className="px-4 py-2 border-b border-slate-200">Sale Deed (Doc A)</th><th className="px-4 py-2 border-b border-slate-200">Revenue Record (Doc B)</th><th className="px-4 py-2 border-b border-slate-200">Variance</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="px-4 py-3 border-b border-slate-100 font-bold">Land Area</td>
                      <td className="px-4 py-3 border-b border-slate-100 font-mono text-red-600">5.0 Acres</td>
                      <td className="px-4 py-3 border-b border-slate-100 font-mono">1.8 Acres</td>
                      <td className="px-4 py-3 border-b border-slate-100 text-red-600 font-bold">178% Mismatch</td>
                    </tr>
                    <tr>
                      <td className="px-4 py-3 border-b border-slate-100 font-bold">Property Value</td>
                      <td className="px-4 py-3 border-b border-slate-100 font-mono text-amber-600">₹45,00,000</td>
                      <td className="px-4 py-3 border-b border-slate-100 font-mono">₹30,00,000</td>
                      <td className="px-4 py-3 border-b border-slate-100 text-amber-600 font-bold">50% Mismatch</td>
                    </tr>
                  </tbody>
                </table>
                <div className="p-4 bg-white">
                  <div className="bg-blue-50 border border-blue-200 p-3 rounded-lg text-sm flex gap-3">
                    <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                    <div>
                      <p className="font-bold text-blue-900 mb-1 text-xs uppercase tracking-wider">Regulatory Citation (RAG System)</p>
                      <p className="text-blue-800 text-xs italic">
                        "Per Canara Bank Property Verification Manual (Section 3.2), cross-document measurement mismatches exceeding 10% require mandatory physical verification."
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 4. Fraud Network */}
          <section>
            <h2 className="text-xl font-bold font-sans text-slate-900 border-b border-slate-200 pb-2 mb-4 uppercase tracking-wider">4. Fraud Network Intelligence</h2>
            
            <p className="text-sm mb-4">
              GraphRAG analysis indicates this case is connected to a suspected organized fraud ring involving 5 other loan applications spanning the past 6 months.
            </p>

            <div className="bg-slate-50 border border-slate-200 rounded p-4 mb-4 page-break-inside-avoid">
              <h3 className="font-bold text-slate-800 mb-3 text-sm">Common Elements Detected in Fraud Ring:</h3>
              <ol className="list-decimal pl-5 space-y-2 text-sm text-slate-700">
                <li><span className="font-bold">Notary Connection:</span> All documents notarized by "John D. (Baner Office)".</li>
                <li><span className="font-bold">Printer Fingerprint:</span> Documents across 4 cases printed from identical hardware.</li>
                <li><span className="font-bold">Pattern Match:</span> High correlation with "Income Inflation Type-B" methodology.</li>
              </ol>
            </div>
          </section>

          {/* Signatures */}
          <section className="pt-12 mt-12 border-t-2 border-slate-200 flex justify-between page-break-inside-avoid">
            <div className="w-64 text-center">
              <div className="h-16 flex items-center justify-center">
                <FileSignature className="w-8 h-8 text-slate-300" />
              </div>
              <div className="border-t border-slate-400 pt-2">
                <p className="font-bold text-slate-900 text-sm">TruthLens AI System</p>
                <p className="text-xs text-slate-500">Automated Signature</p>
              </div>
            </div>
            <div className="w-64 text-center">
              <div className="h-16"></div>
              <div className="border-t border-slate-400 pt-2">
                <p className="font-bold text-slate-900 text-sm">Authorized Officer</p>
                <p className="text-xs text-slate-500">Signature & Date</p>
              </div>
            </div>
          </section>

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
    print("Scaffolded AI Report Page.")
