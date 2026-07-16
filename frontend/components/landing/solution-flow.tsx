'use client'

import { motion } from 'framer-motion'
import { UploadCloud, BrainCircuit, ShieldCheck, FileSearch, Network } from 'lucide-react'
import RadialOrbitalTimeline from '@/components/ui/radial-orbital-timeline'
import { SectionTitle } from '@/components/ui/section-title'

const timelineData = [
  {
    id: 1,
    title: "Secure Upload",
    date: "Step 1",
    content: "Upload loan documents (PAN, Aadhaar, ITR, Statements) to the secure, offline TruthLens vault. All files are encrypted with AES-256.",
    category: "Ingestion",
    icon: UploadCloud,
    color: "text-blue-500",
    relatedIds: [2],
    status: "completed" as const,
    energy: 100,
  },
  {
    id: 2,
    title: "Agentic Analysis",
    date: "Step 2",
    content: "Our LangGraph AI pipeline activates. Specialized agents perform OCR, extract entities, and run deep forensic checks like ELA.",
    category: "Processing",
    icon: BrainCircuit,
    color: "text-purple-500",
    relatedIds: [1, 3, 4],
    status: "in-progress" as const,
    energy: 90,
  },
  {
    id: 3,
    title: "Cross-Validation",
    date: "Step 3",
    content: "Data is cross-referenced across all uploaded documents to ensure consistency in names, addresses, and financials.",
    category: "Validation",
    icon: Network,
    color: "text-amber-500",
    relatedIds: [2, 5],
    status: "pending" as const,
    energy: 70,
  },
  {
    id: 4,
    title: "Fraud DNA",
    date: "Step 4",
    content: "A unique Fraud DNA signature is generated and checked against our Qdrant vector database of known frauds.",
    category: "Detection",
    icon: FileSearch,
    color: "text-teal-500",
    relatedIds: [2, 5],
    status: "pending" as const,
    energy: 85,
  },
  {
    id: 5,
    title: "Court-Ready Report",
    date: "Step 5",
    content: "Within 90 seconds, a comprehensive, immutable PDF report is generated with a Trust Score for the credit officer.",
    category: "Output",
    icon: ShieldCheck,
    color: "text-rose-500",
    relatedIds: [3, 4],
    status: "pending" as const,
    energy: 60,
  },
]

export function SolutionFlow() {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50 relative overflow-hidden">
      {/* Decorative Brand Watermarks */}
      <div className="absolute top-20 -right-20 md:-right-40 opacity-10 pointer-events-none select-none">
        <img 
          src="/canara-bank-icon-trans.png" 
          alt="" 
          className="w-80 md:w-[500px] lg:w-[600px] h-auto object-contain transform -rotate-12 blur-[1px]" 
        />
      </div>
      <div className="absolute bottom-20 -left-20 md:-left-32 opacity-[0.08] pointer-events-none select-none">
        <img 
          src="/canara-bank-icon-trans.png" 
          alt="" 
          className="w-64 md:w-96 lg:w-[450px] h-auto object-contain transform rotate-12 blur-[2px]" 
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <SectionTitle
          title="One Platform. Complete Intelligence."
          subtitle="From document upload to court-ready evidence in a seamless, automated process."
          highlight="Complete Intelligence."
        />

        {/* Custom Radial Orbital Timeline */}
        <div className="w-full relative mt-8 flex justify-center items-center">
          <RadialOrbitalTimeline timelineData={timelineData} />
        </div>
      </div>
    </section>
  )
}
