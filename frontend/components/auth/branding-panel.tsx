'use client'

import { motion } from 'framer-motion'

export function BrandingPanel() {
  return (
    <div className="hidden lg:flex w-full h-full bg-[#030712] flex-col items-center justify-center relative overflow-hidden">
      
      {/* Deep cinematic background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-[#030712] to-[#030712]" />
      
      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.15] mix-blend-overlay pointer-events-none" />

      {/* Cinematic Glowing Orbs */}
      <motion.div 
        animate={{ 
          scale: [1, 1.2, 1],
          opacity: [0.2, 0.4, 0.2],
          rotate: [0, 90, 0]
        }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-600/30 rounded-full blur-[100px] pointer-events-none"
      />
      <motion.div 
        animate={{ 
          scale: [1, 1.4, 1],
          opacity: [0.1, 0.3, 0.1],
        }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-amber-500/20 rounded-full blur-[80px] pointer-events-none"
      />

      {/* Concentric Rings */}
      <motion.div 
        animate={{ rotate: 360 }}
        transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full border border-white/[0.03] border-dashed"
      />
      <motion.div 
        animate={{ rotate: -360 }}
        transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] rounded-full border border-white/[0.05]"
      />

      {/* Center Cinematic Branding */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.9, filter: 'blur(10px)' }}
        animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
        transition={{ duration: 1.5, ease: "easeOut" }}
        className="relative z-10 flex flex-col items-center text-center"
      >
        <span className="text-[5.5rem] font-black text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-white/40 tracking-tighter mb-4 drop-shadow-2xl">
          TruthLens
        </span>
        <div className="w-24 h-[2px] bg-gradient-to-r from-transparent via-amber-400 to-transparent mb-8" />
        <p className="text-blue-200/70 text-2xl font-light tracking-wide max-w-lg leading-relaxed">
          The autonomous AI co-pilot for forensic loan underwriting.
        </p>
      </motion.div>

      {/* Bottom Trust Indicators */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1, duration: 0.8 }}
        className="absolute bottom-12 z-10 flex flex-col items-center"
      >
        <div className="flex gap-2.5 mb-3">
          <div className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse shadow-[0_0_10px_rgba(251,191,36,0.8)]" />
          <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse delay-75 shadow-[0_0_10px_rgba(96,165,250,0.8)]" />
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse delay-150 shadow-[0_0_10px_rgba(52,211,153,0.8)]" />
        </div>
        <p className="text-[10px] text-blue-300/40 uppercase tracking-[0.3em] font-bold">
          Canara Bank SuRaksha Hackathon
        </p>
      </motion.div>
    </div>
  )
}
