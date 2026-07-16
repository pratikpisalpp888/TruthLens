'use client'

import { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, ShieldCheck, Zap, Brain } from 'lucide-react'
import { Button } from '@/components/ui/button'

// Animated cycling words that describe what TruthLens does
const cyclingWords = [
  'in 90 Seconds',
  'with 7 AI Layers',
  'Completely Offline',
  'with Zero Errors',
  'Before It Costs You',
]

export function HeroSection() {
  const [wordIndex, setWordIndex] = useState(0)

  useEffect(() => {
    const id = setTimeout(() => {
      setWordIndex((prev) => (prev + 1) % cyclingWords.length)
    }, 2200)
    return () => clearTimeout(id)
  }, [wordIndex])

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.15, delayChildren: 0.2 } },
  }
  const itemVariants = {
    hidden: { opacity: 0, y: 28 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8 } },
  }

  return (
    <section className="relative w-full min-h-screen overflow-hidden hero-gradient flex items-center justify-center pt-28 pb-32">
      {/* Background blobs — same as before */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-blue-400/20 blur-3xl" />
        <div className="absolute top-1/2 right-0 w-[500px] h-[500px] rounded-full bg-amber-500/10 blur-3xl" />
        <div className="absolute bottom-0 left-1/3 w-72 h-72 rounded-full bg-blue-600/20 blur-3xl" />
      </div>

      <div className="relative z-10 w-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center text-center">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="flex flex-col items-center gap-6 sm:gap-8"
        >
          {/* Top badge */}
          <motion.div
            variants={itemVariants}
            className="inline-flex items-center gap-2 bg-white/10 border border-white/25 px-4 py-1.5 rounded-full backdrop-blur-sm"
          >
            <ShieldCheck className="w-4 h-4 text-amber-400" />
            <span className="text-xs font-semibold tracking-widest text-white/90 uppercase">
              Offline-First · Agentic AI · Bank-Grade
            </span>
          </motion.div>

          {/* Project name with Logo */}
          <motion.div variants={itemVariants} className="flex flex-col items-center justify-center mt-2 mb-2 w-full">
            <div className="flex flex-col md:flex-row items-center justify-center w-full">
              
              {/* Left Side: TruthLens */}
              <div className="flex-1 flex justify-end">
                <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black text-white tracking-tight leading-none drop-shadow-lg">
                  TruthLens
                </h1>
              </div>
              
              {/* Center: X */}
              <div className="flex-shrink-0 px-4 sm:px-8 py-2 md:py-0">
                <span className="text-3xl md:text-5xl text-white/50 font-light tracking-widest drop-shadow-md">✕</span>
              </div>
              
              {/* Right Side: Canara Bank */}
              <div className="flex-1 flex justify-start items-center transform hover:scale-105 transition-transform duration-300 drop-shadow-xl">
                <img 
                  src="/canara-bank-icon-trans.png" 
                  alt="Canara Bank Icon" 
                  className="h-16 sm:h-20 lg:h-24 object-contain -ml-2 -mr-4 sm:-mr-8" 
                />
                <span className="text-5xl sm:text-6xl lg:text-7xl font-black text-white tracking-tight whitespace-nowrap">
                  Canara Bank
                </span>
              </div>
              
            </div>
            <div className="mt-8 h-1.5 w-32 mx-auto rounded-full bg-gradient-to-r from-amber-400 to-amber-200 opacity-90 shadow-[0_0_15px_rgba(251,191,36,0.5)]" />
          </motion.div>

          {/* Animated headline with cycling words */}
          <motion.div variants={itemVariants} className="w-full">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white/90 tracking-tight">
              <span>Detect Loan Fraud</span>{' '}
              {/* Cycling animated word container */}
              <span className="relative inline-flex justify-center overflow-hidden h-[1.2em] align-bottom w-full sm:w-auto">
                {cyclingWords.map((word, i) => (
                  <motion.span
                    key={i}
                    className="absolute font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-amber-200 whitespace-nowrap"
                    initial={{ opacity: 0, y: 60 }}
                    animate={
                      wordIndex === i
                        ? { y: 0, opacity: 1 }
                        : { y: wordIndex > i ? -60 : 60, opacity: 0 }
                    }
                    transition={{ type: 'spring', stiffness: 60, damping: 14 }}
                  >
                    {word}
                  </motion.span>
                ))}
              </span>
            </h2>
          </motion.div>

          {/* Subheadline */}
          <motion.p
            variants={itemVariants}
            className="text-base sm:text-lg text-blue-100/80 max-w-2xl leading-relaxed font-light"
          >
            AI-powered forensic co-pilot for bank underwriting. Seven intelligence layers
            analyze every document. Five AI agents collaborate autonomously. Completely offline.
          </motion.p>

          {/* Stat pills */}
          <motion.div variants={itemVariants} className="flex flex-wrap gap-3 justify-center">
            {[
              { icon: Zap, label: '90s Analysis' },
              { icon: Brain, label: '7 Intelligence Layers' },
              { icon: ShieldCheck, label: 'Zero Cloud' },
            ].map(({ icon: Icon, label }) => (
              <div
                key={label}
                className="flex items-center gap-1.5 bg-white/10 border border-white/20 rounded-full px-3 py-1.5 text-xs text-white/80 font-medium backdrop-blur-sm"
              >
                <Icon className="w-3.5 h-3.5 text-amber-400" />
                {label}
              </div>
            ))}
          </motion.div>

          {/* CTA buttons */}
          <motion.div
            variants={itemVariants}
            className="flex flex-col sm:flex-row items-center gap-4 pt-2"
          >
            <Link href="/login">
              <Button
                size="lg"
                className="h-14 px-10 rounded-full bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-600 hover:to-amber-500 text-primary-900 font-bold text-lg shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300"
              >
                Access Portal <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <Link href="/features">
              <Button
                size="lg"
                variant="outline"
                className="h-14 px-8 rounded-full bg-white/10 border-white/30 text-white hover:bg-white/20 font-semibold backdrop-blur-sm transition-all duration-300"
              >
                See How It Works
              </Button>
            </Link>
          </motion.div>

          {/* Trust note */}
          <motion.div
            variants={itemVariants}
            className="flex items-center gap-2 text-blue-200/60 text-xs"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-green-400" />
            <span>Deployed on your bank infrastructure — Zero cloud dependency</span>
          </motion.div>
        </motion.div>
      </div>

      {/* Bottom Wave Divider */}
      <div className="absolute bottom-0 left-0 right-0 w-full overflow-hidden leading-none z-20 transform translate-y-[1px]">
        <svg
          className="relative block w-full h-[60px] md:h-[100px]"
          data-name="Layer 1"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1200 120"
          preserveAspectRatio="none"
        >
          <path
            d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V120H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
            className="fill-white"
          />
        </svg>
      </div>
    </section>
  )
}
