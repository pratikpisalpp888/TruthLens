import os

files = {
    "app/(protected)/cases/[id]/documents/[docId]/page.tsx": """'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, ZoomIn, ZoomOut, Maximize, RotateCw, FileText, Scan, FileSearch, Search, SlidersHorizontal, ChevronRight, AlertTriangle, ShieldAlert } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function DocumentViewerPage({ params }: { params: { id: string, docId: string } }) {
  const [activeTab, setActiveTab] = useState('Extracted Fields')
  const [showHeatmap, setShowHeatmap] = useState(true)
  
  const TABS = ['Extracted Fields', 'OCR Text', 'Named Entities', 'Forensic Findings']

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col bg-slate-100 overflow-hidden -mx-6 -my-8 absolute inset-0 top-16 z-40">
      
      {/* Top Action Bar */}
      <div className="bg-white border-b border-slate-200 px-4 py-2 flex justify-between items-center shrink-0">
        <div className="flex items-center gap-3">
          <Link href={`/cases/${params.id}`} className="p-2 hover:bg-slate-100 rounded-lg text-slate-500 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <span className="bg-red-50 text-red-700 text-[10px] font-bold px-2 py-0.5 rounded border border-red-100">Sale Deed</span>
              <h1 className="text-sm font-bold text-slate-900">sale_deed_signed.pdf</h1>
            </div>
            <p className="text-xs text-slate-500">Document 2 of 8 • Uploaded 2 hours ago</p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 bg-slate-100 p-1 rounded-lg border border-slate-200">
            <Button variant="ghost" size="icon" className="w-7 h-7 text-slate-600 hover:bg-white hover:shadow-sm"><ZoomOut className="w-4 h-4" /></Button>
            <span className="text-xs font-mono font-medium text-slate-600 w-10 text-center">100%</span>
            <Button variant="ghost" size="icon" className="w-7 h-7 text-slate-600 hover:bg-white hover:shadow-sm"><ZoomIn className="w-4 h-4" /></Button>
          </div>
          
          <div className="w-px h-6 bg-slate-200"></div>
          
          <div className="flex items-center gap-3">
            <label className="flex items-center gap-2 text-sm font-bold text-slate-700 cursor-pointer">
              <input 
                type="checkbox" 
                checked={showHeatmap} 
                onChange={(e) => setShowHeatmap(e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 text-red-500 focus:ring-red-500" 
              />
              <span className={showHeatmap ? 'text-red-600' : ''}>Show ELA Heatmap</span>
            </label>
            <Button size="sm" className="bg-primary hover:bg-primary-600">Export Report</Button>
          </div>
        </div>
      </div>

      {/* Main Split View */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Document Render Area (Left / Center) */}
        <div className="flex-1 flex flex-col bg-slate-200 relative overflow-hidden">
          <div className="absolute inset-0 p-8 overflow-auto flex items-center justify-center">
            
            {/* Simulated Document Container */}
            <div className="bg-white w-full max-w-[800px] aspect-[1/1.4] shadow-2xl relative border border-slate-200 p-12">
              {/* Document Mock Content */}
              <div className="font-serif opacity-40">
                <h1 className="text-3xl text-center mb-8 border-b-2 border-black pb-4">SALE DEED</h1>
                <p className="mb-4">THIS DEED OF SALE is made and executed on this 15th day of May 2019...</p>
                <div className="w-full h-[600px] bg-slate-100 border border-slate-200 mt-4 relative">
                  <div className="absolute inset-0 flex items-center justify-center text-slate-300">
                    [ Document Image Rendered Here ]
                  </div>
                  
                  {/* Heatmap Overlay Simulation */}
                  {showHeatmap && (
                    <div className="absolute inset-0 mix-blend-multiply pointer-events-none z-10">
                      {/* Safe Zones */}
                      <div className="absolute top-10 left-10 w-[60%] h-32 bg-emerald-400/20 blur-xl"></div>
                      
                      {/* Tampered Zones (Red) */}
                      <div className="absolute bottom-24 right-10 w-48 h-20 bg-red-600/40 blur-md border-2 border-red-500/50"></div>
                      <div className="absolute bottom-24 right-10 w-48 h-20 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPjxyZWN0IHdpZHRoPSI0IiBoZWlnaHQ9IjQiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIi8+PHBhdGggZD0iTTAgMEw0IDRaIiBzdHJva2U9IiNmZmYiIHN0cm9rZS1vcGFjaXR5PSIwLjMiLz48L3N2Zz4=')]"></div>
                      
                      {/* Date Alteration Zone */}
                      <div className="absolute top-12 right-20 w-32 h-10 bg-red-500/50 blur-sm border border-red-500/50"></div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Heatmap Legend */}
          {showHeatmap && (
            <div className="absolute bottom-6 right-6 bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-lg border border-slate-200 flex flex-col gap-2 z-20">
              <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">Error Level Analysis</h4>
              <div className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 bg-red-500 rounded-sm"></div> High Prob. Edit
              </div>
              <div className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 bg-amber-400 rounded-sm"></div> Artifacting
              </div>
              <div className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 bg-emerald-400/50 rounded-sm"></div> Baseline
              </div>
            </div>
          )}
        </div>

        {/* Intelligence Sidebar (Right) */}
        <div className="w-[450px] bg-white border-l border-slate-200 flex flex-col z-20 shrink-0">
          
          <div className="flex bg-slate-50 border-b border-slate-200">
            {TABS.map(tab => (
              <button 
                key={tab} 
                onClick={() => setActiveTab(tab)}
                className={`flex-1 py-3 text-[11px] font-bold uppercase tracking-wider text-center border-b-2 transition-colors ${activeTab === tab ? 'border-primary text-primary-700 bg-white' : 'border-transparent text-slate-500 hover:bg-slate-100'}`}
              >
                {tab.split(' ')[0]}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-y-auto p-5">
            {activeTab === 'Extracted Fields' && (
              <div className="space-y-4">
                <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 flex items-start gap-2 mb-6">
                  <Scan className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                  <p className="text-xs text-blue-800 font-medium">Auto-extracted via LayoutLMv3. Confidences below 80% are flagged amber.</p>
                </div>
                
                {[
                  { label: 'Document Date', val: '15/05/2019', conf: 98 },
                  { label: 'Seller Name', val: 'Suresh Menon', conf: 99 },
                  { label: 'Buyer Name', val: 'Rajesh Kumar', conf: 97 },
                  { label: 'Property Area', val: '5.0 Acres', conf: 64, flag: true },
                  { label: 'Sale Consideration', val: '₹45,00,000', conf: 92 },
                  { label: 'Survey Number', val: 'Sy. No 45/2A', conf: 88 },
                ].map((field, i) => (
                  <div key={i} className="group border-b border-slate-100 pb-3 last:border-0 hover:bg-slate-50 p-2 -mx-2 rounded">
                    <div className="flex justify-between items-start mb-1">
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">{field.label}</span>
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${field.flag ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'}`}>{field.conf}%</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-bold text-slate-900">{field.val}</span>
                      <button className="opacity-0 group-hover:opacity-100 text-[10px] text-primary hover:underline">Edit</button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'Forensic Findings' && (
              <div className="space-y-5">
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 shadow-sm">
                  <div className="flex items-center gap-2 text-red-700 font-bold mb-2">
                    <ShieldAlert className="w-5 h-5" /> High Risk Tampering Detected
                  </div>
                  <p className="text-xs text-red-900/80 mb-3">ELA and Metadata signatures indicate post-scan digital modification.</p>
                  
                  <div className="bg-white rounded border border-red-100 p-3 mb-3 relative overflow-hidden">
                    <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500"></div>
                    <h4 className="text-xs font-bold text-slate-900 mb-1">PDF Date Anomaly</h4>
                    <p className="text-[11px] text-slate-600">Document claims creation in 2019, but internal XMP metadata shows PDF generation on 2024-12-10.</p>
                  </div>

                  <div className="bg-white rounded border border-red-100 p-3 relative overflow-hidden">
                    <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500"></div>
                    <h4 className="text-xs font-bold text-slate-900 mb-1">ELA Hotspot: Property Area</h4>
                    <p className="text-[11px] text-slate-600">Error levels at coordinates (840, 230) deviate from document baseline by 400%, indicating copy-paste forgery.</p>
                  </div>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                  <h4 className="font-bold text-slate-800 text-sm mb-3">Metadata Signature</h4>
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between border-b border-slate-100 pb-1">
                      <span className="text-slate-500">Producer</span>
                      <span className="font-mono font-bold text-red-600">Adobe Photoshop 24.0</span>
                    </div>
                    <div className="flex justify-between border-b border-slate-100 pb-1">
                      <span className="text-slate-500">DPI</span>
                      <span className="font-mono font-medium">300</span>
                    </div>
                    <div className="flex justify-between border-b border-slate-100 pb-1">
                      <span className="text-slate-500">Color Space</span>
                      <span className="font-mono font-medium">RGB</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
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
    print("Scaffolded Document Viewer Page.")
