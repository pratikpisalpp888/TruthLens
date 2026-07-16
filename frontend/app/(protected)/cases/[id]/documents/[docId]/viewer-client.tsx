'use client'

import React, { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, ZoomIn, ZoomOut, ShieldCheck, ShieldAlert, AlertTriangle, Info, Eye, EyeOff } from 'lucide-react'
import { useAuthStore } from '@/stores/auth-store'

// Severity config
const SEVERITY_STYLE: Record<string, { border: string; bg: string; badge: string; text: string; icon: React.ReactNode }> = {
  critical: {
    border: 'border-red-500',
    bg: 'bg-red-400/30',
    badge: 'bg-red-100 text-red-800 border border-red-200',
    text: 'text-red-700',
    icon: <AlertTriangle className="w-3.5 h-3.5 text-red-600" />,
  },
  high: {
    border: 'border-orange-500',
    bg: 'bg-orange-400/25',
    badge: 'bg-orange-100 text-orange-800 border border-orange-200',
    text: 'text-orange-700',
    icon: <AlertTriangle className="w-3.5 h-3.5 text-orange-500" />,
  },
  medium: {
    border: 'border-yellow-400',
    bg: 'bg-yellow-300/20',
    badge: 'bg-yellow-100 text-yellow-800 border border-yellow-200',
    text: 'text-yellow-700',
    icon: <Info className="w-3.5 h-3.5 text-yellow-500" />,
  },
  low: {
    border: 'border-blue-400',
    bg: 'bg-blue-300/15',
    badge: 'bg-blue-100 text-blue-700 border border-blue-200',
    text: 'text-blue-600',
    icon: <Info className="w-3.5 h-3.5 text-blue-400" />,
  },
}

function getSeverityStyle(severity: string) {
  return SEVERITY_STYLE[severity] || SEVERITY_STYLE.medium
}

