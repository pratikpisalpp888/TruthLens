import os

files = {
    "app/(protected)/cases/[id]/compare/page.tsx": """'use client'

import Link from 'next/link'
import { ArrowLeft, ZoomIn, ZoomOut, CheckCircle2, AlertTriangle, AlertCircle, X, Download } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function CompareDocumentsPage({ params }: { params: { id: string } }) {

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col bg-slate-50 overflow-hidden -mx-6 -my-8 absolute inset-0 top-16 z-40">
      
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-4 shrink-0 shadow-sm z-10">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <Link href={`/cases/${params.id}`} className="text-slate-400 hover:text-primary transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <h1 className="text-xl font-bold text-slate-900">Cross-Document Comparison</h1>
              <p className="text-sm text-slate-500">Case {params.id}</p>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3 bg-red-50 px-4 py-2 rounded-lg border border-red-100">
              <span className="text-sm font-bold text-red-900">Consistency Score</span>
              <span className="text-xl font-bold text-red-600">23/100</span>
            </div>
            <Button variant="outline" className="border-slate-300 text-slate-700">
              <Download className="w-4 h-4 mr-2" /> Export PDF
            </Button>
          </div>
        </div>

        {/* Document Selectors */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Document A</label>
            <select className="bg-white border border-slate-300 rounded-lg p-2.5 text-sm font-bold text-slate-800 shadow-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary">
              <option>sale_deed_signed.pdf (Sale Deed)</option>
            </select>
          </div>
          <div className="flex flex-col">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Document B</label>
            <select className="bg-white border border-slate-300 rounded-lg p-2.5 text-sm font-bold text-slate-800 shadow-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary">
              <option>revenue_record_712.pdf (Revenue Record)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Split View */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Document A */}
        <div className="flex-1 flex flex-col border-r border-slate-300 relative bg-slate-200">
          <div className="absolute inset-0 p-8 overflow-auto flex items-center justify-center">
            <div className="bg-white w-full max-w-[600px] aspect-[1/1.4] shadow-xl relative border border-slate-200 p-8 font-serif opacity-50">
              <h2 className="text-2xl text-center mb-6">SALE DEED</h2>
              <p className="mb-4 text-sm leading-relaxed">THIS DEED OF SALE made and executed on...</p>
              
              {/* Highlight Simulation */}
              <div className="absolute top-[250px] left-[60px] w-48 h-8 border-2 border-red-500 bg-red-500/10 rounded cursor-pointer group">
                <span className="absolute -top-6 left-0 bg-red-500 text-white text-[10px] font-bold px-1.5 rounded shadow-sm opacity-0 group-hover:opacity-100 transition-opacity">Land Area: 5 Acres</span>
              </div>
            </div>
          </div>
        </div>

        {/* Document B */}
        <div className="flex-1 flex flex-col relative bg-slate-200">
          <div className="absolute inset-0 p-8 overflow-auto flex items-center justify-center">
            <div className="bg-white w-full max-w-[600px] aspect-[1/1.4] shadow-xl relative border border-slate-200 p-8 font-serif opacity-50">
              <h2 className="text-2xl text-center mb-6">REVENUE RECORD (7/12)</h2>
              <p className="mb-4 text-sm leading-relaxed">Village: Pune, Taluka: Haveli...</p>
              
              {/* Highlight Simulation */}
              <div className="absolute top-[320px] left-[120px] w-32 h-8 border-2 border-red-500 bg-red-500/10 rounded cursor-pointer group">
                <span className="absolute -top-6 left-0 bg-red-500 text-white text-[10px] font-bold px-1.5 rounded shadow-sm opacity-0 group-hover:opacity-100 transition-opacity">Land Area: 1.8 Acres</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Visual Connector Overlay Simulation (Absolute Center) */}
        <div className="absolute left-1/2 top-[40%] -translate-x-1/2 -translate-y-1/2 z-20 pointer-events-none">
          <svg width="200" height="100" className="opacity-60 overflow-visible">
            <path d="M 0,0 C 100,0 100,70 200,70" fill="transparent" stroke="red" strokeWidth="3" strokeDasharray="5,5" className="animate-[dash_1s_linear_infinite]" />
          </svg>
        </div>
      </div>

      {/* Mismatch Table (Bottom Panel) */}
      <div className="h-[250px] bg-white border-t border-slate-300 shadow-[0_-10px_20px_-10px_rgba(0,0,0,0.1)] z-30 flex flex-col">
        <div className="p-3 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
          <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" /> Detected Discrepancies (2)
          </h3>
          <div className="text-xs font-bold text-slate-500">6 fields compared total</div>
        </div>
        
        <div className="flex-1 overflow-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-500 bg-slate-50 uppercase font-semibold sticky top-0 border-b border-slate-200">
              <tr>
                <th className="px-4 py-2">Field</th>
                <th className="px-4 py-2">Document A (Sale Deed)</th>
                <th className="px-4 py-2">Document B (Revenue)</th>
                <th className="px-4 py-2">Match Status</th>
                <th className="px-4 py-2 w-1/3">Analysis</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              
              <tr className="hover:bg-red-50/50 cursor-pointer transition-colors bg-red-50/20">
                <td className="px-4 py-3 font-bold text-slate-900">Land Area</td>
                <td className="px-4 py-3 font-mono text-red-700">5.0 Acres</td>
                <td className="px-4 py-3 font-mono text-red-700">1.8 Acres</td>
                <td className="px-4 py-3">
                  <span className="inline-flex items-center gap-1 bg-red-100 text-red-700 px-2 py-0.5 rounded text-xs font-bold"><X className="w-3 h-3" /> MISMATCH</span>
                </td>
                <td className="px-4 py-3 text-xs text-red-900/80">178% variance detected. Highly suspicious inflation of property size in Sale Deed.</td>
              </tr>
              
              <tr className="hover:bg-amber-50/50 cursor-pointer transition-colors bg-amber-50/20">
                <td className="px-4 py-3 font-bold text-slate-900">Property Value</td>
                <td className="px-4 py-3 font-mono text-amber-700">₹45,00,000</td>
                <td className="px-4 py-3 font-mono text-amber-700">₹30,00,000</td>
                <td className="px-4 py-3">
                  <span className="inline-flex items-center gap-1 bg-amber-100 text-amber-700 px-2 py-0.5 rounded text-xs font-bold"><AlertCircle className="w-3 h-3" /> VARIANCE</span>
                </td>
                <td className="px-4 py-3 text-xs text-amber-900/80">50% variance in valuation between declared deed value and govt assessed value.</td>
              </tr>
              
              <tr className="hover:bg-slate-50 cursor-pointer transition-colors opacity-60">
                <td className="px-4 py-3 font-bold text-slate-900">Applicant Name</td>
                <td className="px-4 py-3 font-mono">Rajesh Kumar</td>
                <td className="px-4 py-3 font-mono">Rajesh Kumar</td>
                <td className="px-4 py-3">
                  <span className="inline-flex items-center gap-1 bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded text-xs font-bold"><CheckCircle2 className="w-3 h-3" /> MATCH</span>
                </td>
                <td className="px-4 py-3 text-xs text-slate-600">Exact string match (100% confidence).</td>
              </tr>
              
            </tbody>
          </table>
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
    print("Scaffolded Compare Documents Page.")
