import os

files = {
    "app/(protected)/patterns/page.tsx": """'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, Upload, Download, Search, Filter, Fingerprint, MapPin, Users, FileText, Activity, ShieldAlert, ChevronRight, X, Clock, Target, CheckCircle2 } from 'lucide-react'
import { Button } from '@/components/ui/button'

const PATTERNS = [
  { id: 'pat-1', name: 'Income Inflation Type-B', category: 'Income', icon: Activity, severity: 'Critical', matches: 23, accuracy: 91, added: '8 months ago' },
  { id: 'pat-2', name: 'Property Title Forgery', category: 'Property', icon: MapPin, severity: 'Critical', matches: 12, accuracy: 100, added: '1 year ago' },
  { id: 'pat-3', name: 'Synthetic Identity Gen-4', category: 'Identity', icon: Users, severity: 'High', matches: 45, accuracy: 82, added: '3 months ago' },
  { id: 'pat-4', name: 'Coordinated Ring Print', category: 'Network', icon: Fingerprint, severity: 'High', matches: 8, accuracy: 88, added: '1 month ago' },
  { id: 'pat-5', name: 'Statement Font Tampering', category: 'Document', icon: FileText, severity: 'Medium', matches: 156, accuracy: 76, added: '2 years ago' },
  { id: 'pat-6', name: 'Velocity Submission', category: 'Behavior', icon: Clock, severity: 'Medium', matches: 34, accuracy: 65, added: '5 months ago' }
]

export default function FraudPatternsPage() {
  const [selectedPattern, setSelectedPattern] = useState<any>(null)
  const [search, setSearch] = useState('')

  return (
    <div className="max-w-[1600px] mx-auto pb-20 relative h-[calc(100vh-64px)] overflow-hidden flex flex-col">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-t-2xl shadow-sm border-b border-slate-200 shrink-0">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Fraud Patterns Library</h1>
          <p className="text-sm text-slate-500">Knowledge base of 30 known fraud signatures</p>
        </div>
        
        <div className="flex items-center gap-3">
          <Button variant="outline" className="border-slate-200 text-slate-700 shadow-sm"><Upload className="w-4 h-4 mr-2" /> Import</Button>
          <Button variant="outline" className="border-slate-200 text-slate-700 shadow-sm"><Download className="w-4 h-4 mr-2" /> Export</Button>
          <Button className="bg-primary hover:bg-primary-600 shadow-md text-white"><Plus className="w-4 h-4 mr-2" /> Add Pattern</Button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        
        {/* Left Sidebar (Filters) */}
        <div className="w-64 bg-slate-50 border-r border-slate-200 p-6 flex flex-col gap-8 overflow-y-auto custom-scrollbar shrink-0">
          <div>
            <div className="relative mb-6">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input type="text" placeholder="Search patterns..." className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm outline-none focus:border-primary shadow-sm" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>

            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Categories</h3>
            <div className="space-y-2">
              {['All Patterns', 'Income Inflation', 'Property Forgery', 'Identity Manipulation', 'Coordinated Fraud', 'Document Tampering'].map(cat => (
                <label key={cat} className="flex items-center gap-2 text-sm text-slate-700 cursor-pointer group">
                  <input type="radio" name="category" defaultChecked={cat === 'All Patterns'} className="text-primary focus:ring-primary border-slate-300" />
                  <span className="group-hover:text-primary transition-colors">{cat}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Severity</h3>
            <div className="space-y-2">
              {[
                { label: 'Critical', color: 'bg-red-500' },
                { label: 'High', color: 'bg-amber-500' },
                { label: 'Medium', color: 'bg-blue-500' },
                { label: 'Low', color: 'bg-emerald-500' }
              ].map(sev => (
                <label key={sev.label} className="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
                  <input type="checkbox" defaultChecked className="rounded border-slate-300 text-primary focus:ring-primary" />
                  <span className="flex items-center gap-2"><div className={`w-2.5 h-2.5 rounded-full ${sev.color}`}></div> {sev.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Main Grid */}
        <div className="flex-1 bg-slate-100/50 p-6 overflow-y-auto custom-scrollbar">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {PATTERNS.map((pattern, i) => (
              <div 
                key={pattern.id}
                onClick={() => setSelectedPattern(pattern)}
                className="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-lg transition-all cursor-pointer group hover:border-primary/50 relative overflow-hidden flex flex-col"
              >
                {pattern.severity === 'Critical' && <div className="absolute top-0 left-0 right-0 h-1 bg-red-500"></div>}
                {pattern.severity === 'High' && <div className="absolute top-0 left-0 right-0 h-1 bg-amber-500"></div>}
                
                <div className="p-5 flex-1">
                  <div className="flex justify-between items-start mb-4">
                    <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center text-slate-500 group-hover:bg-primary/10 group-hover:text-primary transition-colors">
                      <pattern.icon className="w-5 h-5" />
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-1 rounded uppercase tracking-wider
                      ${pattern.severity === 'Critical' ? 'bg-red-50 text-red-700 border border-red-100' : 
                        pattern.severity === 'High' ? 'bg-amber-50 text-amber-700 border border-amber-100' : 
                        'bg-blue-50 text-blue-700 border border-blue-100'}`}
                    >
                      {pattern.severity}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-bold text-slate-900 mb-1 group-hover:text-primary transition-colors">{pattern.name}</h3>
                  <p className="text-xs text-slate-500 mb-4">{pattern.category} • Added {pattern.added}</p>
                  
                  <p className="text-sm text-slate-600 line-clamp-2">
                    Manipulation of documents with specific tampering signatures in the designated fields, typically involving digital editing.
                  </p>
                </div>
                
                <div className="bg-slate-50 p-4 border-t border-slate-100 flex justify-between items-center mt-auto">
                  <div>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Total Matches</p>
                    <p className="text-lg font-black text-slate-800">{pattern.matches}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Accuracy</p>
                    <p className={`text-lg font-black ${pattern.accuracy > 90 ? 'text-emerald-600' : 'text-amber-600'}`}>{pattern.accuracy}%</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Pattern Details Sidebar */}
        <AnimatePresence>
          {selectedPattern && (
            <motion.div 
              initial={{ x: '100%', opacity: 0 }} 
              animate={{ x: 0, opacity: 1 }} 
              exit={{ x: '100%', opacity: 0 }} 
              transition={{ type: "spring", damping: 25 }}
              className="absolute right-0 top-0 bottom-0 w-[500px] bg-white border-l border-slate-200 shadow-2xl z-20 flex flex-col"
            >
              <div className="p-6 border-b border-slate-200 flex justify-between items-start bg-slate-50/50">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
                    <selectedPattern.icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-slate-900">{selectedPattern.name}</h2>
                    <p className="text-xs text-slate-500 font-mono">ID: {selectedPattern.id}</p>
                  </div>
                </div>
                <button onClick={() => setSelectedPattern(null)} className="p-2 hover:bg-slate-200 rounded-full text-slate-500 transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-8">
                
                <section>
                  <h3 className="text-sm font-bold text-slate-900 mb-3 border-b border-slate-100 pb-2 flex items-center gap-2"><Target className="w-4 h-4 text-slate-400" /> Detection Signature</h3>
                  <div className="bg-slate-900 rounded-xl p-5 text-white font-mono text-xs shadow-inner">
                    <p className="text-primary-400 mb-2">// 128-dimensional feature vector extraction</p>
                    <p className="opacity-80">"vector_hash": "a8f3b2c9...d4e1",</p>
                    <p className="opacity-80">"primary_features": [</p>
                    <p className="opacity-80 pl-4">"ela_compression_variance > 15%",</p>
                    <p className="opacity-80 pl-4">"metadata_creator != document_source",</p>
                    <p className="opacity-80 pl-4">"font_kerning_anomaly = true"</p>
                    <p className="opacity-80">],</p>
                    <p className="opacity-80">"confidence_threshold": 0.85</p>
                  </div>
                </section>

                <section>
                  <h3 className="text-sm font-bold text-slate-900 mb-3 border-b border-slate-100 pb-2">Recent Matches</h3>
                  <div className="space-y-3">
                    {[
                      { id: 'TL-20250115-0847', date: 'Today', conf: 92, confirmed: true },
                      { id: 'TL-20241210-0234', date: 'Dec 10, 2024', conf: 88, confirmed: true },
                      { id: 'TL-20241122-0112', date: 'Nov 22, 2024', conf: 95, confirmed: true },
                    ].map(match => (
                      <div key={match.id} className="bg-slate-50 border border-slate-200 rounded-lg p-3 flex justify-between items-center">
                        <div>
                          <p className="text-sm font-bold text-slate-900 hover:text-primary cursor-pointer">{match.id}</p>
                          <p className="text-[10px] text-slate-500">{match.date}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="text-xs font-bold text-slate-600">{match.conf}% Match</span>
                          {match.confirmed && <CheckCircle2 className="w-4 h-4 text-emerald-500" />}
                        </div>
                      </div>
                    ))}
                  </div>
                </section>

                <section>
                  <h3 className="text-sm font-bold text-slate-900 mb-3 border-b border-slate-100 pb-2 flex items-center gap-2"><ShieldAlert className="w-4 h-4 text-slate-400" /> Required Actions on Match</h3>
                  <div className="bg-red-50 border border-red-100 rounded-lg p-4 text-sm text-red-900 space-y-2">
                    <p className="font-bold flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-red-500"></div> Automatic rejection recommendation</p>
                    <p className="font-bold flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-red-500"></div> Flag applicant PAN across network</p>
                    <p className="font-bold flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-red-500"></div> Notify branch fraud control officer</p>
                  </div>
                </section>

              </div>
              
              <div className="p-6 border-t border-slate-200 bg-slate-50 flex gap-3">
                <Button className="flex-1 bg-slate-900 hover:bg-slate-800 text-white">Edit Pattern</Button>
                <Button variant="outline" className="flex-1 border-red-200 text-red-600 hover:bg-red-50 bg-white">Disable</Button>
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
    print("Scaffolded Fraud Patterns Page.")
