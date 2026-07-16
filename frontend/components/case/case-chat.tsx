'use client'

import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Send, X, Loader2, Sparkles, BookOpen, ChevronDown, MessageSquare, AlertTriangle, TrendingUp, Scale } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'ai'
  content: string
  sources?: { file: string; relevance: number }[]
  structured_data?: any
  timestamp: Date
}

interface CaseChatProps {
  caseId: string
  token: string
  isOpen: boolean
  onClose: () => void
}

const SUGGESTED_QUESTIONS = [
  "Why was this case flagged?",
  "What are the critical findings?",
  "What documents should I request?",
  "Has this PAN appeared in other cases?",
  "What's the risk score breakdown?",
  "What are the compliance violations?",
  "What actions should I take?",
  "Is this a syndicate attack?",
]

function StructuredDataCard({ data }: { data: any }) {
  if (!data) return null

  if (data.type === 'risk_breakdown' && data.scores) {
    return (
      <div className="mt-3 bg-white/50 rounded-xl border border-white/80 p-3">
        <p className="text-xs font-bold text-slate-600 mb-2 flex items-center gap-1.5">
          <TrendingUp className="w-3.5 h-3.5" /> Risk Breakdown
        </p>
        <div className="space-y-1.5">
          {Object.entries(data.scores).map(([key, val]) => (
            key !== 'category' && typeof val === 'number' && (
              <div key={key} className="flex items-center gap-2">
                <span className="text-[10px] text-slate-500 w-24 capitalize">{key.replace(/_/g, ' ')}</span>
                <div className="flex-1 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${(val as number) > 70 ? 'bg-red-500' : (val as number) > 40 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                    style={{ width: `${val}%` }}
                  />
                </div>
                <span className={`text-[10px] font-bold w-8 text-right ${(val as number) > 70 ? 'text-red-600' : (val as number) > 40 ? 'text-amber-600' : 'text-emerald-600'}`}>
                  {Math.round(val as number)}
                </span>
              </div>
            )
          ))}
        </div>
      </div>
    )
  }

  if (data.type === 'mismatches' && data.items?.length > 0) {
    return (
      <div className="mt-3 bg-white/50 rounded-xl border border-red-100 p-3">
        <p className="text-xs font-bold text-red-700 mb-2 flex items-center gap-1.5">
          <AlertTriangle className="w-3.5 h-3.5" /> {data.items.length} Mismatches Found
        </p>
        <div className="space-y-1">
          {data.items.map((m: any, i: number) => (
            <div key={i} className="text-[10px] text-slate-600 bg-red-50 rounded p-1.5">
              <span className="font-bold capitalize">{m.field}</span>: {m.val1} vs {m.val2}
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (data.type === 'compliance' && data.violations?.length > 0) {
    return (
      <div className="mt-3 bg-white/50 rounded-xl border border-amber-100 p-3">
        <p className="text-xs font-bold text-amber-700 mb-2 flex items-center gap-1.5">
          <Scale className="w-3.5 h-3.5" /> {data.violations.length} Compliance Violations
        </p>
        <div className="space-y-1">
          {data.violations.map((v: any, i: number) => (
            <div key={i} className="text-[10px] text-slate-600 bg-amber-50 rounded p-1.5">{v}</div>
          ))}
        </div>
      </div>
    )
  }

  return null
}

export function CaseChat({ caseId, token, isOpen, onClose }: CaseChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'ai',
      content: "Hello! I'm the TruthLens AI Interrogator. Ask me anything about this case — fraud findings, risk scores, compliance issues, or what actions to take next.",
      timestamp: new Date(),
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (isOpen) setTimeout(() => inputRef.current?.focus(), 100)
  }, [isOpen])

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    setShowSuggestions(false)

    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const history = messages.slice(-6).map(m => ({
        role: m.role === 'user' ? 'user' : 'assistant',
        content: m.content,
      }))

      const resp = await fetch(`${BASE}/api/v1/cases/${caseId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ question: text, history }),
      })

      const data = await resp.json()

      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: data.answer || "I couldn't find specific information about that. Please try rephrasing your question.",
        sources: data.sources,
        structured_data: data.structured_data,
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, aiMsg])
    } catch (e) {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: 'Connection error. Please check if the backend is running.',
        timestamp: new Date(),
      }])
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, x: 40, scale: 0.95 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        exit={{ opacity: 0, x: 40, scale: 0.95 }}
        transition={{ type: 'spring', damping: 28, stiffness: 300 }}
        className="fixed bottom-6 right-6 w-[420px] h-[620px] z-[100] flex flex-col rounded-3xl overflow-hidden shadow-2xl shadow-slate-900/20 border border-slate-200"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-slate-900 to-blue-950 px-5 py-4 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-900/50">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 rounded-full border-2 border-slate-900 animate-pulse" />
            </div>
            <div>
              <h3 className="text-white font-bold text-sm">TruthLens AI Interrogator</h3>
              <p className="text-blue-300 text-[10px] font-medium">Powered by CRAG + Ollama llama3.1:8b</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors p-1.5 rounded-lg hover:bg-white/10">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto bg-slate-50 p-4 space-y-4">
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} gap-2`}
            >
              {msg.role === 'ai' && (
                <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center shrink-0 mt-1 shadow-sm">
                  <Sparkles className="w-3.5 h-3.5 text-white" />
                </div>
              )}
              <div className={`max-w-[85%] ${msg.role === 'user' ? 'order-first' : ''}`}>
                <div className={`rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-md'
                    : 'bg-white text-slate-800 border border-slate-100 rounded-bl-md'
                }`}>
                  {msg.content}
                </div>

                {/* Structured data widget */}
                {msg.structured_data && <StructuredDataCard data={msg.structured_data} />}

                {/* Sources */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {msg.sources.map((src, i) => (
                      <span key={i} className="inline-flex items-center gap-1 text-[9px] font-bold text-blue-600 bg-blue-50 border border-blue-100 px-2 py-0.5 rounded-full">
                        <BookOpen className="w-2.5 h-2.5" />
                        {src.file ? src.file.split('/').pop() : 'Knowledge Base'} · {Math.round(src.relevance * 100)}%
                      </span>
                    ))}
                  </div>
                )}

                <p className="text-[9px] text-slate-400 mt-1 px-1">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </motion.div>
          ))}

          {/* Typing indicator */}
          {loading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-2">
              <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center shrink-0 shadow-sm">
                <Sparkles className="w-3.5 h-3.5 text-white" />
              </div>
              <div className="bg-white border border-slate-100 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                <div className="flex gap-1">
                  <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        <AnimatePresence>
          {showSuggestions && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="bg-white border-t border-slate-100 px-4 py-3 overflow-hidden"
            >
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Suggested Questions</p>
              <div className="flex flex-wrap gap-1.5">
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    className="text-[10px] font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-100 px-2.5 py-1 rounded-full transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Input */}
        <div className="bg-white border-t border-slate-200 px-4 py-3 flex items-center gap-2 shrink-0">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage(input)}
            placeholder="Ask anything about this case..."
            disabled={loading}
            className="flex-1 text-sm outline-none text-slate-900 placeholder:text-slate-400 bg-transparent"
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || loading}
            className="w-9 h-9 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 disabled:text-slate-400 text-white rounded-xl flex items-center justify-center transition-all shadow-sm disabled:shadow-none"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  )
}

// Floating chat button
export function CaseChatButton({ onClick, isOpen }: { onClick: () => void; isOpen: boolean }) {
  return (
    <motion.button
      onClick={onClick}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`fixed bottom-6 right-6 z-[99] flex items-center gap-2.5 px-5 py-3.5 rounded-2xl shadow-2xl transition-all ${
        isOpen
          ? 'bg-slate-800 text-white shadow-slate-900/30'
          : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-blue-900/30'
      }`}
    >
      {isOpen ? <X className="w-5 h-5" /> : <MessageSquare className="w-5 h-5" />}
      <span className="text-sm font-bold">{isOpen ? 'Close Chat' : 'AI Interrogator'}</span>
      {!isOpen && (
        <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
      )}
    </motion.button>
  )
}
