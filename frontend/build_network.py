import os

files = {
    "app/(protected)/cases/[id]/network/page.tsx": """'use client'

import { useState } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, X, Briefcase, User, MapPin, Stamp, Fingerprint, ZoomIn, ZoomOut, Maximize, MousePointer2, AlertTriangle, Network, Download } from 'lucide-react'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { Button } from '@/components/ui/button'

export default function FraudNetworkPage({ params }: { params: { id: string } }) {
  const [selectedNode, setSelectedNode] = useState<string | null>(null)
  
  // Simulated node data for demo
  const mockNode = {
    id: 'notary-1',
    type: 'notary',
    name: 'John D.',
    location: 'Baner Office, Pune',
    cases: 15,
    flagged: 7,
    score: 78
  }

  return (
    <div className="fixed inset-0 z-50 bg-[#0B1121] overflow-hidden flex flex-col font-sans">
      
      {/* Background Grid */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgyNTUsMjU1LDI1NSwwLjAyKSIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')]"></div>

      {/* Header */}
      <header className="relative z-20 flex items-center justify-between px-6 py-4 border-b border-slate-800/80 bg-[#0B1121]/90 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href={`/cases/${params.id}`} className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-xl font-bold text-white flex items-center gap-2">
              <Network className="w-5 h-5 text-primary-400" /> Fraud Network Analysis
            </h1>
            <p className="text-xs text-slate-400 font-mono mt-0.5">Powered by GraphRAG • Case {params.id}</p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex gap-4 text-sm bg-slate-900/50 px-4 py-2 rounded-lg border border-slate-800">
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-500 uppercase font-bold">Connections</span>
              <span className="text-white font-mono font-bold">12</span>
            </div>
            <div className="w-px h-8 bg-slate-800"></div>
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-500 uppercase font-bold">Fraud Rings</span>
              <span className="text-red-400 font-mono font-bold">1</span>
            </div>
            <div className="w-px h-8 bg-slate-800"></div>
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-500 uppercase font-bold">Suspicion</span>
              <span className="text-amber-400 font-mono font-bold">89%</span>
            </div>
          </div>
          <Button variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white">
            <Download className="w-4 h-4 mr-2" /> Export
          </Button>
        </div>
      </header>

      {/* Main Canvas Area */}
      <div className="flex-1 relative overflow-hidden flex">
        
        {/* Left Toolbar (Filters & Layout) */}
        <div className="w-64 bg-slate-900/80 backdrop-blur-sm border-r border-slate-800/80 p-4 flex flex-col gap-6 z-20 shrink-0">
          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Entity Filters</h3>
            <div className="space-y-2">
              {[
                { label: 'Cases', color: 'bg-blue-500', count: 4 },
                { label: 'Applicants', color: 'bg-emerald-500', count: 3 },
                { label: 'Properties', color: 'bg-amber-500', count: 2 },
                { label: 'Notaries', color: 'bg-purple-500', count: 1 },
                { label: 'Fraud Patterns', color: 'bg-red-500', count: 2 },
              ].map(f => (
                <label key={f.label} className="flex items-center justify-between text-sm text-slate-300 cursor-pointer group hover:text-white">
                  <div className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked className={`rounded border-slate-700 bg-slate-800 text-primary focus:ring-0 focus:ring-offset-0`} />
                    <span className="flex items-center gap-1.5"><div className={`w-2 h-2 rounded-full ${f.color}`}></div> {f.label}</span>
                  </div>
                  <span className="text-xs font-mono text-slate-600 bg-slate-800 px-1.5 rounded">{f.count}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="w-full h-px bg-slate-800"></div>

          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">AI Insights</h3>
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-xs text-red-200">
              <AlertTriangle className="w-4 h-4 text-red-500 mb-1" />
              <p className="font-bold mb-1">Coordinated Ring Detected</p>
              <p className="opacity-80 leading-relaxed">5 loan applications share the same notary and locality. Document printer fingerprint analysis reveals 8 documents across these cases were printed from the same device.</p>
            </div>
          </div>
        </div>

        {/* Center Canvas (Simulated Graph) */}
        <div className="flex-1 relative cursor-grab active:cursor-grabbing">
          
          {/* Zoom Controls */}
          <div className="absolute bottom-6 right-6 flex flex-col gap-2 z-20">
            <Button variant="outline" size="icon" className="bg-slate-900/80 border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white"><ZoomIn className="w-5 h-5" /></Button>
            <Button variant="outline" size="icon" className="bg-slate-900/80 border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white"><ZoomOut className="w-5 h-5" /></Button>
            <Button variant="outline" size="icon" className="bg-slate-900/80 border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white"><Maximize className="w-5 h-5" /></Button>
          </div>

          {/* SIMULATED GRAPH RENDER */}
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none scale-110">
            <div className="relative w-[800px] h-[600px] pointer-events-auto">
              
              {/* Edges (SVG) */}
              <svg className="absolute inset-0 w-full h-full overflow-visible pointer-events-none z-0">
                {/* Current Case to Pattern */}
                <path d="M 400,300 Q 550,200 650,250" fill="transparent" stroke="#EF4444" strokeWidth="3" className="opacity-80 animate-[dash_2s_linear_infinite]" strokeDasharray="10,10" />
                {/* Connected Case to Pattern */}
                <path d="M 600,450 Q 625,350 650,250" fill="transparent" stroke="#EF4444" strokeWidth="2" className="opacity-50" />
                {/* Current Case to Applicant */}
                <path d="M 400,300 Q 250,250 200,350" fill="transparent" stroke="#10B981" strokeWidth="2" className="opacity-60" />
                {/* Current Case to Notary */}
                <path d="M 400,300 Q 400,100 450,100" fill="transparent" stroke="#A855F7" strokeWidth="2" strokeDasharray="5,5" className="opacity-60" />
                {/* Connected Case to Notary */}
                <path d="M 600,450 Q 500,275 450,100" fill="transparent" stroke="#A855F7" strokeWidth="2" strokeDasharray="5,5" className="opacity-60" />
                {/* Current Case to Property */}
                <path d="M 400,300 Q 300,450 350,500" fill="transparent" stroke="#F59E0B" strokeWidth="2" className="opacity-60" />
                
                {/* FRAUD RING HIGHLIGHT (Current Case to Connected Case) */}
                <path d="M 400,300 Q 500,400 600,450" fill="transparent" stroke="#EF4444" strokeWidth="6" className="opacity-40" />
                <path d="M 400,300 Q 500,400 600,450" fill="transparent" stroke="#EF4444" strokeWidth="2" strokeDasharray="15,15" className="animate-[dash_1s_linear_infinite]" />
              </svg>

              {/* Edge Labels (HTML overlay) */}
              <div className="absolute top-[230px] left-[525px] bg-slate-900/80 text-red-400 text-[9px] font-bold px-1.5 py-0.5 rounded border border-red-500/30 rotate-[-15deg]">matches</div>
              <div className="absolute top-[180px] left-[430px] bg-slate-900/80 text-purple-400 text-[9px] font-bold px-1.5 py-0.5 rounded border border-purple-500/30 rotate-[-85deg]">notarized by</div>
              <div className="absolute top-[375px] left-[500px] bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-[0_0_10px_rgba(239,68,68,0.5)] rotate-[35deg]">shares elements</div>

              {/* Nodes */}
              
              {/* Central Node: Current Case */}
              <motion.div 
                animate={{ scale: [1, 1.02, 1] }} transition={{ duration: 3, repeat: Infinity }}
                className="absolute top-[300px] left-[400px] -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer group"
                onClick={() => setSelectedNode('current-case')}
              >
                <div className="w-20 h-20 bg-[#0B1121] rounded-full border-4 border-blue-500 flex items-center justify-center relative shadow-[0_0_30px_rgba(59,130,246,0.4)]">
                  <div className="absolute -inset-2 rounded-full border border-blue-500/30 animate-ping opacity-50"></div>
                  <Briefcase className="w-8 h-8 text-blue-400" />
                </div>
                <div className="mt-2 bg-slate-900/90 backdrop-blur px-2.5 py-1 rounded border border-slate-700 text-center">
                  <p className="text-[11px] font-bold text-white leading-none mb-1">{params.id}</p>
                  <p className="text-[9px] text-slate-400">Rajesh Kumar</p>
                </div>
              </motion.div>

              {/* Node: Connected Case (Fraud Ring) */}
              <div className="absolute top-[450px] left-[600px] -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer hover:scale-110 transition-transform">
                <div className="w-16 h-16 bg-slate-900 rounded-full border-2 border-red-500 flex items-center justify-center shadow-[0_0_15px_rgba(239,68,68,0.3)]">
                  <Briefcase className="w-6 h-6 text-red-400" />
                </div>
                <div className="mt-2 bg-slate-900/90 px-2 py-1 rounded border border-red-500/50 text-center">
                  <p className="text-[10px] font-bold text-white mb-0.5">TL-20240815</p>
                  <p className="text-[8px] text-red-400 font-bold">REJECTED</p>
                </div>
              </div>

              {/* Node: Applicant */}
              <div className="absolute top-[350px] left-[200px] -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer hover:scale-110 transition-transform">
                <div className="w-14 h-14 bg-slate-900 rounded-full border-2 border-emerald-500 flex items-center justify-center">
                  <User className="w-6 h-6 text-emerald-400" />
                </div>
                <div className="mt-2 bg-slate-900/90 px-2 py-1 rounded border border-slate-700 text-center">
                  <p className="text-[10px] font-bold text-white">Rajesh Kumar</p>
                  <p className="text-[8px] text-slate-400 font-mono">ABC****123F</p>
                </div>
              </div>

              {/* Node: Property */}
              <div className="absolute top-[500px] left-[350px] -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer hover:scale-110 transition-transform">
                <div className="w-14 h-14 bg-slate-900 rounded-lg border-2 border-amber-500 flex items-center justify-center rotate-3 hover:rotate-0 transition-transform">
                  <MapPin className="w-6 h-6 text-amber-400 -rotate-3" />
                </div>
                <div className="mt-2 bg-slate-900/90 px-2 py-1 rounded border border-slate-700 text-center">
                  <p className="text-[10px] font-bold text-white">Pune Property</p>
                </div>
              </div>

              {/* Node: Notary (Shared) */}
              <div className="absolute top-[100px] left-[450px] -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer hover:scale-110 transition-transform" onClick={() => setSelectedNode('notary')}>
                <div className="w-14 h-14 bg-slate-900 border-2 border-purple-500 flex items-center justify-center rotate-45 hover:rotate-0 transition-all shadow-[0_0_20px_rgba(168,85,247,0.4)]">
                  <Stamp className="w-6 h-6 text-purple-400 -rotate-45 group-hover:rotate-0" />
                  <div className="absolute -top-3 -right-3 rotate-[-45deg] bg-red-500 text-white text-[9px] font-bold w-5 h-5 rounded-full flex items-center justify-center shadow-lg">15</div>
                </div>
                <div className="mt-4 bg-slate-900/90 px-2 py-1 rounded border border-slate-700 text-center">
                  <p className="text-[10px] font-bold text-white">John D.</p>
                  <p className="text-[8px] text-purple-400 font-bold">Baner Notary</p>
                </div>
              </div>

              {/* Node: Pattern (Shared) */}
              <div className="absolute top-[250px] left-[650px] -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer hover:scale-110 transition-transform">
                <div className="w-16 h-16 bg-red-900/30 rounded-lg border-2 border-red-500 flex items-center justify-center rotate-45 hover:rotate-0 transition-all shadow-[0_0_20px_rgba(239,68,68,0.4)] relative overflow-hidden">
                  <Fingerprint className="w-8 h-8 text-red-400 -rotate-45" />
                </div>
                <div className="mt-3 bg-red-500 text-white px-2 py-1 rounded border border-red-600 text-center shadow-lg">
                  <p className="text-[10px] font-bold">Income Inflation</p>
                  <p className="text-[8px]">Type-B Pattern</p>
                </div>
              </div>

            </div>
          </div>
        </div>

        {/* Right Details Panel */}
        <AnimatePresence>
          {selectedNode && (
            <motion.div 
              initial={{ x: 350 }} animate={{ x: 0 }} exit={{ x: 350 }} transition={{ type: "spring", damping: 25 }}
              className="w-[350px] bg-slate-900 border-l border-slate-800 z-30 flex flex-col shadow-2xl shrink-0"
            >
              <div className="p-4 border-b border-slate-800 flex justify-between items-start">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-purple-500/20 border border-purple-500/50 rounded flex items-center justify-center rotate-45 shrink-0">
                    <Stamp className="w-5 h-5 text-purple-400 -rotate-45" />
                  </div>
                  <div>
                    <h2 className="font-bold text-white">John D.</h2>
                    <p className="text-[10px] font-bold text-purple-400 uppercase tracking-wider">Notary Public</p>
                  </div>
                </div>
                <button onClick={() => setSelectedNode(null)} className="text-slate-500 hover:text-white"><X className="w-5 h-5" /></button>
              </div>

              <div className="p-5 flex-1 overflow-auto custom-scrollbar space-y-6">
                
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50">
                    <p className="text-[10px] text-slate-500 uppercase tracking-wider mb-1">Total Cases</p>
                    <p className="text-xl font-bold text-white">15</p>
                  </div>
                  <div className="bg-red-500/10 rounded-lg p-3 border border-red-500/30">
                    <p className="text-[10px] text-red-300 uppercase tracking-wider mb-1">Flagged Cases</p>
                    <p className="text-xl font-bold text-red-400">7</p>
                  </div>
                </div>

                <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
                  <h4 className="text-xs font-bold text-slate-300 mb-3">Suspicion Score</h4>
                  <div className="flex items-center gap-4">
                    <TrustScoreGauge score={78} size="sm" />
                    <div>
                      <p className="text-sm font-bold text-amber-400">High Risk Notary</p>
                      <p className="text-xs text-slate-500 mt-1">46% of notarized documents are tied to fraudulent applications.</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Recent Connected Cases</h4>
                  <div className="space-y-2">
                    <div className="bg-slate-800 rounded p-2.5 flex justify-between items-center border border-slate-700">
                      <div>
                        <p className="text-xs font-bold text-slate-200">TL-20250115-0847</p>
                        <p className="text-[10px] text-slate-500">Current Case</p>
                      </div>
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">Active</span>
                    </div>
                    <div className="bg-slate-800 rounded p-2.5 flex justify-between items-center border border-red-500/30">
                      <div>
                        <p className="text-xs font-bold text-slate-200">TL-20240815-0234</p>
                        <p className="text-[10px] text-slate-500">Aug 15, 2024</p>
                      </div>
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">Rejected</span>
                    </div>
                    <div className="bg-slate-800 rounded p-2.5 flex justify-between items-center border border-red-500/30">
                      <div>
                        <p className="text-xs font-bold text-slate-200">TL-20241015-0512</p>
                        <p className="text-[10px] text-slate-500">Oct 15, 2024</p>
                      </div>
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">Rejected</span>
                    </div>
                  </div>
                </div>

              </div>

              <div className="p-4 border-t border-slate-800 bg-slate-900">
                <Button className="w-full bg-slate-800 hover:bg-slate-700 text-white mb-2">View Full Profile</Button>
                <Button variant="outline" className="w-full border-red-500/50 text-red-400 hover:bg-red-500/10 hover:text-red-300 bg-transparent">Report to Authorities</Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

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
    print("Scaffolded Fraud Network Page.")
