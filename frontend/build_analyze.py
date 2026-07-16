import os

files = {
    "stores/analysis-store.ts": """import { create } from 'zustand'

export type AgentStatus = 'waiting' | 'working' | 'completed' | 'error'

export interface AgentState {
  id: string
  name: string
  status: AgentStatus
  progress: number
  subtask: string
  findings: string[]
  timeTaken?: string
}

interface AnalysisState {
  isAnalyzing: boolean
  isComplete: boolean
  progress: number
  timeElapsed: number
  agents: Record<string, AgentState>
  feed: { id: string; type: 'info' | 'warning' | 'critical' | 'success' | 'system'; message: string; time: string }[]
  metrics: { docs: number; findings: number; critical: number; mismatches: number }
  
  startSimulation: () => void
  reset: () => void
}

const initialAgents: Record<string, AgentState> = {
  classifier: { id: 'classifier', name: 'Document Classifier', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  forensic: { id: 'forensic', name: 'Forensic Investigator', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  crossref: { id: 'crossref', name: 'Cross-Reference Agent', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  compliance: { id: 'compliance', name: 'Compliance Agent', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  decision: { id: 'decision', name: 'Decision Agent', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  isAnalyzing: false,
  isComplete: false,
  progress: 0,
  timeElapsed: 0,
  agents: initialAgents,
  feed: [],
  metrics: { docs: 0, findings: 0, critical: 0, mismatches: 0 },

  startSimulation: () => {
    set({ isAnalyzing: true, isComplete: false, progress: 0, timeElapsed: 0, agents: initialAgents, feed: [], metrics: { docs: 0, findings: 0, critical: 0, mismatches: 0 } })
    
    // Simple timer
    const timer = setInterval(() => {
      set(state => ({ timeElapsed: state.timeElapsed + 1 }))
    }, 1000)

    const addFeed = (type: any, message: string) => {
      set(state => ({ feed: [{ id: Math.random().toString(), type, message, time: 'just now' }, ...state.feed] }))
    }

    const updateAgent = (id: string, updates: Partial<AgentState>) => {
      set(state => ({ agents: { ...state.agents, [id]: { ...state.agents[id], ...updates } } }))
    }

    // Agent 1: Classifier (0-3s)
    setTimeout(() => {
      addFeed('system', '🔄 Starting analysis pipeline')
      updateAgent('classifier', { status: 'working', subtask: 'Identifying document types...', progress: 30 })
    }, 500)
    
    setTimeout(() => {
      addFeed('success', '✅ Identified 8 documents successfully')
      updateAgent('classifier', { status: 'completed', subtask: 'Classification complete', progress: 100, timeTaken: '2.4s', findings: ['Found 3 ITRs, 2 Bank Statements', 'Sale Deed detected'] })
      set(state => ({ progress: 20, metrics: { ...state.metrics, docs: 8 } }))
      
      // Agent 2 & 3: Forensic & CrossRef start (3s-8s)
      updateAgent('forensic', { status: 'working', subtask: 'Scanning metadata & ELA...', progress: 10 })
      updateAgent('crossref', { status: 'working', subtask: 'Extracting named entities...', progress: 15 })
    }, 3000)

    // Parallel findings
    setTimeout(() => {
      addFeed('warning', '⚠️ Metadata anomaly detected in Sale Deed')
      updateAgent('forensic', { progress: 45, subtask: 'Running deep pixel analysis...', findings: ['Sale deed modified 3 days ago', 'Font inconsistencies detected'] })
      set(state => ({ progress: 40, metrics: { ...state.metrics, findings: 2 } }))
    }, 5000)

    setTimeout(() => {
      addFeed('critical', '🚨 Income mismatch across 3 documents')
      updateAgent('crossref', { progress: 60, subtask: 'Comparing financial fields...', findings: ['Declared income > ITR by 40%', 'Name spelling variation found'] })
      set(state => ({ progress: 60, metrics: { ...state.metrics, findings: 4, critical: 1, mismatches: 2 } }))
    }, 6500)

    // Complete parallel agents
    setTimeout(() => {
      updateAgent('forensic', { status: 'completed', progress: 100, subtask: 'Forensic scan complete', timeTaken: '5.1s' })
      updateAgent('crossref', { status: 'completed', progress: 100, subtask: 'Cross-reference complete', timeTaken: '5.8s' })
      
      // Agent 4: Compliance (9s-12s)
      updateAgent('compliance', { status: 'working', subtask: 'Checking banking regulations...', progress: 20 })
    }, 8500)

    setTimeout(() => {
      addFeed('warning', '⚠️ Missing property tax receipt')
      updateAgent('compliance', { progress: 100, status: 'completed', subtask: 'Compliance check complete', timeTaken: '3.2s', findings: ['KYC norms met', 'Property tax doc missing'] })
      set(state => ({ progress: 85, metrics: { ...state.metrics, findings: 5 } }))
      
      // Agent 5: Decision (12s-14s)
      updateAgent('decision', { status: 'working', subtask: 'Calculating Trust Score...', progress: 50 })
    }, 11500)

    // Finalize
    setTimeout(() => {
      addFeed('system', '📊 Risk score calculated: HIGH RISK')
      updateAgent('decision', { status: 'completed', progress: 100, subtask: 'Decision generated', timeTaken: '1.5s', findings: ['Trust Score: 18/100', 'Recommendation: FLAGGED'] })
      set({ progress: 100, isComplete: true, isAnalyzing: false })
      clearInterval(timer)
    }, 13500)
  },

  reset: () => set({ isAnalyzing: false, isComplete: false, progress: 0, timeElapsed: 0, agents: initialAgents, feed: [], metrics: { docs: 0, findings: 0, critical: 0, mismatches: 0 } })
}))
""",
    "app/(protected)/cases/[id]/analyze/page.tsx": """'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { FileSearch, Fingerprint, GitCompare, Scale, Gavel, X, FileText, CheckCircle2, AlertTriangle, Brain, Loader2, ArrowRight } from 'lucide-react'
import { useAnalysisStore } from '@/stores/analysis-store'
import { TrustScoreGauge } from '@/components/shared/trust-score-gauge'
import { Button } from '@/components/ui/button'

const iconMap: Record<string, any> = {
  classifier: FileSearch,
  forensic: Fingerprint,
  crossref: GitCompare,
  compliance: Scale,
  decision: Gavel
}

export default function LiveAnalysisPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const { isAnalyzing, isComplete, progress, timeElapsed, agents, feed, metrics, startSimulation, reset } = useAnalysisStore()

  useEffect(() => {
    startSimulation()
    return () => reset()
  }, [startSimulation, reset])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const getBorderColor = (status: string) => {
    if (status === 'working') return 'border-primary shadow-[0_0_15px_rgba(37,99,235,0.3)]'
    if (status === 'completed') return 'border-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.2)]'
    if (status === 'error') return 'border-red-500'
    return 'border-slate-700/50'
  }

  return (
    <div className="fixed inset-0 z-50 bg-[#0B1121] overflow-hidden flex flex-col text-slate-200">
      
      {/* Dynamic Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary-900/40 via-[#0B1121] to-[#0B1121] pointer-events-none"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-6 py-4 border-b border-slate-800/60 bg-[#0B1121]/80 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="bg-primary/20 p-2 rounded-lg border border-primary/30">
            <Brain className="w-5 h-5 text-primary-400" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white leading-tight">Live AI Analysis</h1>
            <p className="text-xs text-slate-400 font-mono">Case: {params.id}</p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-slate-400">Total Progress</span>
            <div className="w-48 h-2.5 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
              <motion.div 
                className="h-full bg-gradient-to-r from-primary to-blue-400"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ ease: "linear" }}
              />
            </div>
            <span className="text-sm font-bold text-white w-10">{progress}%</span>
          </div>
          <div className="w-px h-6 bg-slate-700"></div>
          <div className="font-mono text-xl font-bold tracking-wider text-primary-400">
            {formatTime(timeElapsed)}
          </div>
          <button onClick={() => router.push(`/cases`)} className="ml-2 p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Main Orchestration Area */}
      <div className="flex-1 relative z-10 flex p-6 gap-6 overflow-hidden">
        
        {/* Agent Cards (Left Side) */}
        <div className="flex-1 flex flex-col justify-center gap-4 overflow-y-auto pr-4 custom-scrollbar">
          {Object.values(agents).map((agent, index) => {
            const Icon = iconMap[agent.id]
            const isWorking = agent.status === 'working'
            const isCompleted = agent.status === 'completed'
            
            return (
              <motion.div 
                key={agent.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`bg-slate-900/60 backdrop-blur-md rounded-xl p-5 border transition-all duration-500 relative overflow-hidden ${getBorderColor(agent.status)} ${isWorking ? 'scale-[1.02]' : 'scale-100 opacity-80'}`}
              >
                {/* Background pulse effect for working state */}
                {isWorking && (
                  <motion.div 
                    className="absolute inset-0 bg-primary/5 rounded-xl"
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
                
                <div className="relative z-10 flex items-start gap-5">
                  {/* Agent Icon */}
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center shrink-0 border-2 transition-colors duration-300
                    ${isWorking ? 'bg-primary/20 border-primary text-primary-400' : 
                      isCompleted ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400' : 
                      'bg-slate-800 border-slate-700 text-slate-500'}`}
                  >
                    {isCompleted ? <CheckCircle2 className="w-6 h-6" /> : <Icon className="w-6 h-6" />}
                  </div>

                  {/* Agent Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className={`text-lg font-bold truncate ${isWorking ? 'text-white' : 'text-slate-300'}`}>{agent.name}</h3>
                      {agent.timeTaken && <span className="text-xs font-mono text-slate-500">{agent.timeTaken}</span>}
                    </div>
                    
                    <div className="flex items-center gap-2 mb-3 h-5">
                      {isWorking && <Loader2 className="w-3.5 h-3.5 text-primary-400 animate-spin" />}
                      <p className={`text-sm ${isWorking ? 'text-primary-300 font-medium' : isCompleted ? 'text-emerald-400' : 'text-slate-500'}`}>
                        {agent.subtask}
                      </p>
                    </div>

                    {/* Findings */}
                    <AnimatePresence>
                      {agent.findings.length > 0 && (
                        <motion.div 
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          className="mt-3 space-y-1.5"
                        >
                          {agent.findings.map((finding, i) => (
                            <div key={i} className="flex items-start gap-2 text-xs">
                              <ArrowRight className="w-3 h-3 mt-0.5 text-slate-500 shrink-0" />
                              <span className="text-slate-300">{finding}</span>
                            </div>
                          ))}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                  
                  {/* Small Progress Ring */}
                  {isWorking && (
                    <div className="w-10 h-10 shrink-0 relative flex items-center justify-center">
                      <svg className="transform -rotate-90 absolute w-full h-full">
                        <circle cx="20" cy="20" r="16" fill="transparent" stroke="rgba(255,255,255,0.1)" strokeWidth="3" />
                        <circle cx="20" cy="20" r="16" fill="transparent" stroke="currentColor" strokeWidth="3" 
                          strokeDasharray="100" strokeDashoffset={100 - agent.progress} 
                          className="text-primary-400 transition-all duration-300" />
                      </svg>
                      <span className="text-[10px] font-bold text-white absolute">{agent.progress}%</span>
                    </div>
                  )}
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* Right Side: Metrics & Feed */}
        <div className="w-[350px] flex flex-col gap-4">
          
          {/* Live Metrics */}
          <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-xl p-4 grid grid-cols-2 gap-4">
            <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50">
              <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Docs Processed</p>
              <p className="text-2xl font-bold text-white">{metrics.docs}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50">
              <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Anomalies</p>
              <p className="text-2xl font-bold text-amber-400">{metrics.findings}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50">
              <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Mismatches</p>
              <p className="text-2xl font-bold text-red-400">{metrics.mismatches}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/50">
              <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Critical Alerts</p>
              <p className="text-2xl font-bold text-red-500">{metrics.critical}</p>
            </div>
          </div>

          {/* Activity Feed */}
          <div className="flex-1 bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-xl flex flex-col overflow-hidden">
            <div className="p-3 border-b border-slate-800 bg-slate-900/80">
              <h3 className="text-sm font-bold text-slate-300 flex items-center gap-2">
                <ActivityIcon className="w-4 h-4 text-emerald-400 animate-pulse" /> Live Activity Feed
              </h3>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar flex flex-col-reverse">
              <AnimatePresence>
                {feed.map((event) => (
                  <motion.div 
                    key={event.id}
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    className={`p-3 rounded-lg border text-sm flex gap-3
                      ${event.type === 'critical' ? 'bg-red-500/10 border-red-500/30 text-red-200' :
                        event.type === 'warning' ? 'bg-amber-500/10 border-amber-500/30 text-amber-200' :
                        event.type === 'success' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-200' :
                        'bg-slate-800/50 border-slate-700 text-slate-300'}`}
                  >
                    <span className="text-lg leading-none shrink-0">{
                      event.type === 'critical' ? '🚨' :
                      event.type === 'warning' ? '⚠️' :
                      event.type === 'success' ? '✅' : '🔄'
                    }</span>
                    <div>
                      <p>{event.message}</p>
                      <p className="text-[10px] opacity-50 mt-1 uppercase tracking-wider">{event.time}</p>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>

      {/* Completion Overlay */}
      <AnimatePresence>
        {isComplete && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="absolute inset-0 z-50 bg-[#0B1121]/95 backdrop-blur-lg flex items-center justify-center p-6"
          >
            <motion.div 
              initial={{ scale: 0.9, y: 20 }} animate={{ scale: 1, y: 0 }} transition={{ delay: 0.2 }}
              className="bg-slate-900 border border-slate-700 p-10 rounded-2xl shadow-2xl max-w-xl w-full text-center relative overflow-hidden"
            >
              <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-red-500 to-amber-500"></div>
              
              <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6 border border-red-500/20">
                <AlertTriangle className="w-10 h-10 text-red-500" />
              </div>
              
              <h2 className="text-3xl font-bold text-white mb-2">Analysis Complete</h2>
              <p className="text-slate-400 mb-8">Generated in {formatTime(timeElapsed)} across 5 AI Agents</p>
              
              <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 mb-8 flex justify-between items-center text-left">
                <div>
                  <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Final Decision</p>
                  <p className="text-xl font-bold text-red-500 flex items-center gap-2"><X className="w-5 h-5" /> REJECT / HIGH RISK</p>
                </div>
                <div className="w-px h-12 bg-slate-700"></div>
                <div>
                  <TrustScoreGauge score={18} size="md" />
                </div>
              </div>
              
              <div className="flex gap-4">
                <Button onClick={() => router.push(`/cases/${params.id}`)} className="flex-1 bg-white text-slate-900 hover:bg-slate-100 font-bold h-12">
                  View Full Report
                </Button>
                <Button variant="outline" onClick={() => router.push('/cases')} className="flex-1 border-slate-600 text-slate-300 hover:bg-slate-800 h-12">
                  Back to Cases
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      
    </div>
  )
}

function ActivityIcon({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
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
    print("Scaffolded Live Analysis page.")
