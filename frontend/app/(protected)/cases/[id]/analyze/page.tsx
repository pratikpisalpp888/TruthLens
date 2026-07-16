'use client'

import { useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import {
  FileSearch, Fingerprint, GitCompare, Scale, Gavel,
  X, CheckCircle2, Brain, Loader2, AlertTriangle,
  AlertCircle, Activity, Zap, FileText
} from 'lucide-react'
import { useAnalysisStore, AgentStatus } from '@/stores/analysis-store'
import { useAuthStore } from '@/stores/auth-store'

/* ──────────────────────────────────────────────
   Agent Pipeline Config
─────────────────────────────────────────────── */
const AGENTS = [
  { id: 'classifier',  label: 'Classify',   icon: FileSearch,  color: '#3b82f6', bg: 'bg-blue-50', border: 'border-blue-500', shadow: 'shadow-blue-500/30' },
  { id: 'forensic',    label: 'Forensic',   icon: Fingerprint, color: '#a855f7', bg: 'bg-purple-50', border: 'border-purple-500', shadow: 'shadow-purple-500/30' },
  { id: 'crossref',    label: 'CrossRef',   icon: GitCompare,  color: '#f59e0b', bg: 'bg-amber-50', border: 'border-amber-500', shadow: 'shadow-amber-500/30' },
  { id: 'compliance',  label: 'Compliance', icon: Scale,       color: '#06b6d4', bg: 'bg-cyan-50', border: 'border-cyan-500', shadow: 'shadow-cyan-500/30' },
  { id: 'decision',    label: 'Decision',   icon: Gavel,       color: '#10b981', bg: 'bg-emerald-50', border: 'border-emerald-500', shadow: 'shadow-emerald-500/30' },
]

/* ──────────────────────────────────────────────
   Feed event icon helper
─────────────────────────────────────────────── */
function FeedIcon({ type }: { type: string }) {
  if (type === 'critical') return <AlertCircle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
  if (type === 'warning')  return <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 shrink-0" />
  if (type === 'success')  return <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5 shrink-0" />
  return <Zap className="w-4 h-4 text-blue-500 mt-0.5 shrink-0" />
}

/* ──────────────────────────────────────────────
   Metric Card
─────────────────────────────────────────────── */
function MetricCard({ label, value, icon: Icon, color, bg }: {
  label: string; value: number; icon: any; color: string; bg: string
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative bg-white border border-slate-200 shadow-sm rounded-2xl p-6 flex-1 overflow-hidden group hover:shadow-md transition-all duration-300"
    >
      <div className="flex items-center justify-between mb-4">
        <span className="text-xs font-bold uppercase tracking-widest text-slate-500">{label}</span>
        <div className={`p-2 rounded-xl ${bg}`}>
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
      </div>
      <p className="text-5xl font-black text-slate-900">{value}</p>
    </motion.div>
  )
}

/* ──────────────────────────────────────────────
   Main Page
─────────────────────────────────────────────── */
export default function LiveAnalysisPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const token = useAuthStore(state => state.token)
  const {
    isComplete, progress, timeElapsed, agents, feed,
    metrics, finalSummary, startSimulation, reset
  } = useAnalysisStore()

  const startedRef = useRef(false)

  useEffect(() => {
    if (token && !startedRef.current) {
      startedRef.current = true
      startSimulation(params.id, token)
    }
    return () => {
      startedRef.current = false
      reset()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id, token])

  // Auto-redirect to the AI Report page when complete
  useEffect(() => {
    if (isComplete) {
      const timer = setTimeout(() => {
        router.push(`/cases/${params.id}/report`)
      }, 2000)
      return () => clearTimeout(timer)
    }
  }, [isComplete, params.id, router])

  const formatTime = (s: number) =>
    `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`

  const decisionColor =
    finalSummary?.decision === 'approved' ? '#10b981' :
    finalSummary?.decision === 'rejected' ? '#ef4444' : '#f59e0b'

  return (
    <div className="fixed inset-0 z-50 bg-slate-50 text-slate-900 flex flex-col font-sans overflow-hidden">
      
      {/* Decorative Watermark */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.02] pointer-events-none select-none z-0">
        <img src="/canara-bank-icon-trans.png" alt="" className="w-[800px] h-auto grayscale blur-[2px]" />
      </div>

      {/* ══════════════════════════════════════════
          TOP HEADER BAR
      ══════════════════════════════════════════ */}
      <header className="relative z-10 flex items-center gap-6 px-8 py-5 border-b border-slate-200 bg-white shadow-sm">
        {/* Title */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-blue-500 flex items-center justify-center shadow-md shadow-blue-500/20">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-base font-black text-slate-900 leading-none">TruthLens Orchestrator</h1>
            <p className="text-[11px] font-bold text-slate-400 mt-1 uppercase tracking-widest">
              Live AI Analysis
            </p>
          </div>
        </div>

        {/* ── Agent Pipeline Strip ── */}
        <div className="flex-1 flex items-center justify-center gap-0">
          {AGENTS.map((ag, i) => {
            const state = agents[ag.id]
            const status: AgentStatus = state?.status || 'waiting'
            const isWorking = status === 'working'
            const isDone = status === 'completed'
            const Icon = ag.icon

            return (
              <div key={ag.id} className="flex items-center">
                {/* Agent chip */}
                <motion.div
                  className={`relative flex items-center gap-2 px-4 py-2 rounded-full border-2 text-sm font-bold transition-all duration-300 ${
                    isDone ? 'bg-emerald-50 border-emerald-500 text-emerald-700' :
                    isWorking ? `${ag.bg} ${ag.border} ${ag.shadow} shadow-lg text-slate-900` :
                    'bg-white border-slate-200 text-slate-400'
                  }`}
                  animate={isWorking ? { scale: [1, 1.05, 1] } : { scale: 1 }}
                  transition={{ duration: 2, repeat: isWorking ? Infinity : 0 }}
                >
                  {isWorking && (
                    <motion.div className="absolute inset-0 rounded-full border-2 border-inherit"
                      animate={{ scale: [1, 1.3, 1], opacity: [0.5, 0, 0.5] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                    />
                  )}

                  {isDone
                    ? <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                    : isWorking
                      ? <Loader2 className="w-4 h-4 animate-spin shrink-0" style={{ color: ag.color }} />
                      : <Icon className="w-4 h-4 shrink-0 text-slate-300" />
                  }
                  <span>{ag.label}</span>
                </motion.div>

                {/* Connector arrow */}
                {i < AGENTS.length - 1 && (
                  <div className="flex items-center px-2">
                    <motion.div className="h-[2px] w-8 rounded-full"
                      style={{ background: isDone ? '#10b981' : '#e2e8f0' }}
                      animate={{ opacity: isDone ? [0.4, 1, 0.4] : 1 }}
                      transition={{ duration: 1.5, repeat: isDone ? Infinity : 0 }}
                    />
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Right: Progress + Timer + Close */}
        <div className="flex items-center gap-6 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-40 h-2 bg-slate-100 rounded-full overflow-hidden shadow-inner border border-slate-200">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-blue-500 to-blue-400"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ ease: 'easeOut', duration: 0.5 }}
              />
            </div>
            <span className="text-sm font-black text-slate-700 w-9">{progress}%</span>
          </div>
          <div className="font-mono text-xl font-black text-blue-600 tabular-nums bg-blue-50 px-3 py-1 rounded-lg border border-blue-100">
            {formatTime(timeElapsed)}
          </div>
          <button onClick={() => router.push('/cases')}
            className="w-10 h-10 rounded-full bg-slate-50 hover:bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500 hover:text-slate-800 transition-all shadow-sm">
            <X className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* ══════════════════════════════════════════
          MAIN CONTENT AREA
      ══════════════════════════════════════════ */}
      <div className="relative z-10 flex-1 flex flex-col p-8 gap-8 overflow-hidden max-w-[1600px] mx-auto w-full">

        {/* ── Metric Cards Row ── */}
        <div className="flex gap-6">
          <MetricCard label="Docs Analyzed" value={metrics.docs}      icon={FileText}      color="#3b82f6" bg="bg-blue-50" />
          <MetricCard label="Anomalies"     value={metrics.findings}  icon={AlertTriangle} color="#f59e0b" bg="bg-amber-50" />
          <MetricCard label="Mismatches"    value={metrics.mismatches}icon={GitCompare}    color="#a855f7" bg="bg-purple-50" />
          <MetricCard label="Criticals"     value={metrics.critical}  icon={AlertCircle}   color="#ef4444" bg="bg-red-50" />
          
          {finalSummary && (
            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
              className="relative bg-white border border-slate-200 shadow-sm rounded-2xl p-6 flex-1 overflow-hidden">
              <div className="absolute inset-0 opacity-10 rounded-2xl"
                style={{ background: `radial-gradient(circle at 50% 0%, ${decisionColor}, transparent 70%)` }} />
              <span className="text-xs font-bold uppercase tracking-widest text-slate-500 block mb-3">AI Decision</span>
              <p className="text-4xl font-black" style={{ color: decisionColor }}>
                {finalSummary.decision.toUpperCase()}
              </p>
              <p className="text-sm font-bold text-slate-500 mt-2">Risk Score: {finalSummary.composite_score}/100</p>
            </motion.div>
          )}
        </div>

        {/* ── Neural Log Stream ── */}
        <div className="flex-1 relative bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden flex flex-col min-h-0">
          {/* Header */}
          <div className="flex items-center gap-3 px-6 py-4 border-b border-slate-100 bg-slate-50/50">
            <motion.div
              animate={{ opacity: [1, 0.4, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"
            />
            <Activity className="w-5 h-5 text-slate-400" />
            <h2 className="text-sm font-bold text-slate-700 uppercase tracking-widest">Neural Log Stream</h2>
            <div className="ml-auto flex items-center gap-2 bg-white px-3 py-1 rounded-full border border-slate-200">
              <span className="text-xs font-bold text-slate-500">{feed.length} events logged</span>
            </div>
          </div>

          {/* Feed */}
          <div className="flex-1 overflow-y-auto p-6 space-y-3 flex flex-col-reverse custom-scrollbar bg-slate-50/30">
            <AnimatePresence initial={false}>
              {feed.map((event) => (
                <motion.div key={event.id}
                  initial={{ opacity: 0, x: -16, scale: 0.98 }}
                  animate={{ opacity: 1, x: 0, scale: 1 }}
                  transition={{ duration: 0.25 }}
                  className={`flex items-start gap-4 p-4 rounded-xl border shadow-sm text-sm bg-white
                    ${event.type === 'critical' ? 'border-l-4 border-l-red-500 border-y-slate-200 border-r-slate-200' :
                      event.type === 'warning'  ? 'border-l-4 border-l-amber-500 border-y-slate-200 border-r-slate-200' :
                      event.type === 'success'  ? 'border-l-4 border-l-emerald-500 border-y-slate-200 border-r-slate-200' :
                      'border-l-4 border-l-blue-500 border-y-slate-200 border-r-slate-200'}`}
                >
                  <FeedIcon type={event.type} />
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-slate-700 leading-snug">{event.message}</p>
                  </div>
                  <span className="text-xs font-bold text-slate-400 shrink-0 mt-0.5">{event.time}</span>
                </motion.div>
              ))}
            </AnimatePresence>

            {/* Empty state */}
            {feed.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full gap-4">
                <Loader2 className="w-10 h-10 text-blue-500 animate-spin" />
                <p className="text-slate-500 text-sm font-bold">Initializing AI Agents...</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ══════════════════════════════════════════
          COMPLETION OVERLAY — redirects to report
      ══════════════════════════════════════════ */}
      <AnimatePresence>
        {isComplete && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute inset-0 z-50 flex items-center justify-center p-8 backdrop-blur-md bg-slate-900/40"
          >
            <motion.div
              initial={{ scale: 0.88, y: 32, opacity: 0 }}
              animate={{ scale: 1, y: 0, opacity: 1 }}
              transition={{ type: 'spring', damping: 24, stiffness: 180, delay: 0.1 }}
              className="relative w-full max-w-md rounded-3xl overflow-hidden border border-slate-200 text-center bg-white shadow-2xl"
            >
              <div className="h-2 w-full bg-gradient-to-r from-blue-500 via-purple-500 to-emerald-500" />
              <div className="p-10">
                <motion.div
                  initial={{ scale: 0 }} animate={{ scale: 1 }}
                  transition={{ type: 'spring', delay: 0.3 }}
                  className="w-20 h-20 mx-auto mb-6 rounded-2xl flex items-center justify-center bg-emerald-100 shadow-[0_0_40px_rgba(16,185,129,0.3)]"
                >
                  <CheckCircle2 className="w-10 h-10 text-emerald-600" />
                </motion.div>
                <h2 className="text-3xl font-black text-slate-900 mb-3">Analysis Complete</h2>
                <p className="text-slate-500 font-medium mb-8">Generating comprehensive AI Report...</p>
                <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
