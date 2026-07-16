import os

components = {
    "components/landing/navigation.tsx": """'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { Shield, Menu, X, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function Navigation() {
  const [scrolled, setScrolled] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navLinks = [
    { name: 'Features', href: '/features' },
    { name: 'How It Works', href: '/how-it-works' },
    { name: 'About', href: '/about' },
  ]

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/80 backdrop-blur-md shadow-sm border-b border-border' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="bg-primary p-2 rounded-lg group-hover:bg-primary/90 transition-colors">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-primary-900 tracking-tight">TruthLens</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-8">
            <div className="flex gap-6">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  className="text-sm font-medium text-slate-600 hover:text-primary transition-colors"
                >
                  {link.name}
                </Link>
              ))}
            </div>
            <Link href="/login">
              <Button className="bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-600 hover:to-amber-500 text-primary-900 font-semibold shadow-md transition-all hover:shadow-lg rounded-full px-6">
                Access Portal <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </Link>
          </div>

          {/* Mobile Menu Toggle */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-600 hover:text-primary"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Nav */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-white border-b border-border overflow-hidden"
          >
            <div className="px-4 pt-2 pb-6 space-y-4 flex flex-col">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="block px-3 py-2 text-base font-medium text-slate-700 hover:text-primary hover:bg-slate-50 rounded-md"
                >
                  {link.name}
                </Link>
              ))}
              <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                <Button className="w-full bg-gradient-to-r from-amber-500 to-amber-400 text-primary-900 font-semibold rounded-full mt-4">
                  Access Portal <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
""",
    
    "components/landing/hero-section.tsx": """'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, ShieldCheck } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function HeroSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8 } },
  }

  return (
    <section className="relative w-full min-h-screen pt-32 pb-20 overflow-hidden hero-gradient flex items-center">
      {/* Subtle Background Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-blue-400/20 blur-3xl"></div>
        <div className="absolute top-1/2 right-0 w-[500px] h-[500px] rounded-full bg-amber-500/10 blur-3xl"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
        <div className="grid lg:grid-cols-[60%_40%] gap-12 items-center">
          
          {/* Left Content */}
          <motion.div
            initial="hidden"
            animate="visible"
            variants={containerVariants}
            className="space-y-8"
          >
            {/* Badge */}
            <motion.div variants={itemVariants} className="inline-flex items-center gap-2 bg-white/10 border border-white/20 px-4 py-1.5 rounded-full backdrop-blur-sm">
              <ShieldCheck className="w-4 h-4 text-amber-400" />
              <span className="text-xs font-semibold tracking-wide text-white">Offline-First • Agentic AI • Bank-Grade</span>
            </motion.div>

            {/* Headline */}
            <motion.h1 variants={itemVariants} className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white leading-[1.1] tracking-tight">
              Detect Loan Document Fraud in <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-amber-200">90 Seconds</span>
            </motion.h1>

            {/* Subheadline */}
            <motion.p variants={itemVariants} className="text-lg sm:text-xl text-blue-100 max-w-2xl leading-relaxed font-light">
              AI-powered forensic co-pilot for bank underwriting. Seven intelligence layers analyze every document. Five AI agents collaborate autonomously. Completely offline.
            </motion.p>

            {/* CTA */}
            <motion.div variants={itemVariants} className="flex flex-col sm:flex-row items-start sm:items-center gap-4 pt-4">
              <Link href="/login">
                <Button size="lg" className="h-14 px-8 rounded-full bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-600 hover:to-amber-500 text-primary-900 font-bold text-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all">
                  Access Portal <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
              <div className="flex items-center gap-3 px-4 py-2">
                <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center shrink-0">
                  <ShieldCheck className="w-5 h-5 text-green-400" />
                </div>
                <div className="flex flex-col">
                  <span className="text-sm font-semibold text-white">Zero cloud dependency</span>
                  <span className="text-xs text-blue-200">Deployed on bank infrastructure</span>
                </div>
              </div>
            </motion.div>
          </motion.div>

          {/* Right Content / Mockup */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1, delay: 0.5 }}
            className="hidden lg:block relative"
          >
            <div className="relative w-full aspect-square max-w-lg mx-auto">
              {/* Dashboard Preview Glass Card */}
              <div className="absolute inset-0 rounded-2xl border border-white/20 bg-white/10 backdrop-blur-md shadow-2xl p-6 flex flex-col gap-4 transform rotate-2 hover:rotate-0 transition-transform duration-500">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-400"></div>
                    <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                    <div className="w-3 h-3 rounded-full bg-green-400"></div>
                  </div>
                  <div className="text-white/60 text-xs font-mono">Live Analysis</div>
                </div>
                <div className="space-y-4">
                  <div className="h-20 rounded-lg bg-white/5 border border-white/10 flex items-center p-4 gap-4">
                    <div className="w-12 h-12 rounded-full bg-amber-500/20 flex items-center justify-center border border-amber-500/30">
                      <span className="text-amber-400 font-bold text-sm">98%</span>
                    </div>
                    <div className="flex-1 space-y-2">
                      <div className="h-4 bg-white/20 rounded w-1/3"></div>
                      <div className="h-3 bg-white/10 rounded w-full"></div>
                    </div>
                  </div>
                  <div className="h-20 rounded-lg bg-white/5 border border-white/10 flex items-center p-4 gap-4">
                    <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center border border-green-500/30">
                      <span className="text-green-400 font-bold text-sm">OK</span>
                    </div>
                    <div className="flex-1 space-y-2">
                      <div className="h-4 bg-white/20 rounded w-1/2"></div>
                      <div className="h-3 bg-white/10 rounded w-5/6"></div>
                    </div>
                  </div>
                </div>
                <div className="mt-auto pt-4 border-t border-white/10 flex justify-between items-center">
                  <div className="text-white/80 text-sm font-medium">Cross-Doc Intelligence</div>
                  <div className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-200 text-xs border border-blue-500/30">Active</div>
                </div>
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  )
}
""",

    "components/landing/metrics-bar.tsx": """'use client'

import { motion } from 'framer-motion'
import { Timer, Layers, Bot, WifiOff } from 'lucide-react'

export function MetricsBar() {
  const metrics = [
    { number: '90s', label: 'Average analysis time', icon: Timer, color: 'text-primary-600' },
    { number: '7', label: 'Intelligence layers', icon: Layers, color: 'text-amber-500' },
    { number: '5', label: 'Autonomous AI agents', icon: Bot, color: 'text-primary-600' },
    { number: '100%', label: 'Offline capable', icon: WifiOff, color: 'text-green-500' },
  ]

  return (
    <section className="bg-slate-50 py-12 border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 divide-x-0 md:divide-x divide-slate-200">
          {metrics.map((metric, i) => {
            const Icon = metric.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
                className="flex flex-col items-center text-center px-4"
              >
                <div className={`p-3 rounded-full bg-white shadow-sm mb-4 border border-slate-100 ${metric.color}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className={`text-4xl md:text-5xl font-black mb-2 tracking-tight ${metric.color}`}>
                  {metric.number}
                </h3>
                <p className="text-sm md:text-base font-medium text-slate-500">
                  {metric.label}
                </p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
""",

    "components/landing/problem-section.tsx": """'use client'

import { motion } from 'framer-motion'
import { Clock, EyeOff, FileX } from 'lucide-react'

export function ProblemSection() {
  const problems = [
    {
      icon: Clock,
      title: 'Days, Not Seconds',
      description: 'Loan officers spend 3-7 days manually verifying documents for a single application, delaying genuine customers and overwhelming teams.',
    },
    {
      icon: EyeOff,
      title: 'Invisible to Human Eyes',
      description: 'Modern document tampering through PDF editors, metadata manipulation, and image forensics goes undetected without specialized forensic analysis.',
    },
    {
      icon: FileX,
      title: 'Isolated Verification',
      description: 'Documents are verified individually, missing the fraud that hides in mismatches between ITR income, bank statements, and property records.',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.2 } },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  }

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white relative">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16 space-y-4"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 tracking-tight">
            Manual Verification Cannot Scale
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            The three critical gaps in traditional loan underwriting that expose banks to sophisticated fraud rings.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-8"
        >
          {problems.map((problem, i) => {
            const Icon = problem.icon
            return (
              <motion.div
                key={i}
                variants={itemVariants}
                className="bg-white rounded-2xl p-8 border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group"
              >
                <div className="w-14 h-14 rounded-full bg-amber-50 flex items-center justify-center mb-6 group-hover:bg-amber-100 transition-colors">
                  <Icon className="w-7 h-7 text-amber-500" />
                </div>
                <h3 className="text-xl font-bold text-primary-900 mb-4">{problem.title}</h3>
                <p className="text-slate-600 leading-relaxed">{problem.description}</p>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
""",

    "components/landing/solution-flow.tsx": """'use client'

import { motion } from 'framer-motion'
import { UploadCloud, BrainCircuit, ShieldCheck } from 'lucide-react'

export function SolutionFlow() {
  const steps = [
    {
      num: '01',
      title: 'Upload',
      desc: 'Drag and drop all loan documents. Auto-classification identifies types instantly.',
      icon: UploadCloud,
    },
    {
      num: '02',
      title: 'Analyze',
      desc: 'Five specialized AI agents run seven intelligence layers in parallel.',
      icon: BrainCircuit,
    },
    {
      num: '03',
      title: 'Decide',
      desc: 'Trust score, forensic evidence, and regulatory citations delivered in 90 seconds.',
      icon: ShieldCheck,
    }
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50 relative overflow-hidden">
      <div className="max-w-7xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-4 tracking-tight">
            One Platform. <span className="text-primary-600">Complete Intelligence.</span>
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            From document upload to court-ready evidence in three simple steps.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-12 relative">
          {/* Animated Connecting Line (Desktop) */}
          <div className="hidden md:block absolute top-1/2 left-[10%] right-[10%] h-0.5 bg-gradient-to-r from-slate-200 via-primary-300 to-slate-200 -z-10 transform -translate-y-1/2">
            <motion.div 
              initial={{ width: 0 }}
              whileInView={{ width: '100%' }}
              transition={{ duration: 1.5, ease: "easeInOut" }}
              viewport={{ once: true }}
              className="h-full bg-primary-500"
            />
          </div>

          {steps.map((step, i) => {
            const Icon = step.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.3, duration: 0.6 }}
                className="relative bg-white p-8 rounded-2xl shadow-lg border border-slate-100 flex flex-col items-center text-center group hover:border-primary-200 transition-colors"
              >
                <div className="absolute -top-6 bg-white w-12 h-12 rounded-full flex items-center justify-center font-black text-xl text-primary-900 border-2 border-primary-100 shadow-sm group-hover:border-primary-500 transition-colors">
                  {step.num}
                </div>
                <div className="w-20 h-20 rounded-full bg-primary-50 flex items-center justify-center mt-4 mb-6 group-hover:bg-primary-100 transition-colors">
                  <Icon className="w-10 h-10 text-primary-600" />
                </div>
                <h3 className="text-xl font-bold text-primary-900 mb-3">{step.title}</h3>
                <p className="text-slate-600 leading-relaxed">{step.desc}</p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
""",

    "components/landing/layers-section.tsx": """'use client'

import { motion } from 'framer-motion'
import { Scan, Languages, GitCompare, FileText, Dna, BrainCircuit, Gavel } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

export function LayersSection() {
  const layers = [
    {
      title: 'Document Forensics',
      desc: 'Error Level Analysis, metadata examination, font anomaly detection, compression analysis, and printer fingerprinting.',
      icon: Scan,
      badge: null
    },
    {
      title: 'Multilingual OCR',
      desc: 'PaddleOCR-powered extraction supporting six Indian languages with named entity recognition.',
      icon: Languages,
      badge: null
    },
    {
      title: 'Cross-Document Consistency',
      desc: 'Verifies the entire loan application as one truth, catching mismatches between documents that isolated checks miss.',
      icon: GitCompare,
      badge: { text: 'Strongest Differentiator', variant: 'default' as const }
    },
    {
      title: 'ITR Special Verification',
      desc: 'Five-sub-layer income tax validation covering format, computation, bank cross-reference, visual authentication, and behavioral analysis.',
      icon: FileText,
      badge: { text: 'Organizer Focus', variant: 'secondary' as const }
    },
    {
      title: 'Fraud DNA Pattern Matching',
      desc: 'Extracts forensic signatures and matches against historical fraud patterns using vector similarity and graph traversal.',
      icon: Dna,
      badge: { text: 'Unique', variant: 'destructive' as const }
    },
    {
      title: 'Risk Intelligence',
      desc: 'Multi-dimensional fraud probability scoring with human-readable explanations and specific regulatory citations.',
      icon: BrainCircuit,
      badge: null
    },
    {
      title: 'Legal Evidence & Audit',
      desc: 'Auto-generated court-ready forensic packages with annotated documents, methodology, and chain-of-custody documentation.',
      icon: Gavel,
      badge: null
    }
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-4 tracking-tight">
            Seven Intelligence Layers
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Each layer catches what others miss, providing impenetrable verification.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {layers.map((layer, i) => {
            const Icon = layer.icon
            const isCenter = i === layers.length - 1 && layers.length % 3 === 1
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.4 }}
                className={`group relative bg-white p-8 rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden ${isCenter ? 'lg:col-start-2' : ''}`}
              >
                {/* Hover Glow Effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-primary-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
                
                <div className="relative z-10 flex flex-col h-full">
                  <div className="flex justify-between items-start mb-6">
                    <div className="w-12 h-12 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center group-hover:bg-primary-50 group-hover:border-primary-100 transition-colors">
                      <Icon className="w-6 h-6 text-primary-700" />
                    </div>
                    {layer.badge && (
                      <Badge variant={layer.badge.variant} className={layer.badge.variant === 'secondary' ? 'bg-amber-100 text-amber-800' : layer.badge.variant === 'destructive' ? 'bg-purple-100 text-purple-800' : ''}>
                        {layer.badge.text}
                      </Badge>
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-primary-900 mb-3">{layer.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed mt-auto">{layer.desc}</p>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
""",

    "components/landing/agents-section.tsx": """'use client'

import { motion } from 'framer-motion'
import { FileSearch, ShieldAlert, GitCompareArrows, FileCheck2, Cpu } from 'lucide-react'

export function AgentsSection() {
  const agents = [
    { icon: FileSearch, name: 'Classifier', role: 'Identifies document types and routes to specialized verifiers' },
    { icon: ShieldAlert, name: 'Forensic Investigator', role: 'Runs multi-technique tamper detection and evidence collection' },
    { icon: GitCompareArrows, name: 'Cross-Reference', role: 'Compares fields across documents and identifies inconsistencies' },
    { icon: FileCheck2, name: 'Compliance', role: 'Validates against RBI, DPDP, and PMLA regulations with citations' },
    { icon: Cpu, name: 'Decision', role: 'Synthesizes findings into recommendations with explainable reasoning' },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-primary-950 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <div className="absolute top-0 right-0 w-full h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary-700 via-primary-950 to-primary-950"></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-4 tracking-tight">
            Agentic AI Architecture
          </h2>
          <p className="text-lg text-primary-200 max-w-2xl mx-auto">
            Five specialized agents collaborate autonomously through LangGraph orchestration.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-5 gap-6">
          {agents.map((agent, i) => {
            const Icon = agent.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15, duration: 0.5 }}
                className="dark-glass rounded-2xl p-6 flex flex-col items-center text-center hover:bg-white/10 transition-colors duration-300 relative"
              >
                {/* Desktop connecting lines except last one */}
                {i < agents.length - 1 && (
                  <div className="hidden md:block absolute top-1/4 -right-3 w-6 h-[2px] bg-white/20"></div>
                )}
                
                <div className="w-14 h-14 rounded-full bg-white/5 border border-white/10 flex items-center justify-center mb-4">
                  <Icon className="w-7 h-7 text-amber-400" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{agent.name}</h3>
                <p className="text-sm text-primary-200 leading-relaxed">{agent.role}</p>
              </motion.div>
            )
          })}
        </div>
        
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 1 }}
          className="mt-16 text-center text-primary-300 text-sm font-mono bg-white/5 py-3 rounded-full max-w-xl mx-auto border border-white/10"
        >
          Powered by CRAG + GraphRAG for verified, contextual AI responses
        </motion.div>
      </div>
    </section>
  )
}
""",

    "components/landing/technology-section.tsx": """'use client'

import { motion } from 'framer-motion'
import { Database, Search, Cpu, Network } from 'lucide-react'

export function TechnologySection() {
  const stack = [
    {
      icon: Database,
      title: 'Bank-Grade Database',
      desc: 'CockroachDB provides distributed SQL with ACID compliance for financial data integrity.',
    },
    {
      icon: Search,
      title: 'Advanced Vector Search',
      desc: 'Qdrant delivers production-grade vector search powering RAG and fraud pattern matching.',
    },
    {
      icon: Cpu,
      title: 'Local LLM Inference',
      desc: 'Ollama runs Phi-3 and Llama models locally with zero external dependencies.',
    },
    {
      icon: Network,
      title: 'Agent Orchestration',
      desc: 'LangGraph coordinates multi-agent workflows with state management and parallel execution.',
    },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white border-t border-border">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-4 tracking-tight">
            Production Architecture <br/> from Day One
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl">
            Built with the stack designed for bank deployment.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stack.map((item, i) => {
            const Icon = item.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
                className="space-y-4"
              >
                <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center">
                  <Icon className="w-6 h-6 text-primary-700" />
                </div>
                <h3 className="text-xl font-bold text-primary-900">{item.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{item.desc}</p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
""",

    "components/landing/compliance-section.tsx": """'use client'

import { motion } from 'framer-motion'
import { WifiOff, Shield, FileCheck, Lock } from 'lucide-react'

export function ComplianceSection() {
  const features = [
    { icon: WifiOff, title: 'Offline-First', desc: 'Sensitive customer data never leaves bank premises. No cloud dependencies at runtime.' },
    { icon: Shield, title: 'DPDP Act Aligned', desc: 'Purpose limitation, consent management, data minimization, and full accountability.' },
    { icon: FileCheck, title: 'Complete Audit Trail', desc: 'Every action logged with timestamps. RBI inspection-ready from day one.' },
    { icon: Lock, title: 'Encrypted by Default', desc: 'AES-256 document encryption. Role-based access control. Sensitive data masking.' },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-[40%_60%] gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-6 tracking-tight">
              Built for <br/>Banking Reality
            </h2>
            <p className="text-lg text-slate-600 mb-8">
              Security, privacy, and compliance by design. We understand that bank data cannot be sent to public API endpoints.
            </p>
            <div className="inline-flex items-center gap-2 bg-green-50 text-green-700 px-4 py-2 rounded-full border border-green-200 font-semibold text-sm">
              <Shield className="w-4 h-4" /> Ready for internal deployment
            </div>
          </motion.div>

          <div className="grid sm:grid-cols-2 gap-6">
            {features.map((f, i) => {
              const Icon = f.icon
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-white p-6 rounded-2xl shadow-sm border border-border"
                >
                  <Icon className="w-8 h-8 text-primary-600 mb-4" />
                  <h3 className="text-lg font-bold text-primary-900 mb-2">{f.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed">{f.desc}</p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}
""",

    "components/landing/differentiator-section.tsx": """'use client'

import { motion } from 'framer-motion'
import { Check, X } from 'lucide-react'

export function DifferentiatorSection() {
  const comparison = [
    { label: 'Document Scope', trad: 'Single-document verification', truth: 'Cross-document intelligence' },
    { label: 'Data Privacy', trad: 'Cloud-dependent AI', truth: 'Completely offline operation' },
    { label: 'Explainability', trad: 'Black-box decisions', truth: 'Explainable AI with regulatory citations' },
    { label: 'Localization', trad: 'Generic fraud detection', truth: 'Indian document context and languages' },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-4 tracking-tight">
            Not Another AI Tool
          </h2>
          <p className="text-lg text-slate-600">
            Purpose-built for Indian banking underwriting.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden"
        >
          {/* Header Row */}
          <div className="grid grid-cols-2 md:grid-cols-[1fr_1fr_1fr] bg-slate-50 border-b border-border p-6 font-bold text-sm uppercase tracking-wider text-slate-500">
            <div className="hidden md:block">Capabilities</div>
            <div className="text-center">Traditional Tools</div>
            <div className="text-center text-primary-700">TruthLens</div>
          </div>
          
          {/* Body Rows */}
          <div className="divide-y divide-border">
            {comparison.map((row, i) => (
              <div key={i} className="grid grid-cols-2 md:grid-cols-[1fr_1fr_1fr] p-6 items-center hover:bg-slate-50 transition-colors">
                <div className="hidden md:block font-medium text-slate-700">{row.label}</div>
                <div className="flex flex-col md:flex-row items-center gap-3 text-center md:text-left text-slate-500 justify-center">
                  <X className="w-5 h-5 text-red-400 shrink-0" />
                  <span className="text-sm">{row.trad}</span>
                </div>
                <div className="flex flex-col md:flex-row items-center gap-3 text-center md:text-left text-primary-900 font-medium justify-center bg-primary-50 py-3 px-4 rounded-xl">
                  <Check className="w-5 h-5 text-green-500 shrink-0" />
                  <span className="text-sm">{row.truth}</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
""",

    "components/landing/cta-section.tsx": """'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function CtaSection() {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 cta-gradient relative overflow-hidden">
      {/* Decorative patterns */}
      <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#000_1px,transparent_1px)] [background-size:20px_20px]"></div>
      
      <div className="max-w-4xl mx-auto text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="space-y-8"
        >
          <h2 className="text-4xl md:text-6xl font-black text-primary-900 tracking-tight">
            Transform Underwriting Today
          </h2>
          <p className="text-xl text-primary-800 max-w-2xl mx-auto">
            Ninety seconds to a decision. Complete forensic evidence. Ready for production.
          </p>
          
          <div className="pt-8">
            <Link href="/login">
              <Button size="lg" className="h-16 px-10 rounded-full bg-primary-900 hover:bg-primary-800 text-white font-bold text-lg shadow-xl hover:scale-105 transition-transform duration-300">
                Access Portal <ArrowRight className="ml-3 w-6 h-6" />
              </Button>
            </Link>
          </div>
          
          <p className="text-sm font-medium text-primary-700/60 pt-8 uppercase tracking-widest">
            Built for Canara Bank SuRaksha Hackathon
          </p>
        </motion.div>
      </div>
    </section>
  )
}
""",

    "components/landing/footer.tsx": """import Link from 'next/link'
import { Shield } from 'lucide-react'

export function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1 space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="bg-primary p-1.5 rounded-md">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-primary-900 tracking-tight">TruthLens</span>
            </Link>
            <p className="text-sm text-slate-500">
              AI-powered document forensics for banking.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-semibold text-primary-900 mb-4">Product</h4>
            <ul className="space-y-3 text-sm text-slate-500">
              <li><Link href="/features" className="hover:text-primary transition-colors">Features</Link></li>
              <li><Link href="/how-it-works" className="hover:text-primary transition-colors">How It Works</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-primary-900 mb-4">Company</h4>
            <ul className="space-y-3 text-sm text-slate-500">
              <li><Link href="/about" className="hover:text-primary transition-colors">About</Link></li>
              <li><Link href="/login" className="hover:text-primary transition-colors">Login</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-primary-900 mb-4">Resources</h4>
            <ul className="space-y-3 text-sm text-slate-500">
              <li><a href="#" className="hover:text-primary transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">API Reference</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-200 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-slate-500">
          <div>© {new Date().getFullYear()} TruthLens</div>
          <div className="font-medium text-slate-400">Built for Canara Bank SuRaksha Hackathon</div>
        </div>
      </div>
    </footer>
  )
}
"""
}

def scaffold_components():
    for path, content in components.items():
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
if __name__ == "__main__":
    scaffold_components()
    print("Scaffolded all 12 landing components.")
