import os

files = {
    "app/(protected)/voice/page.tsx": """'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, MicOff, Settings, History, Activity, LayoutDashboard, Search, ShieldAlert, BarChart3, FileText, Globe, Volume2 } from 'lucide-react'
import { Button } from '@/components/ui/button'

const COMMANDS = [
  { icon: LayoutDashboard, category: 'Navigation', cmds: ['"Show my dashboard"', '"Go to analytics"'] },
  { icon: Search, category: 'Case Analysis', cmds: ['"Analyze case TL-2025..."', '"Explain findings"'] },
  { icon: ShieldAlert, category: 'Actions', cmds: ['"Approve case"', '"Flag for review"'] },
  { icon: BarChart3, category: 'Information', cmds: ['"Top fraud patterns?"', '"How many pending?"'] }
]

export default function VoiceAssistantPage() {
  const [isListening, setIsListening] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [messages, setMessages] = useState<{role: 'user'|'ai', text: string}[]>([])

  // Simulated Voice Flow for Demo purposes
  const toggleListening = () => {
    if (isListening) {
      setIsListening(false)
      setTranscript('')
    } else {
      setIsListening(true)
      setTranscript('')
      // Simulate typing transcript
      setTimeout(() => setTranscript('Show me '), 600)
      setTimeout(() => setTranscript('Show me the high risk '), 1200)
      setTimeout(() => setTranscript('Show me the high risk cases from today'), 1800)
      
      // Simulate processing
      setTimeout(() => {
        setIsListening(false)
        setIsProcessing(true)
        setMessages(prev => [...prev, { role: 'user', text: 'Show me the high risk cases from today' }])
      }, 2400)

      // Simulate AI response
      setTimeout(() => {
        setIsProcessing(false)
        setTranscript('')
        setMessages(prev => [...prev, { role: 'ai', text: 'I found 4 high-risk cases from today. I have filtered your Cases dashboard to display them.' }])
      }, 4000)
    }
  }

  return (
    <div className="max-w-5xl mx-auto pb-20 pt-10">
      
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-black text-slate-900 tracking-tight mb-3">Voice Assistant</h1>
        <p className="text-slate-500 text-lg">Navigate and control TruthLens completely hands-free.</p>
        <div className="flex justify-center items-center gap-6 mt-6">
          <div className="flex items-center gap-2 text-sm font-bold text-slate-600 bg-white px-4 py-2 rounded-full border border-slate-200 shadow-sm">
            <Globe className="w-4 h-4 text-primary" /> English (India)
          </div>
          <div className="flex items-center gap-2 text-sm font-bold text-slate-600 bg-white px-4 py-2 rounded-full border border-slate-200 shadow-sm">
            <Settings className="w-4 h-4 text-slate-400" /> Settings
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Interface */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col min-h-[600px] relative">
          
          {/* Chat / Transcript Area */}
          <div className="flex-1 p-8 overflow-y-auto space-y-6 bg-slate-50/50">
            {messages.length === 0 && !isListening && (
              <div className="h-full flex flex-col items-center justify-center text-slate-400">
                <Mic className="w-12 h-12 mb-4 opacity-20" />
                <p>Tap the microphone to start speaking</p>
              </div>
            )}
            
            <AnimatePresence>
              {messages.map((msg, idx) => (
                <motion.div 
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] rounded-2xl px-6 py-4 ${msg.role === 'user' ? 'bg-primary text-white shadow-md rounded-br-sm' : 'bg-white border border-slate-200 text-slate-800 shadow-sm rounded-bl-sm'}`}>
                    {msg.role === 'ai' && <Volume2 className="w-4 h-4 text-primary mb-2" />}
                    <p className="text-sm font-medium leading-relaxed">{msg.text}</p>
                  </div>
                </motion.div>
              ))}
              
              {isProcessing && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                  <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-sm px-6 py-4 shadow-sm flex items-center gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200"></div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Active Listening Overlay */}
          <AnimatePresence>
            {isListening && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                className="absolute bottom-40 left-8 right-8 bg-slate-900 rounded-2xl p-6 shadow-2xl text-center"
              >
                <Activity className="w-6 h-6 text-emerald-400 mx-auto mb-3 animate-pulse" />
                <p className="text-white text-xl font-medium tracking-wide">
                  {transcript || <span className="text-slate-500">Listening...</span>}
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Microphone Controller */}
          <div className="h-40 bg-white border-t border-slate-200 flex items-center justify-center relative shrink-0">
            {isListening && (
              <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-primary/10 rounded-full animate-ping"></div>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-primary/5 rounded-full animate-ping delay-150"></div>
              </div>
            )}
            
            <button 
              onClick={toggleListening}
              className={`relative z-10 w-24 h-24 rounded-full flex items-center justify-center shadow-xl transition-all duration-300 ${isListening ? 'bg-red-500 scale-110 shadow-red-500/30' : isProcessing ? 'bg-slate-300 cursor-not-allowed' : 'bg-gradient-to-tr from-primary to-blue-400 hover:scale-105 shadow-primary/30'}`}
              disabled={isProcessing}
            >
              {isListening ? (
                <div className="w-8 h-8 rounded-sm bg-white"></div>
              ) : (
                <Mic className="w-10 h-10 text-white" />
              )}
            </button>
            <p className="absolute bottom-4 text-xs font-bold text-slate-400 uppercase tracking-widest">
              {isListening ? 'Tap to Stop' : isProcessing ? 'Processing' : 'Tap to Speak'}
            </p>
          </div>
        </div>

        {/* Side Panel: Commands */}
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-6 flex items-center gap-2"><History className="w-4 h-4 text-slate-400" /> Example Commands</h2>
            
            <div className="space-y-4">
              {COMMANDS.map((cat, idx) => (
                <div key={idx} className="bg-slate-50 rounded-xl p-4 border border-slate-100">
                  <div className="flex items-center gap-2 mb-3">
                    <cat.icon className="w-4 h-4 text-primary" />
                    <h3 className="text-xs font-bold text-slate-700">{cat.category}</h3>
                  </div>
                  <div className="space-y-2">
                    {cat.cmds.map((cmd, i) => (
                      <div key={i} className="text-sm text-slate-600 bg-white px-3 py-1.5 rounded-md border border-slate-200 shadow-sm font-medium">
                        {cmd}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
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
    print("Scaffolded Voice Assistant Page.")
