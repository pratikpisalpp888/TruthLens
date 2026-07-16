/**
 * PAGE: How It Works
 * ROUTE: /how-it-works
 * PURPOSE: Process walkthrough
 * 
 * CONTENT SECTIONS:
 * - Hero: "How TruthLens Works" / "From document upload to fraud detection in 90 seconds"
 * - Journey section: 6 steps - Create Case, Upload Documents, AI Analysis Begins, Real-Time Progress, Comprehensive Results, Officer Decision
 * - Technology highlights section with LangGraph, CockroachDB, Qdrant, Ollama mentions
 * - Time breakdown section: Detailed time distribution showing how 90 seconds is achieved (upload 5s, classification 3s, OCR 15s, forensics 25s, cross-doc 12s, ITR 8s, fraud DNA 5s, compliance 10s, decision 7s)
 * - CTA: "Start your first analysis"
 * 
 * TO BE IMPLEMENTED IN: Phase 14+
 */

import { Metadata } from 'next'
import { Upload, Search, ShieldAlert, FileCheck } from 'lucide-react'

export const metadata: Metadata = {
  title: 'How It Works | TruthLens',
  description: 'Understand the TruthLens 4-step document verification process.',
}

const steps = [
  {
    icon: Upload,
    title: '1. Secure Upload',
    description: 'Upload loan documents (PAN, Aadhaar, ITR, Statements) to the secure, offline TruthLens vault. All files are immediately encrypted with AES-256.'
  },
  {
    icon: Search,
    title: '2. Agentic Analysis',
    description: 'Our LangGraph AI pipeline activates. Specialized agents perform OCR, extract entities, and run deep forensic checks like ELA and font consistency.'
  },
  {
    icon: ShieldAlert,
    title: '3. Cross-Validation & DNA Matching',
    description: 'Data is cross-referenced across all uploaded documents. A unique Fraud DNA signature is generated and checked against our vector database of known frauds.'
  },
  {
    icon: FileCheck,
    title: '4. Court-Ready Report',
    description: 'Within 90 seconds, a comprehensive, immutable PDF report is generated with a Trust Score, highlighting any tampering or inconsistencies for the credit officer.'
  }
]

export default function HowItWorksPage() {
  return (
    <div className="bg-slate-50 min-h-screen pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl mb-4">
            How TruthLens Works
          </h1>
          <p className="text-xl text-slate-600">
            A seamless, automated 4-step process to secure your loan underwriting against sophisticated document fraud.
          </p>
        </div>

        <div className="relative">
          {/* Connecting line for desktop */}
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-1 bg-slate-200 -translate-y-1/2 z-0"></div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative z-10">
            {steps.map((step, idx) => {
              const Icon = step.icon
              return (
                <div key={idx} className="bg-white rounded-2xl p-8 shadow-md border border-slate-200 flex flex-col items-center text-center hover:-translate-y-2 transition-transform duration-300">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-6 text-primary-600 shadow-inner">
                    <Icon className="w-8 h-8" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">{step.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed">
                    {step.description}
                  </p>
                </div>
              )
            })}
          </div>
        </div>

      </div>
    </div>
  )
}