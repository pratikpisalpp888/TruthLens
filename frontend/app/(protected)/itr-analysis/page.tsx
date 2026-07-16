'use client'

import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Upload, Scan, FileText, Brain, Fingerprint, GitCompare,
  Scale, Calculator, AlertTriangle, CheckCircle2, ChevronRight, XCircle, RefreshCw
} from 'lucide-react'
import { useAuthStore } from '@/stores/auth-store'

const LAYERS = [
  { id: 'format',      name: 'Format & Syntax',                icon: FileText   },
  { id: 'computation', name: 'Computational Math',             icon: Calculator },
  { id: 'bank',        name: 'Bank Cross-Reference',           icon: GitCompare },
  { id: 'behavior',    name: 'Behavior & Trends',              icon: Brain      },
  { id: 'statistical', name: 'Statistical Anomalies (Benford)',icon: Scan       },
  { id: 'semantic',    name: 'Semantic Keyword NLP',           icon: Scale      },
  { id: 'identity',    name: 'Identity Consistency',           icon: Fingerprint},
]

type Status = 'idle' | 'scanning' | 'complete' | 'error'

export default function ITRAnalysisPage() {
  const [file, setFile]               = useState<File | null>(null)
  const [filePreview, setFilePreview] = useState<string | null>(null)
  const [status, setStatus]           = useState<Status>('idle')
  const [activeLayer, setActiveLayer] = useState(-1)
  const [results, setResults]         = useState<any>(null)
  const [errorMsg, setErrorMsg]       = useState<string>('')

  const { token } = useAuthStore()

  /* Refs so async fetch can update state even after component re-renders */
  const apiResultRef = useRef<any>(null)
  const apiErrorRef  = useRef<string | null>(null)
  const intervalRef  = useRef<any>(null)

  const reset = () => {
    clearInterval(intervalRef.current)
    setFile(null)
    setFilePreview(null)
    setStatus('idle')
    setActiveLayer(-1)
    setResults(null)
    setErrorMsg('')
    apiResultRef.current = null
    apiErrorRef.current  = null
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return
    const f = e.target.files[0]
    if (filePreview) URL.revokeObjectURL(filePreview)
    setFile(f)
    setFilePreview(URL.createObjectURL(f))
    setStatus('idle')
    setResults(null)
    setActiveLayer(-1)
    setErrorMsg('')
    apiResultRef.current = null
    apiErrorRef.current  = null
  }

  const startScan = async () => {
    if (!file) { setErrorMsg('Please select a file first.'); return }
    if (!token) { setErrorMsg('Not authenticated. Please log in again.'); return }

    // Start UI animation
    setStatus('scanning')
    setActiveLayer(0)
    setResults(null)
    setErrorMsg('')
    apiResultRef.current = null
    apiErrorRef.current  = null

    // Fire API in parallel (non-blocking — animation runs independently)
    const formData = new FormData()
    formData.append('file', file)
    
    // Dynamically resolve backend host to bypass proxy while supporting LAN access
    const backendUrl = `http://${window.location.hostname}:8000/api/v1/itr/standalone-scan`

    // Bypass Next.js proxy to avoid 30-second timeout for local AI processing
    fetch(backendUrl, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    })
      .then(async (res) => {
        if (!res.ok) {
          const txt = await res.text().catch(() => res.statusText)
          apiErrorRef.current = `Server error ${res.status}: ${txt.slice(0, 200)}`
        } else {
          apiResultRef.current = await res.json()
        }
      })
      .catch((err) => {
        apiErrorRef.current = `Network error: ${err.message}`
      })
  }

  /* Layer animation: advances every 1.2 s; when done, resolves with API result */
  useEffect(() => {
    if (status !== 'scanning') return

    clearInterval(intervalRef.current)
    intervalRef.current = setInterval(() => {
      setActiveLayer((prev) => {
        const next = prev + 1

        if (next >= LAYERS.length) {
          // All layers done — check if API has responded
          clearInterval(intervalRef.current)

          if (apiResultRef.current !== null) {
            setResults(apiResultRef.current)
            setStatus('complete')
          } else if (apiErrorRef.current !== null) {
            setErrorMsg(apiErrorRef.current)
            setStatus('error')
          } else {
            // API still running — wait for it with a polling interval
            const wait = setInterval(() => {
              if (apiResultRef.current !== null) {
                clearInterval(wait)
                setResults(apiResultRef.current)
                setStatus('complete')
              } else if (apiErrorRef.current !== null) {
                clearInterval(wait)
                setErrorMsg(apiErrorRef.current)
                setStatus('error')
              }
            }, 500)
          }
          return LAYERS.length - 1  // keep last layer highlighted during wait
        }
        return next
      })
    }, 1200)

    return () => clearInterval(intervalRef.current)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [status])

  const layerDone  = (idx: number) => status === 'complete' || activeLayer > idx
  const layerActive= (idx: number) => status === 'scanning' && activeLayer === idx

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-200">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <header className="mb-10 text-center pt-6">
          <motion.h1
            initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-black bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent"
          >
            7-Layer ITR Intelligence
          </motion.h1>
          <p className="mt-3 text-slate-400 text-sm">
            Advanced anomaly detection &amp; statistical forensics for ITR documents.
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-10">

          {/* ── LEFT: Document Preview ── */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 overflow-hidden">

            {!file ? (
              <label className="flex flex-col items-center justify-center h-full min-h-[400px] cursor-pointer border-2 border-dashed border-slate-700 rounded-2xl hover:border-indigo-500/60 transition-colors gap-4">
                <Upload className="w-14 h-14 text-indigo-400 opacity-70" />
                <div className="text-center">
                  <p className="text-lg font-bold text-white">Upload ITR Document</p>
                  <p className="text-sm text-slate-400 mt-1">PDF, PNG, JPG — click or drag & drop</p>
                </div>
                <span className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl font-bold transition-colors text-sm">
                  Select File
                </span>
                <input type="file" className="hidden" accept=".pdf,.png,.jpg,.jpeg" onChange={handleFileChange} />
              </label>
            ) : (
              <div className="flex flex-col h-full gap-4">
                {/* File info bar */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 bg-indigo-500/20 rounded-xl">
                      <FileText className="text-indigo-400 w-6 h-6" />
                    </div>
                    <div>
                      <p className="font-semibold text-white text-sm truncate max-w-[180px]">{file.name}</p>
                      <p className="text-xs text-slate-400">{(file.size / 1024).toFixed(1)} KB</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {status === 'idle' && (
                      <button
                        onClick={startScan}
                        className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-5 py-2 rounded-xl font-bold text-sm transition-all shadow-lg shadow-indigo-500/20"
                      >
                        Start Scan
                      </button>
                    )}
                    {(status === 'complete' || status === 'error') && (
                      <button onClick={reset} className="flex items-center gap-1 bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-xl text-sm font-medium transition-colors">
                        <RefreshCw className="w-3.5 h-3.5" /> Reset
                      </button>
                    )}
                  </div>
                </div>

                {/* Document Preview box */}
                <div className="relative flex-1 min-h-[340px] bg-slate-800 rounded-xl overflow-hidden border border-slate-700">
                  {filePreview && (
                    <object data={filePreview} type={file.type} className="w-full h-full pointer-events-none opacity-70" />
                  )}

                  {/* Scanner laser */}
                  {status === 'scanning' && (
                    <motion.div
                      initial={{ top: '-5%' }}
                      animate={{ top: '105%' }}
                      transition={{ duration: 2.5, repeat: Infinity, ease: 'linear' }}
                      className="absolute left-0 right-0 h-0.5 bg-cyan-400 shadow-[0_0_18px_4px_rgba(34,211,238,0.55)] z-20 pointer-events-none"
                    />
                  )}

                  {/* Fraud highlight overlay */}
                  {status === 'complete' && results?.critical_issues?.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                      className="absolute inset-4 border-2 border-red-500 bg-red-500/10 rounded-lg z-20 pointer-events-none shadow-[0_0_30px_rgba(239,68,68,0.4)] flex items-start justify-center pt-4"
                    >
                      <span className="bg-red-950/90 text-red-300 px-4 py-1.5 rounded-full text-xs font-bold border border-red-600/50">
                        ⚠ {results.critical_issues.length} Fraud Indicator{results.critical_issues.length > 1 ? 's' : ''} Detected
                      </span>
                    </motion.div>
                  )}

                  {/* Clean overlay */}
                  {status === 'complete' && results?.critical_issues?.length === 0 && (
                    <motion.div
                      initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                      className="absolute inset-4 border-2 border-emerald-500 bg-emerald-500/10 rounded-lg z-20 pointer-events-none shadow-[0_0_30px_rgba(16,185,129,0.3)] flex items-start justify-center pt-4"
                    >
                      <span className="bg-emerald-950/90 text-emerald-300 px-4 py-1.5 rounded-full text-xs font-bold border border-emerald-600/50">
                        ✓ Document Appears Authentic
                      </span>
                    </motion.div>
                  )}
                </div>

                {/* Error message */}
                {status === 'error' && errorMsg && (
                  <div className="flex items-start gap-2 bg-red-950/60 border border-red-700/50 rounded-xl p-3 text-red-300 text-sm">
                    <XCircle className="w-4 h-4 mt-0.5 shrink-0" />
                    <span>{errorMsg}</span>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* ── RIGHT: Intelligence Layers ── */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Brain className="text-indigo-400 w-5 h-5" /> Intelligence Layers
            </h3>

            <div className="space-y-2.5">
              {LAYERS.map((layer, idx) => {
                const Icon = layer.icon
                const done   = layerDone(idx)
                const active = layerActive(idx)
                return (
                  <motion.div
                    key={layer.id}
                    initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.06 }}
                    className={`flex items-center justify-between p-3.5 rounded-xl border transition-all ${
                      done   ? 'bg-emerald-500/10 border-emerald-500/30' :
                      active ? 'bg-indigo-500/20 border-indigo-500/50 shadow-[0_0_12px_rgba(99,102,241,0.25)]' :
                               'bg-slate-900/60 border-slate-800'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-lg ${
                        done   ? 'bg-emerald-500/20 text-emerald-400' :
                        active ? 'bg-indigo-500/25 text-indigo-400' :
                                 'bg-slate-800 text-slate-500'
                      }`}>
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className={`text-sm font-medium ${
                        done ? 'text-emerald-300' : active ? 'text-indigo-300' : 'text-slate-500'
                      }`}>{layer.name}</span>
                    </div>
                    {done   && <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />}
                    {active && (
                      <motion.div animate={{ rotate: 360 }} transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}>
                        <Scan className="w-4 h-4 text-indigo-400" />
                      </motion.div>
                    )}
                  </motion.div>
                )
              })}
            </div>

            {/* Progress bar */}
            <div className="mt-2">
              <div className="flex justify-between text-xs text-slate-500 mb-1.5 font-medium uppercase tracking-wider">
                <span>Progress</span>
                <span>
                  {status === 'complete' ? '100' :
                   status === 'scanning' ? Math.round(((activeLayer + 1) / LAYERS.length) * 100) : 0}%
                </span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-full"
                  animate={{
                    width: status === 'complete' ? '100%' :
                           status === 'scanning' ? `${((activeLayer + 1) / LAYERS.length) * 100}%` : '0%'
                  }}
                  transition={{ duration: 0.4 }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* ── Results Section ── */}
        <AnimatePresence>
          {status === 'complete' && results && (
            <motion.div
              initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
              className="mt-10 mb-16 bg-slate-900/80 backdrop-blur border border-slate-800 rounded-3xl p-8"
            >
              <div className="flex flex-col md:flex-row gap-6 items-start justify-between mb-8">
                <div>
                  <h2 className="text-2xl font-black text-white">Analysis Complete</h2>
                  <p className="text-slate-400 text-sm mt-1">
                    {results.form_type && <span className="mr-3">Form: <strong className="text-slate-300">{results.form_type}</strong></span>}
                    {results.assessment_year && <span>AY: <strong className="text-slate-300">{results.assessment_year}</strong></span>}
                    <span className="ml-3 text-slate-500">({results.processing_time_ms}ms)</span>
                  </p>
                </div>
                <div className="flex gap-6">
                  <div className="text-center">
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-wider mb-1">Validity Score</p>
                    <p className={`text-4xl font-black ${results.validity_score > 70 ? 'text-emerald-400' : 'text-red-400'}`}>
                      {results.validity_score.toFixed(1)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-wider mb-1">Issues</p>
                    <p className={`text-4xl font-black ${results.critical_issues.length > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
                      {results.critical_issues.length}
                    </p>
                  </div>
                </div>
              </div>

              {results.critical_issues.length > 0 ? (
                <div className="bg-red-950/40 border border-red-700/40 rounded-2xl p-6">
                  <h4 className="flex items-center gap-2 text-red-400 font-bold mb-4 text-sm uppercase tracking-wider">
                    <AlertTriangle className="w-4 h-4" /> Fraud Indicators Detected
                  </h4>
                  <ul className="space-y-2.5">
                    {results.critical_issues.map((issue: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-red-200 text-sm">
                        <ChevronRight className="w-4 h-4 mt-0.5 shrink-0 text-red-400" />
                        {issue}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <div className="bg-emerald-950/40 border border-emerald-700/40 rounded-2xl p-6 flex items-center gap-3">
                  <CheckCircle2 className="w-6 h-6 text-emerald-400 shrink-0" />
                  <p className="text-emerald-300 font-medium">No critical anomalies detected. Document appears authentic.</p>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}
