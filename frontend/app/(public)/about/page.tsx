/**
 * PAGE: About Page
 * ROUTE: /about
 * PURPOSE: Company/product story
 * 
 * CONTENT SECTIONS:
 * - Our Story section: Built for Real Banking Problems
 * - Our Mission: Empowering Underwriters Not Replacing Them
 * - What Makes Us Different: 5 points (Offline-First, Agentic AI, Advanced RAG, Cross-Document Intelligence, Production-Grade)
 * - Hackathon section: Built for Canara Bank SuRaksha
 * - Team section (placeholder for team info)
 * - Technology stack list
 * - Contact information
 * 
 * TO BE IMPLEMENTED IN: Phase 14+
 */

import { Metadata } from 'next'
import { CheckCircle2 } from 'lucide-react'

export const metadata: Metadata = {
  title: 'About | TruthLens',
  description: 'About TruthLens and our mission to combat loan document fraud.',
}

export default function AboutPage() {
  return (
    <div className="bg-white min-h-screen pt-24 pb-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl mb-8 text-center">
          About TruthLens
        </h1>
        
        <div className="prose prose-lg prose-slate mx-auto">
          <p className="lead text-xl text-slate-600 mb-8">
            TruthLens was developed specifically for the Canara Bank SuRaksha Hackathon to solve one of the most pressing challenges in modern banking: sophisticated digital document forgery in loan underwriting.
          </p>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-4">Our Mission</h2>
          <p className="text-slate-600 mb-6">
            To empower credit officers with cutting-edge AI and forensic science, enabling them to detect fraudulent documents with unprecedented accuracy and speed, ultimately protecting the bank&apos;s assets and maintaining trust in the financial system.
          </p>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-4">The Challenge</h2>
          <p className="text-slate-600 mb-6">
            With the rise of advanced image editing tools and generative AI, fraudsters can easily manipulate PAN cards, Aadhaar cards, ITR forms, and bank statements. Traditional verification methods are slow and often miss subtle digital tampeirng, leading to significant financial losses due to NPAs (Non-Performing Assets).
          </p>

          <h2 className="text-2xl font-bold text-slate-900 mt-12 mb-4">Our Approach</h2>
          <ul className="space-y-4 mb-8">
            {[
              'Multi-layered forensic analysis targeting metadata, fonts, and error levels (ELA).',
              'Agentic AI pipelines powered by LangGraph for reasoning and decision-making.',
              'Cross-document consistency checks to ensure all claims match across submitted proofs.',
              'Strict adherence to DPDP (Digital Personal Data Protection) guidelines with localized, offline-first processing.'
            ].map((item, idx) => (
              <li key={idx} className="flex items-start">
                <CheckCircle2 className="h-6 w-6 text-primary-500 mr-3 flex-shrink-0 mt-0.5" />
                <span className="text-slate-700">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}