'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { useEffect, useState, useRef } from 'react'
import { CheckCircle, Loader2, Clock, ScanLine, Tag, FileSearch, Fingerprint, BarChart3, ShieldCheck, AlertTriangle, Zap } from 'lucide-react'

// Maps backend processing_status to pipeline step index
const STATUS_TO_STEP: Record<string, number> = {
  uploaded:   0,
  ocr_done:   1,
  classified: 2,
  extracted:  3,
  ner_done:   4,
  analyzed:   5,
  completed:  6,
  error:      -1,
}

interface PipelineStep {
  id: string
  label: string
  detail: string
  icon: React.ElementType
  color: string
  glow: string
}

const STEPS: PipelineStep[] = [
  { id: 'ingest',   label: 'Secure Ingestion',       detail: 'Encrypting & storing document (AES-256)',       icon: ShieldCheck,  color: 'text-sky-400',      glow: 'shadow-sky-500/30'    },
  { id: 'ocr',      label: 'OCR Extraction',          detail: 'PaddleOCR reading text, layout & confidence',   icon: ScanLine,     color: 'text-violet-400',   glow: 'shadow-violet-500/30' },
  { id: 'classify', label: 'Document Classification', detail: 'AI identifying document type & sub-type',       icon: Tag,          color: 'text-amber-400',    glow: 'shadow-amber-500/30'  },
  { id: 'extract',  label: 'Data Extraction',         detail: 'Pulling PAN, income, dates, amounts via regex', icon: FileSearch,   color: 'text-emerald-400',  glow: 'shadow-emerald-500/30'},
  { id: 'ner',      label: 'Named Entity Recognition',detail: 'spaCy NLP tagging people, orgs & money',       icon: Fingerprint,  color: 'text-pink-400',     glow: 'shadow-pink-500/30'   },
  { id: 'score',    label: 'Risk Scoring',            detail: 'Computing Trust Score from all signals',        icon: BarChart3,    color: 'text-orange-400',   glow: 'shadow-orange-500/30' },
  { id: 'done',     label: 'Analysis Complete',       detail: 'Report ready — all findings consolidated',      icon: CheckCircle,  color: 'text-green-400',    glow: 'shadow-green-500/30'  },
]

interface Props {
  documentId: string
  token: string
  onComplete?: (status: string) => void
}

type StepStatus = 'waiting' | 'running' | 'done' | 'error'