export default function DocumentViewerClient({ params }: { params: { id: string; docId: string } }) {
  const router = useRouter()
  const token = useAuthStore(state => state.token)

  // PDF state
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [pdfDoc, setPdfDoc] = useState<any>(null)
  const [pdfjsReady, setPdfjsReady] = useState(false)
  const [numPages, setNumPages] = useState(1)
  const [pageNumber, setPageNumber] = useState(1)
  const [scale, setScale] = useState(1.3)
  const [canvasSize, setCanvasSize] = useState({ width: 0, height: 0 })

  // Data state
  const [pdfUrl, setPdfUrl] = useState<string | null>(null)
  const [annotations, setAnnotations] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showOverlays, setShowOverlays] = useState(true)
  const [activeAnnotation, setActiveAnnotation] = useState<number | null>(null)

  // ── Step 1: Inject pdf.js from CDN (no npm, no Webpack crash) ────────────
  useEffect(() => {
    const existingScript = document.getElementById('pdfjs-cdn-script')
    if (existingScript) {
      setPdfjsReady(true)
      return
    }
    const script = document.createElement('script')
    script.id = 'pdfjs-cdn-script'
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js'
    script.onload = () => {
      // @ts-ignore
      window.pdfjsLib.GlobalWorkerOptions.workerSrc =
        'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'
      setPdfjsReady(true)
    }
    script.onerror = () => {
      // Fallback to unpkg
      const s2 = document.createElement('script')
      s2.src = 'https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.min.js'
      s2.onload = () => {
        // @ts-ignore
        window.pdfjsLib.GlobalWorkerOptions.workerSrc =
          'https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js'
        setPdfjsReady(true)
      }
      document.body.appendChild(s2)
    }
    document.body.appendChild(script)
  }, [])

  // ── Step 2: Fetch document preview + annotations from backend ────────────
  useEffect(() => {
    if (!token) return
    const BASE = process.env.NEXT_PUBLIC_API_URL || ''
    setLoading(true)

    Promise.all([
      // Fetch the decrypted PDF blob
      fetch(`${BASE}/api/v1/documents/${params.docId}/preview`, {
        headers: { Authorization: `Bearer ${token}` },
      }).then(r => r.ok ? r.blob() : null),

      // Fetch fraud annotations (bounding boxes)
      fetch(`${BASE}/api/v1/documents/${params.docId}/annotations`, {
        headers: { Authorization: `Bearer ${token}` },
      }).then(r => r.ok ? r.json() : { anomaly_regions: [] }),
    ]).then(([blob, annData]) => {
      if (blob) setPdfUrl(URL.createObjectURL(blob))
      setAnnotations(annData?.anomaly_regions || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [params.docId, token])

  // ── Step 3: Load PDF via pdf.js ──────────────────────────────────────────
  useEffect(() => {
    if (!pdfjsReady || !pdfUrl) return
    // @ts-ignore
    window.pdfjsLib.getDocument(pdfUrl).promise.then((pdf: any) => {
      setPdfDoc(pdf)
      setNumPages(pdf.numPages)
    })
  }, [pdfjsReady, pdfUrl])

  // ── Step 4: Render page to canvas ────────────────────────────────────────
  useEffect(() => {
    if (!pdfDoc || !canvasRef.current) return
    pdfDoc.getPage(pageNumber).then((page: any) => {
      const viewport = page.getViewport({ scale })
      const canvas = canvasRef.current!
      canvas.width = viewport.width
      canvas.height = viewport.height
      setCanvasSize({ width: viewport.width, height: viewport.height })
      const ctx = canvas.getContext('2d')!
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      page.render({ canvasContext: ctx, viewport })
    })
  }, [pdfDoc, pageNumber, scale])

  // Filter annotations to the current page
  const pageAnnotations = annotations.filter(a => a.page === pageNumber)
  const allHighSeverity = annotations.filter(a => a.severity === 'critical' || a.severity === 'high')

  const isClean = annotations.length === 0

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col bg-[#0f1117] overflow-hidden -mx-6 -my-8 absolute inset-0 top-16 z-40 text-slate-200">
      <div className="flex flex-1 overflow-hidden">

        {/* ── Left Panel: Findings Sidebar ── */}
        <div className="w-80 bg-[#181c27] border-r border-slate-700/60 flex flex-col shrink-0">
          {/* Header */}
          <div className="p-4 border-b border-slate-700/60">
            <button
              onClick={() => router.push(`/cases/${params.id}`)}
              className="flex items-center gap-2 text-xs text-slate-400 hover:text-slate-100 transition-colors mb-4"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Back to Case
            </button>
            <h2 className="font-bold text-base text-slate-100">Fraud Intelligence</h2>
            <p className="text-xs text-slate-400 mt-0.5">Document annotation viewer</p>
          </div>

          {/* Status Badge */}
          <div className="px-4 py-3 border-b border-slate-700/40">
            {loading ? (
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <div className="w-4 h-4 border-2 border-slate-600 border-t-indigo-400 rounded-full animate-spin" />
                Loading analysis...
              </div>
            ) : isClean ? (
              <div className="flex items-center gap-2.5 px-3 py-2 rounded-lg bg-emerald-900/40 border border-emerald-700/50">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
                <div>
                  <p className="text-xs font-bold text-emerald-300">Document Appears Clean</p>
                  <p className="text-[11px] text-emerald-500">No fraud indicators detected</p>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-2.5 px-3 py-2 rounded-lg bg-red-900/30 border border-red-700/50">
                <ShieldAlert className="w-4 h-4 text-red-400 shrink-0" />
                <div>
                  <p className="text-xs font-bold text-red-300">{annotations.length} Finding{annotations.length !== 1 ? 's' : ''} Detected</p>
                  <p className="text-[11px] text-red-500">{allHighSeverity.length} critical/high severity</p>
                </div>
              </div>
            )}
          </div>

          {/* Findings List */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {annotations.length === 0 && !loading && (
              <div className="text-center py-12 text-slate-500">
                <ShieldCheck className="w-8 h-8 mx-auto mb-2 text-emerald-600 opacity-60" />
                <p className="text-sm">No anomalies found</p>
              </div>
            )}
            {annotations.map((ann, idx) => {
              const style = getSeverityStyle(ann.severity)
              const isActive = activeAnnotation === idx
              return (
                <button
                  key={idx}
                  onClick={() => {
                    setPageNumber(ann.page || 1)
                    setActiveAnnotation(isActive ? null : idx)
                  }}
                  className={`w-full text-left p-3 rounded-xl border transition-all ${
                    isActive
                      ? `${style.border} bg-slate-800/80 shadow-md`
                      : 'border-slate-700/50 bg-slate-800/40 hover:bg-slate-800/70'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${style.badge}`}>
                      {ann.severity}
                    </span>
                    <span className="text-[10px] text-slate-500">Page {ann.page || 1}</span>
                  </div>
                  <p className="text-xs font-semibold text-slate-200 mb-0.5">{ann.label || ann.check_type}</p>
                  <p className="text-[11px] text-slate-400 leading-relaxed line-clamp-2">{ann.reason || ann.description}</p>
                </button>
              )
            })}
          </div>
        </div>

        {/* ── Right Panel: PDF Canvas Viewer ── */}
        <div className="flex-1 flex flex-col bg-[#12151e]">
          {/* Toolbar */}
          <div className="h-12 bg-[#181c27] border-b border-slate-700/60 flex items-center justify-between px-5 shrink-0">
            {/* Page nav */}
            <div className="flex items-center gap-2 text-sm">
              <button
                onClick={() => setPageNumber(p => Math.max(1, p - 1))}
                disabled={pageNumber <= 1}
                className="px-2.5 py-1 rounded-lg bg-slate-700/60 text-slate-300 hover:bg-slate-600 disabled:opacity-30 text-xs font-medium"
              >← Prev</button>
              <span className="text-slate-400 text-xs font-mono min-w-[50px] text-center">
                {pageNumber} / {numPages}
              </span>
              <button
                onClick={() => setPageNumber(p => Math.min(numPages, p + 1))}
                disabled={pageNumber >= numPages}
                className="px-2.5 py-1 rounded-lg bg-slate-700/60 text-slate-300 hover:bg-slate-600 disabled:opacity-30 text-xs font-medium"
              >Next →</button>
            </div>

            {/* Controls */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowOverlays(v => !v)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                  showOverlays
                    ? 'bg-red-900/40 text-red-300 border-red-700/60'
                    : 'bg-slate-700/40 text-slate-400 border-slate-600/40'
                }`}
              >
                {showOverlays ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
                {showOverlays ? 'Overlays On' : 'Overlays Off'}
              </button>
              <div className="w-px h-5 bg-slate-700" />
              <button onClick={() => setScale(s => Math.max(0.5, s - 0.2))} className="p-1.5 text-slate-400 hover:text-slate-100 hover:bg-slate-700 rounded-lg transition-colors">
                <ZoomOut className="w-4 h-4" />
              </button>
              <span className="text-xs text-slate-400 font-mono w-10 text-center">{Math.round(scale * 100)}%</span>
              <button onClick={() => setScale(s => Math.min(3, s + 0.2))} className="p-1.5 text-slate-400 hover:text-slate-100 hover:bg-slate-700 rounded-lg transition-colors">
                <ZoomIn className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Canvas Area */}
          <div ref={containerRef} className="flex-1 overflow-auto flex justify-center items-start p-8 bg-[#0d1018]">
            {loading || !pdfjsReady ? (
              <div className="flex flex-col items-center justify-center h-[600px] gap-3 text-slate-500">
                <div className="w-8 h-8 border-4 border-slate-700 border-t-indigo-500 rounded-full animate-spin" />
                <p className="text-sm">Loading document viewer...</p>
              </div>
            ) : !pdfUrl ? (
              <div className="flex flex-col items-center justify-center h-[600px] gap-3 text-slate-500">
                <ShieldAlert className="w-10 h-10 text-slate-600" />
                <p className="text-sm">Document could not be loaded. Run analysis first.</p>
              </div>
            ) : (
              // Canvas + overlay container — must be position:relative
              <div
                className="relative shadow-2xl rounded-sm bg-white"
                style={{ width: canvasSize.width || 'auto', height: canvasSize.height || 'auto' }}
              >
                <canvas ref={canvasRef} className="block rounded-sm" />

                {/* Fraud Annotation Overlays */}
                {showOverlays && canvasSize.width > 0 && pageAnnotations.map((ann, idx) => {
                  const style = getSeverityStyle(ann.severity)
                  // Normalise coordinates to canvas pixel space
                  // Backend stores PDF-space coords (595.276 × 841.890 standard A4)
                  const PDF_W = 595.276
                  const PDF_H = 841.890
                  const scaleX = canvasSize.width / PDF_W
                  const scaleY = canvasSize.height / PDF_H

                  return (
                    <div
                      key={`overlay-${idx}`}
                      title={ann.label || ann.check_type}
                      className={`absolute pointer-events-none border-2 ${style.border} ${style.bg} rounded-[2px]`}
                      style={{
                        left: (ann.x || 0) * scaleX,
                        top: (ann.y || 0) * scaleY,
                        width: Math.max((ann.width || 50) * scaleX, 30),
                        height: Math.max((ann.height || 20) * scaleY, 16),
                      }}
                    >
                      {/* Label badge top-left */}
                      <span
                        className={`absolute -top-5 left-0 text-[9px] font-bold px-1.5 py-0.5 rounded whitespace-nowrap ${style.badge}`}
                        style={{ pointerEvents: 'none' }}
                      >
                        {ann.label || ann.severity?.toUpperCase()}
                      </span>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
