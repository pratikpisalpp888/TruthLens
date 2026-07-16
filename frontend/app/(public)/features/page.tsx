/**
 * PAGE: Features Page
 * ROUTE: /features
 * PURPOSE: Detailed capabilities showcase
 * 
 * CONTENT SECTIONS:
 * - Hero heading "Complete Fraud Intelligence Platform"
 * - 12 detailed feature cards covering:
 *   1. Document Forensics Engine
 *   2. Multilingual OCR
 *   3. Cross-Document Consistency Engine
 *   4. ITR Special Verification Module
 *   5. Fraud DNA Pattern Matching
 *   6. Agentic AI Architecture
 *   7. Advanced RAG System
 *   8. Court-Ready Evidence Generation
 *   9. Explainable AI with Regulatory Citations
 *   10. Live Analysis Visualization
 *   11. Fraud Network Visualization
 *   12. Voice-Powered Assistant
 * - Bottom CTA: "Access Portal"
 * 
 * TO BE IMPLEMENTED IN: Phase 14+
 */

import { Metadata } from 'next'
import { Shield, FileSearch, Fingerprint, RefreshCcw, BrainCircuit, Activity, BarChart3, Database } from 'lucide-react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export const metadata: Metadata = {
  title: 'Features | TruthLens',
  description: 'Explore the advanced features of TruthLens AI-powered document forensics platform.',
}

const features = [
  {
    icon: Shield,
    title: 'Bank-Grade Security',
    description: 'AES-256 encryption for all documents at rest and in transit. Fully compliant with DPDP guidelines, ensuring your data never leaves the secure environment.',
    color: 'text-blue-500',
    bg: 'bg-blue-50'
  },
  {
    icon: BrainCircuit,
    title: 'Agentic AI Analysis',
    description: 'A cutting-edge LangGraph-powered pipeline featuring 5 specialized AI agents working together to scrutinize every detail of loan documents.',
    color: 'text-purple-500',
    bg: 'bg-purple-50'
  },
  {
    icon: FileSearch,
    title: 'Forensic Detection',
    description: 'Error Level Analysis (ELA), metadata extraction, and font consistency checks to detect digital tampering with pinpoint accuracy.',
    color: 'text-emerald-500',
    bg: 'bg-emerald-50'
  },
  {
    icon: RefreshCcw,
    title: 'Cross-Document Consistency',
    description: 'Automatically cross-references names, addresses, and financial figures across multiple documents (e.g., PAN, Aadhaar, ITR, Bank Statements).',
    color: 'text-amber-500',
    bg: 'bg-amber-50'
  },
  {
    icon: Activity,
    title: 'ITR Validation',
    description: 'Specialized module for parsing complex Income Tax Returns, recalculating tax liabilities, and comparing them against claimed income.',
    color: 'text-rose-500',
    bg: 'bg-rose-50'
  },
  {
    icon: Fingerprint,
    title: 'Fraud DNA & Patterns',
    description: 'Extracts unique fraud signatures and compares them against a Qdrant vector database of known fraud patterns to catch repeat offenders.',
    color: 'text-indigo-500',
    bg: 'bg-indigo-50'
  },
  {
    icon: BarChart3,
    title: 'Court-Ready Reports',
    description: 'Automatically generates comprehensive, immutable PDF audit reports detailing all forensic findings for legal compliance and underwriting review.',
    color: 'text-cyan-500',
    bg: 'bg-cyan-50'
  },
  {
    icon: Database,
    title: 'GraphRAG Knowledge Base',
    description: 'Leverages CRAG and GraphRAG to map complex relationships between fraudulent entities, uncovering hidden fraud rings.',
    color: 'text-fuchsia-500',
    bg: 'bg-fuchsia-50'
  }
]

export default function FeaturesPage() {
  return (
    <div className="bg-slate-50 min-h-screen pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl mb-4">
            Advanced Capabilities
          </h1>
          <p className="text-xl text-slate-600">
            Discover how TruthLens combines forensic science with agentic AI to protect Canara Bank from sophisticated document fraud.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon
            return (
              <div key={idx} className="bg-white rounded-2xl p-8 shadow-sm border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className={`w-14 h-14 ${feature.bg} rounded-xl flex items-center justify-center mb-6`}>
                  <Icon className={`w-7 h-7 ${feature.color}`} />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">{feature.title}</h3>
                <p className="text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            )
          })}
        </div>

        <div className="mt-20 bg-primary-900 rounded-3xl p-10 sm:p-16 text-center text-white overflow-hidden relative shadow-2xl">
          <div className="absolute top-0 left-0 w-full h-full bg-[url('/noise.png')] opacity-10 mix-blend-overlay pointer-events-none"></div>
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-3xl font-bold mb-4">Ready to secure your lending process?</h2>
            <p className="text-primary-200 mb-8 text-lg">
              Experience the power of TruthLens and detect document tampering in under 90 seconds.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link href="/login">
                <Button size="lg" className="bg-white text-primary-900 hover:bg-slate-100 font-bold w-full sm:w-auto h-14 px-8 text-lg">
                  Access Demo Portal
                </Button>
              </Link>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}