export function LivePipelineTracker({ documentId, token, onComplete }: Props) {
  const [stepStatuses, setStepStatuses] = useState<StepStatus[]>(STEPS.map(() => 'waiting'))
  const [currentStep, setCurrentStep] = useState(0)
  const [elapsed, setElapsed] = useState<number[]>(STEPS.map(() => 0))
  const [finalStatus, setFinalStatus] = useState<string | null>(null)
  const [isError, setIsError] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')
  const startTime = useRef(Date.now())
  const stepStartTimes = useRef<number[]>(STEPS.map(() => 0))
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    stepStartTimes.current[0] = Date.now()

    // Tick elapsed time for running step
    timerRef.current = setInterval(() => {
      setElapsed(prev => {
        const next = [...prev]
        const running = stepStatuses.findIndex(s => s === 'running')
        if (running >= 0) {
          next[running] = (Date.now() - stepStartTimes.current[running]) / 1000
        }
        return next
      })
    }, 250)

    // Poll backend
    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/documents/${documentId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (!res.ok) return
        const data = await res.json()
        const status: string = data.processing_status || 'uploaded'
        const step = STATUS_TO_STEP[status] ?? 0

        if (status === 'error') {
          setIsError(true)
          setErrorMsg(data.error_message || 'Pipeline encountered an error')
          clearInterval(pollRef.current!)
          clearInterval(timerRef.current!)
          setFinalStatus('error')
          onComplete?.('error')
          return
        }

        setCurrentStep(step)
        setStepStatuses(prev => {
          const next: StepStatus[] = STEPS.map((_, i) => {
            if (i < step) return 'done'
            if (i === step) {
              if (step === STEPS.length - 1 && status === 'completed') {
                return 'done'
              }
              return 'running'
            }
            return 'waiting'
          })
          // Record start time when step transitions to running
          if (next[step] === 'running' && prev[step] !== 'running') {
            stepStartTimes.current[step] = Date.now()
          }
          return next
        })

        if (status === 'completed' || step >= STEPS.length - 1) {
          clearInterval(pollRef.current!)
          clearInterval(timerRef.current!)
          setFinalStatus('completed')
          setStepStatuses(STEPS.map(() => 'done'))
          onComplete?.('completed')
        }
      } catch (_) {}
    }, 2000)

    return () => {
      clearInterval(pollRef.current!)
      clearInterval(timerRef.current!)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentId, token])

  const totalElapsed = ((Date.now() - startTime.current) / 1000).toFixed(0)

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 rounded-2xl border border-white/10 overflow-hidden shadow-2xl"
    >
      {/* Animated background grid */}
      <div className="absolute inset-0 opacity-10"
        style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(99,102,241,0.4) 1px, transparent 0)', backgroundSize: '28px 28px' }} />

      {/* Top bar */}
      <div className="relative z-10 flex items-center justify-between px-6 py-4 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-3 h-3 rounded-full bg-indigo-400 animate-pulse" />
            <div className="absolute inset-0 w-3 h-3 rounded-full bg-indigo-400 animate-ping opacity-40" />
          </div>
          <div>
            <p className="text-sm font-bold text-white">AI Agent Processing</p>
            <p className="text-xs text-slate-400">Live pipeline — document analysis in progress</p>
          </div>
        </div>
        <div className="flex items-center gap-2 bg-white/5 rounded-full px-3 py-1.5 border border-white/5">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs font-mono text-slate-300">{totalElapsed}s elapsed</span>
        </div>
      </div>

      {/* Steps */}
      <div className="relative z-10 p-6 space-y-3">
        {STEPS.map((step, i) => {
          const status = stepStatuses[i]
          const Icon = step.icon
          const isDone = status === 'done'
          const isRunning = status === 'running'
          const isWaiting = status === 'waiting'

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: isWaiting ? 0.4 : 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className={`flex items-center gap-4 p-3.5 rounded-xl border transition-all duration-500 ${
                isRunning
                  ? 'bg-white/10 border-white/20 shadow-lg ' + step.glow
                  : isDone
                  ? 'bg-white/5 border-white/5'
                  : 'bg-transparent border-transparent'
              }`}
            >
              {/* Icon */}
              <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 transition-all duration-500 ${
                isDone ? 'bg-emerald-500/20 border border-emerald-500/30' :
                isRunning ? 'bg-white/10 border border-white/20' :
                'bg-white/5 border border-white/5'
              }`}>
                {isDone ? (
                  <CheckCircle className="w-5 h-5 text-emerald-400" />
                ) : isRunning ? (
                  <Loader2 className={`w-5 h-5 ${step.color} animate-spin`} />
                ) : (
                  <Icon className="w-5 h-5 text-slate-600" />
                )}
              </div>

              {/* Text */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <p className={`text-sm font-semibold transition-colors ${
                    isDone ? 'text-emerald-300' : isRunning ? 'text-white' : 'text-slate-500'
                  }`}>
                    {step.label}
                  </p>
                  {isRunning && (
                    <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full bg-white/10 ${step.color}`}>
                      Live
                    </span>
                  )}
                  {isDone && (
                    <span className="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400">
                      Done
                    </span>
                  )}
                </div>
                <p className={`text-xs mt-0.5 truncate transition-colors ${isRunning ? 'text-slate-300' : 'text-slate-600'}`}>
                  {step.detail}
                </p>
              </div>

              {/* Timer */}
              <div className="text-right shrink-0">
                {isDone && elapsed[i] > 0 && (
                  <span className="text-xs font-mono text-emerald-500">{elapsed[i].toFixed(1)}s</span>
                )}
                {isRunning && (
                  <span className={`text-xs font-mono ${step.color}`}>{elapsed[i].toFixed(1)}s</span>
                )}
                {isWaiting && (
                  <span className="text-xs text-slate-700">—</span>
                )}
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Progress Bar */}
      <div className="relative z-10 px-6 pb-4">
        <div className="flex justify-between text-xs text-slate-500 mb-2">
          <span>Overall Progress</span>
          <span>{Math.round((currentStep / (STEPS.length - 1)) * 100)}%</span>
        </div>
        <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
          <motion.div
            animate={{ width: `${(currentStep / (STEPS.length - 1)) * 100}%` }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
            className="h-full bg-gradient-to-r from-indigo-500 via-violet-500 to-purple-500 rounded-full shadow-lg shadow-indigo-500/40"
          />
        </div>
      </div>

      {/* Error State */}
      <AnimatePresence>
        {isError && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative z-10 mx-6 mb-6 p-4 bg-red-950/60 border border-red-500/30 rounded-xl flex items-start gap-3"
          >
            <AlertTriangle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-bold text-red-300">Pipeline Error</p>
              <p className="text-xs text-red-400 mt-0.5">{errorMsg}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Completed State */}
      <AnimatePresence>
        {finalStatus === 'completed' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative z-10 mx-6 mb-6 p-4 bg-emerald-950/60 border border-emerald-500/30 rounded-xl flex items-center gap-3"
          >
            <Zap className="w-5 h-5 text-emerald-400 shrink-0" />
            <div className="flex-1">
              <p className="text-sm font-bold text-emerald-300">Analysis Complete!</p>
              <p className="text-xs text-emerald-500 mt-0.5">All signals processed · Trust Score & Risk Report ready</p>
            </div>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-full">{totalElapsed}s total</span>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
